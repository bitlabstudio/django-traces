"""Admin registration for the ``test_app`` app."""
from django.contrib import admin

from . import models


admin.site.register(models.DummyModel)
