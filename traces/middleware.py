"""Custom middlewares for the ``traces`` app."""
from django.conf import settings
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
    def process_request(self, request):
        view_name = request.resolver_match.url_name
        if view_name in getattr(settings, 'TRACED_VIEWS', []):
            ip = get_ip(request)
            if not ip:
                return False
            user_agent = request.META.get('HTTP_USER_AGENT', '')[:255]
            user = request.user

            # Check IP and user agent against blacklist
            if (BlacklistIP.objects.filter(ip__exact=ip)
                    or BlacklistUserAgent.objects.filter(
                        user_agent__exact=user_agent)):
                return False

            # Create session key, if unexistant
            if not request.session.session_key:
                request.session.save()
                request.session.modified = True

            # Check if trace exists
            if user.is_authenticated():
                if not Trace.objects.filter(user=user, view_name=view_name):
                    Trace.objects.create(
                        user=user,
                        view_name=view_name,
                        ip=ip,
                        user_agent=user_agent,
                        session_key=request.session.session_key,
                    )
                    return True
                trace = Trace.objects.get(user=user, view_name=view_name)
                trace.hits += 1
                trace.save()
                return True
            if not Trace.objects.filter(
                    session_key=request.session.session_key,
                    view_name=view_name):
                Trace.objects.create(
                    view_name=view_name,
                    ip=ip,
                    user_agent=user_agent,
                    session_key=request.session.session_key,
                )
                return True
            trace = Trace.objects.get(
                session_key=request.session.session_key,
                view_name=view_name)
            trace.hits += 1
            trace.save()
            return True
        return None
