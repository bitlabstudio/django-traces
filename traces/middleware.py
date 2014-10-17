"""Custom middlewares for the ``traces`` app."""
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import resolve, Resolver404
from django.core.validators import ipv4_re

from .models import BlacklistIP, BlacklistUserAgent, Trace


def get_ip(request):
    """
    Retrieves the remote IP address from the request data.  If the user is
    behind a proxy, they may have a comma-separated list of IP addresses, so
    we need to account for that.  In such a case, only the first IP in the
    list will be retrieved.  Also, some hosts that use a proxy will put the
    REMOTE_ADDR into HTTP_X_FORWARDED_FOR.  This will handle pulling back the
    IP from the proper place.

    """
    ip = request.META.get('HTTP_X_FORWARDED_FOR',
                          request.META.get('REMOTE_ADDR', '127.0.0.1'))
    ip = ipv4_re.match(ip)
    if not ip:
        return None
    return ip.group(0)


class TracesMiddleware(object):
    """
    Middleware that checks if the url name matches a traced view.

    If the trace should be tracked, a new hit is counted.

    """
    def process_response(self, request, response):
        if response.status_code in [404, 500]:
            return response
        try:
            view_name = resolve(request.path_info).url_name
        except Resolver404:
            return response
        if view_name in getattr(settings, 'TRACED_VIEWS', []):
            ip = get_ip(request)
            if not ip:
                return response
            user_agent = request.META.get('HTTP_USER_AGENT', '')[:255]
            user = request.user
            if hasattr(response, 'context_data') and response.context_data:
                view_object = response.context_data.get('object')
            else:
                view_object = None

            # Check IP and user agent against blacklist
            if (BlacklistIP.objects.filter(ip__exact=ip)
                    or BlacklistUserAgent.objects.filter(
                        user_agent__exact=user_agent)):
                return response

            # Create session key, if unexistant
            if not request.session.session_key:
                request.session.modified = True
                request.session.save()

            trace_kwargs = {
                'view_name': view_name,
                'ip': ip,
                'user_agent': user_agent,
                'session_key': request.session.session_key,
            }
            filter_kwargs = {'view_name': view_name}
            if view_object:
                trace_kwargs['view_object'] = view_object
                filter_kwargs['content_type'] = \
                    ContentType.objects.get_for_model(view_object)
                filter_kwargs['object_id'] = view_object.pk

            # Check if trace exists
            if user.is_authenticated():
                filter_kwargs['user'] = user
                trace_kwargs['user'] = user
            else:
                filter_kwargs['session_key'] = request.session.session_key
                trace_kwargs['session_key'] = request.session.session_key
            try:
                trace = Trace.objects.get(**filter_kwargs)
            except Trace.DoesNotExist:
                Trace.objects.create(**trace_kwargs)
                return response
            trace.hits += 1
            trace.save()
            return response
        return response
