"""Factories for the ``traces`` app."""
from factory import DjangoModelFactory, Sequence

from .. import models


class TraceFactory(DjangoModelFactory):
    FACTORY_FOR = models.Trace

    ip = Sequence(lambda x: '66.66.66.{}'.format(x))


class BlacklistIPFactory(DjangoModelFactory):
    FACTORY_FOR = models.BlacklistIP

    ip = Sequence(lambda x: '77.77.77.{}'.format(x))


class BlacklistUserAgentFactory(DjangoModelFactory):
    FACTORY_FOR = models.BlacklistUserAgent

    user_agent = Sequence(lambda x: 'user_agent_{}'.format(x))
