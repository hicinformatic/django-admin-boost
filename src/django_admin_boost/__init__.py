"""Public exports for django-admin-boost."""
default_app_config = "django_admin_boost.apps.DjangoAdminBoostConfig"  # noqa: E402

from .admin import AdminBoostModel  # noqa: E402
from .decorators import admin_boost_view  # noqa: E402

__all__ = [
    "AdminBoostModel",
    "admin_boost_view",
]

__version__ = "0.1.1"
