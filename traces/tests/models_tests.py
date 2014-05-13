"""Tests for the models of the ``traces`` app."""
from django.test import TestCase

from . import factories


class TraceTestCase(TestCase):
    def setUp(self):
        self.instance = factories.TraceFactory()

    def test_model(self):
        self.assertTrue(self.instance.pk)


class BlacklistIPTestCase(TestCase):
    def setUp(self):
        self.instance = factories.BlacklistIPFactory()

    def test_model(self):
        self.assertTrue(self.instance.pk)


class BlacklistUserAgentTestCase(TestCase):
    def setUp(self):
        self.instance = factories.BlacklistUserAgentFactory()

    def test_model(self):
        self.assertTrue(self.instance.pk)
