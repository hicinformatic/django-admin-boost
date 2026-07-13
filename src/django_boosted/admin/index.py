"""Registry for global admin views and the admin index panel."""

from __future__ import annotations

from typing import Callable

from django.urls import NoReverseMatch, reverse

_global_views: list[dict] = []
_index_links: list[dict] = []


def admin_boost_global_view(
    view_type: str,
    label: str,
    *,
    path_fragment: str | None = None,
    template_name: str | None = None,
    permission=None,
    order: int = 0,
    show_in_index: bool = True,
):
    """Register a global (object-less) admin view rendered with the existing
    django-boosted view generators. The decorated function receives ``request``
    (and ``form`` for form/adminform views on valid POST) and returns a form or
    a context dict, exactly like the model-level boost views."""

    def decorator(func: Callable) -> Callable:
        name = func.__name__
        if any(entry["name"] == name for entry in _global_views):
            return func
        _global_views.append(
            {
                "func": func,
                "name": name,
                "view_type": view_type,
                "label": label,
                "path_fragment": path_fragment or name.replace("_", "-"),
                "template_name": template_name,
                "permission": permission,
                "order": order,
                "show_in_index": show_in_index,
            }
        )
        return func

    return decorator


def register_index_view(label, url, *, permission=None, order=0):
    """Register a plain link in the admin index panel (e.g. pointing to an
    existing admin view). ``url`` may be a resolved path or ``reverse_lazy(...)``."""
    _index_links.append(
        {"label": label, "url": url, "permission": permission, "order": order}
    )


def get_global_views() -> list[dict]:
    return list(_global_views)


def check_permission(permission, request) -> bool:
    user = getattr(request, "user", None)
    if permission is None:
        return bool(user and user.is_staff)
    if callable(permission):
        return bool(permission(request))
    return bool(user and user.has_perm(permission))


def get_index_views(request) -> list[dict]:
    """Return the visible panel entries for the current user, sorted by order."""
    items: list[dict] = []
    for entry in _global_views:
        if not entry["show_in_index"]:
            continue
        if not check_permission(entry["permission"], request):
            continue
        try:
            url = reverse(f"admin:django_boosted_boostedview_{entry['name']}")
        except NoReverseMatch:
            continue
        items.append(
            {"label": entry["label"], "url": url, "order": entry["order"]}
        )
    for link in _index_links:
        if not check_permission(link["permission"], request):
            continue
        items.append(
            {"label": link["label"], "url": str(link["url"]), "order": link["order"]}
        )
    items.sort(key=lambda item: (item["order"], str(item["label"])))
    return items
