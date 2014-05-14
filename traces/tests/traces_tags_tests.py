"""Test for the template tags of the ``traces`` app."""
from django.test import TestCase

from django_libs.tests.factories import UserFactory
from mock import Mock

from ..templatetags import traces_tags
from . import factories


class GetViewHitsTestCase(TestCase):
    """Tests for the ``get_view_hits`` template tag."""
    longMessage = True

    def test_tag(self):
        self.assertEqual(traces_tags.get_view_hits({}, 'test_view'), 0, msg=(
            'Should return one hit.'))

        with self.settings(TRACED_VIEWS=['view_with_hits']):
            factories.TraceFactory(view_name='view_with_hits', hits='4')
            self.assertEqual(
                traces_tags.get_view_hits({}, 'view_with_hits'), 4,
                msg=('Should return five hits.'))

        with self.settings(TRACED_VIEWS=[]):
            self.assertIsNone(traces_tags.get_view_hits({}, 'test_view'))

            request = Mock()
            request.path_info = '/inexistant-view/'
            context = {'request': request}
            self.assertIsNone(traces_tags.get_view_hits(context))

        with self.settings(TRACED_VIEWS=['view_with_an_object']):
            context = {'object': UserFactory()}
            self.assertEqual(
                traces_tags.get_view_hits(context, 'view_with_an_object'), 0,
                msg=('Should return five hits.'))
