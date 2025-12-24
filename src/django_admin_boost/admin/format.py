"""Formatting utilities for django-admin-boost."""

from django.utils.html import format_html


def format_label(
    text: str, label_type: str = "info", size: str | None = None, link: bool = False
) -> str:
    classes = ["boost-label"]
    valid_types = [
        "success",
        "info",
        "warning",
        "danger",
        "primary",
        "secondary",
        "default",
    ]
    if label_type.lower() in valid_types:
        classes.append(label_type.lower())
    else:
        classes.append("info")
    if size and size.lower() in ["small", "big"]:
        classes.append(size.lower())
    if link:
        classes.append("link")
    css_class = " ".join(classes)
    return format_html('<span class="{}">{}</span>', css_class, text)


def format_status(name: str, status: bool) -> str:
    icon = "✓" if status else "✗"
    status_class = "success" if status else "error"
    return format_html(
        '<span class="boost-status {}">{}</span> <code>{}</code>',
        status_class,
        icon,
        name,
    )
