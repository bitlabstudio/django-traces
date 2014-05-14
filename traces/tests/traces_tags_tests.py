"""Test for the template tags of the ``traces`` app."""
from django.test import TestCase

from ..templatetags import traces_tags
from . import factories


class GetViewHitsTestCase(TestCase):
    """Tests for the ``get_view_hits`` template tag."""
    longMessage = True

    def test_tag(self):
        self.assertEqual(traces_tags.get_view_hits({}, 'test_view'), 1, msg=(
            'Should return one hit.'))

        with self.settings(TRACED_VIEWS=['view_with_hits']):
            factories.TraceFactory(view_name='view_with_hits', hits='4')
            self.assertEqual(
                traces_tags.get_view_hits({}, 'view_with_hits'), 5,
                msg=('Should return five hits.'))

        with self.settings(TRACED_VIEWS=[]):
            self.assertIsNone(traces_tags.get_view_hits({}, 'test_view'))