from django.db import models
from django.utils.translation import gettext_lazy as _

from django_boosted.managers import SettingManager
from django_boosted.models.fields import SecretTextField


class SettingModel(models.Model):
    name: models.CharField = models.CharField(
        max_length=255, primary_key=True, verbose_name=_("Name")
    )
    value = SecretTextField(verbose_name=_("Value"), blank=True)

    objects = SettingManager()

    def __str__(self) -> str:
        return str(self.name)

    class Meta:
        verbose_name = _("Setting")
        verbose_name_plural = _("Settings")
