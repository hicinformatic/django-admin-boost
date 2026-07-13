"""Admin module for django-boosted."""

from .index import admin_boost_global_view, get_index_views, register_index_view
from .model import AdminBoostFormat, AdminBoostModel

__all__ = [
    "AdminBoostModel",
    "AdminBoostFormat",
    "admin_boost_global_view",
    "register_index_view",
    "get_index_views",
]
