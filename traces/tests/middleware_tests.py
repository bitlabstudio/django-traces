"""Tests for the middlewares of the ``traces`` app."""
from django.contrib.auth.models import AnonymousUser
from django.test import TestCase

from django_libs.tests.factories import UserFactory
from mock import Mock

from factories import BlacklistIPFactory
from ..middleware import TracesMiddleware
from ..models import Trace


class TraceMiddlewareTestCase(TestCase):
    longMessage = True

    def setUp(self):
        self.middleware = TracesMiddleware()
        self.request = Mock()
        self.request.user = AnonymousUser()
        self.request.session.session_key = 'foobar'
        self.request.resolver_match.url_name = 'test_view'
        self.request.META = {'HTTP_USER_AGENT': ''}

    def test_untraced_view(self):
        self.assertIsNone(self.middleware.process_request(self.request))

    def test_traced_view(self):
        with self.settings(TRACED_VIEWS=['test_view']):
            # Anonymous user
            self.assertTrue(self.middleware.process_request(self.request))
            self.assertEqual(Trace.objects.count(), 1, msg=(
                'A new trace should have been created.'))

            self.assertTrue(self.middleware.process_request(self.request))
            self.assertEqual(Trace.objects.count(), 1, msg=(
                'No new trace should have been created.'))
            self.assertEqual(Trace.objects.all()[0].hits, 2, msg=(
                'Hits should have been increased.'))

            BlacklistIPFactory(ip=Trace.objects.get().ip)
            self.assertFalse(self.middleware.process_request(self.request))

            self.request.session.session_key = ''
            self.request.META['HTTP_X_FORWARDED_FOR'] = '1.1.1.1'
            self.assertTrue(self.middleware.process_request(self.request))

            # Logged in user
            self.request.user = UserFactory()
            self.assertTrue(self.middleware.process_request(self.request))
            self.assertEqual(Trace.objects.count(), 3, msg=(
                'A new trace should have been created.'))

            self.assertTrue(self.middleware.process_request(self.request))
            self.assertEqual(Trace.objects.count(), 3, msg=(
                'No new trace should have been created.'))
            self.assertEqual(Trace.objects.all()[0].hits, 2, msg=(
                'Hits should have been increased.'))

            self.request.META['HTTP_X_FORWARDED_FOR'] = '1.1.1.1.1.1.1'
            self.assertFalse(self.middleware.process_request(self.request))
