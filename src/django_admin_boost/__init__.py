"""Public exports for django-admin-boost."""

from .admin import AdminBoostModel
from .decorators import admin_boost_view

__all__ = [
    "AdminBoostModel",
    "admin_boost_view",
]

__version__ = "0.1.1"
