"""Django app configuration."""

from django.apps import AppConfig


class DjangoAdminBoostConfig(AppConfig):
    """Configuration for the django-admin-boost app."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "django_admin_boost"
    verbose_name = "Django Admin Boost"

    def ready(self):
        from django.contrib import admin

        from django_admin_boost.models.urls import UrlModel

        if not admin.site.is_registered(UrlModel):
            from django_admin_boost.admin.urls import UrlAdmin
            admin.site.register(UrlModel, UrlAdmin)