"""Auto-discovered global boosted views (via autodiscover_modules)."""

from django_boosted import admin_boost_global_view


@admin_boost_global_view("message", "Global hello")
def global_hello_view(request):
    return {"message": "Hello from a global boosted view"}
