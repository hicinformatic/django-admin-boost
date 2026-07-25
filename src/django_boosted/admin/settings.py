from __future__ import annotations

import json
from typing import Any

from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from .format import reveal_html

SIMPLE_TYPES = (str, int, float, bool, type(None))


def _is_simple(value: Any) -> bool:
    return isinstance(value, SIMPLE_TYPES)


def _as_json(value: Any) -> str | None:
    """Return a pretty JSON string when the value is JSON-serializable."""
    try:
        return json.dumps(value, indent=2, ensure_ascii=False, sort_keys=True)
    except (TypeError, ValueError):
        return None


class SettingAdmin(admin.ModelAdmin):
    list_display = ["name", "display_value"]
    search_fields = ["name"]
    readonly_fields = ["name", "display_full_value"]
    fields = ["name", "display_full_value"]

    class Media:
        css = {"all": ("admin_boost/admin_boost.css",)}

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return True

    @admin.display(description=_("Value"))
    def display_value(self, obj):
        if _is_simple(obj.value):
            return reveal_html(str(obj.value))
        return _("complexe")

    @admin.display(description=_("Value"))
    def display_full_value(self, obj):
        if _is_simple(obj.value):
            return reveal_html(str(obj.value))
        as_json = _as_json(obj.value)
        if as_json is not None:
            return reveal_html(format_html("<pre class='boost-json'>{}</pre>", as_json))
        return _("complexe")
