"""URLs to run the tests."""
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import DetailView, TemplateView

from test_app.models import DummyModel


admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^(?P<pk>\d+)/$',
        DetailView.as_view(model=DummyModel, template_name='base.html'),
        name='test_dummy_view'),
    url(r'^$', TemplateView.as_view(template_name='base.html'),
        name='test_view'),
)
