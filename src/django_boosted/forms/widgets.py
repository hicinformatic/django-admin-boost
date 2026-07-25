"""Form widgets for django-boosted."""

from django import forms


class RevealWidget(forms.TextInput):
    """Password-style input with a button to toggle plain-text visibility."""

    input_type = "password"
    template_name = "admin_boost/widgets/reveal.html"

    class Media:
        css = {"all": ("admin_boost/admin_boost.css",)}
