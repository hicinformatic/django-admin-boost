from django.db import models
from django.utils.translation import gettext_lazy as _


class BoostedView(models.Model):
    """Virtual host for global admin views. No table is created (managed=False);
    it only provides admin URLs and context for views registered via
    ``admin_boost_global_view``."""

    class Meta:
        managed = False
        default_permissions = ()
        verbose_name = _("Boosted")
        verbose_name_plural = _("Boosted")
