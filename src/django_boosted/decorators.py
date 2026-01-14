"""Decorators for django-boosted."""

from __future__ import annotations

from typing import Callable


def admin_boost_view(
    view_type: str,
    label: str,
    template_name: str | None = None,
    path_fragment: str | None = None,
    requires_object: bool | None = None,
    permission: str = "view",
):
    def decorator(func: Callable) -> Callable:
        func._admin_boost_view_config = {  # type: ignore[attr-defined]
            "name": func.__name__,
            "view_type": view_type,
            "label": label,
            "template_name": template_name,
            "path_fragment": path_fragment,
            "requires_object": requires_object,
            "permission": permission,
        }
        return func

    return decorator
