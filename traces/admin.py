"""Admin registration for the ``traces`` app."""
from django.contrib import admin

from . import models


admin.site.register(models.BlacklistIP)
admin.site.register(models.BlacklistUserAgent)
admin.site.register(models.Trace)
