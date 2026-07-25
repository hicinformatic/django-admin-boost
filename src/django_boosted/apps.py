"""Django app configuration."""

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class DjangoBoostedConfig(AppConfig):
    """Configuration for the django-boosted app."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "django_boosted"
    verbose_name = _("Django Boosted")

    def ready(self):
        from importlib import import_module

        from django.conf import settings
        from django.contrib import admin
        from django.utils.module_loading import autodiscover_modules

        from django_boosted.models.urls import UrlModel

        if not admin.site.is_registered(UrlModel):
            from django_boosted.admin.urls import UrlAdmin
            admin.site.register(UrlModel, UrlAdmin)

        from django_boosted.models.settings import SettingModel

        if not admin.site.is_registered(SettingModel):
            from django_boosted.admin.settings import SettingAdmin
            admin.site.register(SettingModel, SettingAdmin)

        from django_boosted.admin.views.global_admin import BoostedViewAdmin
        from django_boosted.models.global_view import BoostedView

        if not admin.site.is_registered(BoostedView):
            admin.site.register(BoostedView, BoostedViewAdmin)

        if not admin.site.index_template:
            admin.site.index_template = "admin_boost/index.html"

        autodiscover_modules("boosted_views")
        for module_path in getattr(settings, "DJANGO_BOOSTED_VIEW_MODULES", []):
            import_module(module_path)
