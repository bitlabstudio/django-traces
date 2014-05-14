"""Models for the ``traces`` app."""
from django.db import models
from django.conf import settings
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType


class Trace(models.Model):
    """
    Model to track a user's view hits.

    :creation_date: Auto-added datetime of the model creation.
    :view_name: Name of the called view.
    :ip: IP of the visitor.
    :user_agent: User agent of the request.
    :session_key: Session key in the request.
    :user: User who called the website, if not anonymous.
    :view_object: Object of the called view.
    :hits: Hit count of the user/view combination.

    """
    creation_date = models.DateTimeField(
        auto_now_add=True,
        editable=False,
        verbose_name=('Creation date'),
    )

    view_name = models.CharField(
        max_length=50,
        verbose_name=('View name'),
    )

    ip = models.IPAddressField(
        verbose_name=('IP'),
    )

    session_key = models.CharField(
        max_length=40,
        verbose_name=('Session key'),
    )

    user_agent = models.CharField(
        max_length=255,
        verbose_name=('User agent'),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True, blank=True,
        verbose_name=('User'),
    )

    # GFK 'view_object'
    content_type = models.ForeignKey(ContentType, blank=True, null=True)
    object_id = models.PositiveIntegerField(blank=True, null=True)
    view_object = generic.GenericForeignKey('content_type', 'object_id')

    hits = models.PositiveIntegerField(
        default=1,
        verbose_name=('Hits'),
    )

    class Meta:
        ordering = ('-creation_date', )

    def __unicode__(self):
        return u'{} ({})'.format(self.view_name, self.ip)


class BlacklistIP(models.Model):
    """
    Model to contain information about unwanted IPs.

    :ip: IP to be blacklisted.
    :description: Optional description of this entry.

    """
    ip = models.IPAddressField(
        verbose_name=('IP'),
        unique=True,
    )

    description = models.TextField(
        max_length=1024,
        verbose_name=('Description'),
        blank=True,
    )

    class Meta:
        ordering = ('ip', )

    def __unicode__(self):
        return u'{}'.format(self.ip)


class BlacklistUserAgent(models.Model):
    """
    Model to contain information about unwanted user agents.

    :user_agent: User agent to be blacklisted.
    :description: Optional description of this entry.

    """
    user_agent = models.CharField(
        max_length=255,
        verbose_name=('User agent'),
        unique=True,
    )

    description = models.TextField(
        max_length=1024,
        verbose_name=('Description'),
        blank=True,
    )

    class Meta:
        ordering = ('user_agent', )

    def __unicode__(self):
        return u'{}'.format(self.user_agent)
