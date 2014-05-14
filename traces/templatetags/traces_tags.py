"""Template tags for the ``traces`` app."""
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import resolve, Resolver404
from django.db.models import Sum
from django.template import Library

from ..models import Trace


register = Library()


@register.assignment_tag(takes_context=True)
def get_view_hits(context, view_name='', view_object=None):
    """Simply returns the amount of hits for this view."""
    try:
        view_name = view_name or resolve(context['request'].path_info).url_name
    except Resolver404:
        return None
    if view_name not in getattr(settings, 'TRACED_VIEWS', []):
        # If it's not a traced view return None
        return None
    filter_kwargs = {'view_name': view_name}
    view_object = view_object or context.get('object')
    if view_object:
        filter_kwargs['content_type'] = \
            ContentType.objects.get_for_model(view_object)
        filter_kwargs['object_id'] = view_object.pk
    traces = Trace.objects.filter(**filter_kwargs)
    if traces:
        # If there are saved traces aggregate their hits
        # Since the hit is updated with the view response (and not yet saved)
        # we can already add a 1
        return traces.aggregate(hits=Sum('hits'))['hits']
    # If it's a traced view we know that a new trace will be created with
    # the response, so we return one hit
    return 0
