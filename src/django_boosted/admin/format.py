"""Formatting utilities for django-boosted."""

from django.utils.html import format_html
from django.templatetags.static import static
from django.utils.translation import gettext_lazy as _

_REVEAL_JS = (
    "const w=this.previousElementSibling,"
    "m=w.querySelector('.boost-secret-mask'),"
    "v=w.querySelector('.boost-secret-value'),"
    "s=v.style.display!=='none';"
    "v.style.display=s?'none':'';"
    "m.style.display=s?'':'none';"
)


def reveal_html(content, mask="••••••••"):
    """Wrap read-only content so it is masked by default with a reveal toggle."""
    return format_html(
        '<span class="boost-reveal">'
        '<span class="boost-secret">'
        '<span class="boost-secret-mask">{}</span>'
        '<span class="boost-secret-value" style="display:none">{}</span>'
        '</span>'
        '<img class="boost-reveal-toggle" src="{}" alt="{}" '
        'onclick="' + _REVEAL_JS + '">'
        '</span>',
        mask,
        content,
        static("admin/img/icon-viewlink.svg"),
        _("Reveal"),
    )


def boolean_icon_html(value):
    """Return the HTML image (admin icon) for a boolean value."""
    is_ok = value == "✓" if isinstance(value, str) else bool(value)
    icon = "icon-yes.svg" if is_ok else "icon-no.svg"
    return format_html(
        '<img src="{}" alt="{}">',
        static(f"admin/img/{icon}"),
        _("Yes") if is_ok else _("No"),
    )


def format_label(
    text: str,
    label_type: str = "info",
    size: str | None = None,
    link: str | None = None,
    style: str | None = None,
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
    tag = "a" if link else "span"
    if link and style:
        return format_html(
            '<{} href="{}" class="{}" style="{}">{}</{}>',
            tag,
            link,
            css_class,
            style,
            text,
            tag,
        )
    if link:
        return format_html(
            '<{} href="{}" class="{}">{}</{}>', tag, link, css_class, text, tag
        )
    if style:
        return format_html(
            '<{} class="{}" style="{}">{}</{}>', tag, css_class, style, text, tag
        )
    return format_html('<{} class="{}">{}</{}>', tag, css_class, text, tag)


def format_status(
    name: str, status: bool, style: str | None = None, link: str | None = None
) -> str:
    icon = "✓" if status else "✗"
    status_class = "success" if status else "error"
    tag = "a" if link else "span"
    return format_html(
        '<{} href="{}"><span class="boost-status {}" style="{}">{}</span> '
        '<code>{}</code></{}>',
        tag,
        link,
        status_class,
        style,
        icon,
        name,
        tag,
    )


def format_with_help_text(html_content: str, help_text: str | None = None) -> str:
    if help_text:
        return format_html(
            '{}<br><small class="help">{}</small>', html_content, help_text
        )
    return html_content
