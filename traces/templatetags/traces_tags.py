"""Template tags for the ``traces`` app."""
from django.core.urlresolvers import resolve
from django.db.models import Sum
from django.template import Library

from ..models import Trace


register = Library()


@register.assignment_tag(takes_context=True)
def get_view_hits(context, view_name=''):
    """Simply returns the amount of hits for this view."""
    view_name = view_name or resolve(context['request'].path_info).url_name
    traces = Trace.objects.filter(view_name=view_name)
    return traces.aggregate(hits=Sum('hits')).get('hits')
