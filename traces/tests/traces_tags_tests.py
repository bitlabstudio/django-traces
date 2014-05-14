"""Test for the template tags of the ``traces`` app."""
from django.test import TestCase

from django_libs.tests.factories import UserFactory

from ..templatetags import traces_tags
from . import factories


class GetViewHitsTestCase(TestCase):
    """Tests for the ``get_view_hits`` template tag."""
    longMessage = True

    def test_tag(self):
        self.assertIsNone(traces_tags.get_view_hits({}, 'test_view'))
