"""Template tags for the ``traces`` app."""
from django.conf import settings
from django.core.urlresolvers import resolve
from django.db.models import Sum
from django.template import Library

from ..models import Trace


register = Library()


@register.assignment_tag(takes_context=True)
def get_view_hits(context, view_name=''):
    """Simply returns the amount of hits for this view."""
    view_name = view_name or resolve(context['request'].path_info).url_name
    if view_name not in getattr(settings, 'TRACED_VIEWS', []):
        # If it's not a traced view return None
        return None
    traces = Trace.objects.filter(view_name=view_name)
    if traces:
        # If there are saved traces aggregate their hits
        # Since the hit is updated with the view response (and not yet saved)
        # we can already add a 1
        return traces.aggregate(hits=Sum('hits'))['hits'] + 1
    # If it's a traced view we know that a new trace will be created with
    # the response, so we return one hit
    return 1
