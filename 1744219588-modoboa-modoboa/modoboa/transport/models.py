"""Transport models."""

from reversion import revisions as reversion

from django.core.serializers.json import DjangoJSONEncoder
from django.db import models
from django.utils.translation import gettext_lazy as _

from . import backends


class Transport(models.Model):
    """Transport table."""

    pattern = models.CharField(_("pattern"), unique=True, max_length=253, db_index=True)
    service = models.CharField(_("service"), max_length=30)
    next_hop = models.CharField(_("next hop"), max_length=100, blank=True)

    _settings = models.JSONField(default=dict, encoder=DjangoJSONEncoder)

    class Meta:
        ordering = ["pattern"]

    def __str__(self):
        return self.pattern

    @property
    def backend(self):
        """Shortcut to access backend."""
        if not self.service:
            return None
        return backends.manager.get_backend(self.service)


reversion.register(Transport)
