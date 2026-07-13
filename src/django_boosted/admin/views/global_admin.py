"""Host ModelAdmin that exposes global boosted views under the admin.

Kept out of ``admin/views/__init__.py`` on purpose: importing ``..model`` here
would create a circular import if this module were loaded while ``admin.model``
is still initializing.
"""

from __future__ import annotations

from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.urls import path

from ..index import check_permission, get_global_views
from ..model import AdminBoostModel
from .generator import ViewGenerator


class BoostedViewAdmin(AdminBoostModel):
    """Runs global views on a virtual model. Hidden from the app index and
    without persistence: the default changelist redirects to the admin index
    and full-count queries are disabled so the missing table is never hit."""

    show_full_result_count = False

    def has_module_permission(self, request):
        return False

    def has_view_permission(self, request, obj=None):
        return bool(getattr(request, "user", None) and request.user.is_staff)

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        # Enables the default "Save" button on adminform views (Django's
        # submit_row shows it only when the user can add or change).
        return bool(getattr(request, "user", None) and request.user.is_staff)

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        return redirect("admin:index")

    def changeform_view(
        self, request, object_id=None, form_url="", extra_context=None
    ):
        # The virtual host has no table; the default add/change pages would hit
        # a missing table. Global views are served from their own URLs.
        return redirect("admin:index")

    def _guard(self, view, permission):
        def wrapped(request, *args, **kwargs):
            if not check_permission(permission, request):
                raise PermissionDenied
            return view(request, *args, **kwargs)

        return wrapped

    def get_urls(self):
        generator = ViewGenerator(self)
        opts = self.model._meta
        boost_urls = []
        for entry in get_global_views():
            method = getattr(
                generator,
                f"generate_admin_custom_{entry['view_type']}_view",
                None,
            )
            if method is None:
                continue
            kwargs = {
                "path_fragment": entry["path_fragment"],
                "requires_object": False,
            }
            if entry.get("template_name"):
                key = (
                    "_template_name"
                    if entry["view_type"] == "json"
                    else "template_name"
                )
                kwargs[key] = entry["template_name"]
            view = method(entry["func"], entry["label"], **kwargs)
            guarded = self._guard(view, entry["permission"])
            boost_urls.append(
                path(
                    f"{entry['path_fragment']}/",
                    self.admin_site.admin_view(guarded),
                    name=f"{opts.app_label}_{opts.model_name}_{entry['name']}",
                )
            )
        return boost_urls + super().get_urls()
