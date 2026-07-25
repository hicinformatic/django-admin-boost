from __future__ import annotations

from typing import Any

from django.conf import settings
from virtualqueryset.managers import VirtualManager  # type: ignore[import-untyped]


class SettingManager(VirtualManager):
    """
    Collects Django configuration settings as a virtual queryset.

    Each entry exposes the setting name and its raw value. The value keeps its
    original Python type so the admin can decide how to render it (simple text,
    pretty JSON or an opaque "complexe" placeholder).
    """

    def get_data(self) -> list[dict[str, Any]]:
        data: list[dict[str, Any]] = []
        for name in dir(settings):
            if not name.isupper():
                continue
            try:
                value = getattr(settings, name)
            except Exception:  # pragma: no cover - defensive against lazy settings
                continue
            data.append({"name": name, "value": value})
        return data

    def get_queryset(self):
        return super().get_queryset().order_by("name")
