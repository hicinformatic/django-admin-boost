from django import get_version
from django.contrib import admin

from django_admin_boost import AdminBoostModel, admin_boost_view
from django_admin_boost import __version__ as admin_boost_version

from .models import Alphabet, Country


class CountryAdmin(AdminBoostModel):
    boost_views = [
        "custom_message_view",
        "custom_json_view",
        "custom_list_view",
        "custom_form_view",
        "custom_message_object_view",
        "custom_list_object_view",
        "custom_json_object_view",
        "custom_form_object_view",
    ]
    search_fields = ["name"]
    list_display = [
        "name",
        "label_link_success_small",
        "label_link_info_small",
        "label_link_warning_default",
        "label_link_danger_default",
        "label_link_primary_big",
        "label_link_secondary_big",
        "label_link_default_big",
    ]

    @admin.display(description="Success Small")
    def label_link_success_small(self, obj):
        return self.format_label("Success", "success", size="small", link=True)

    @admin.display(description="Info Small")
    def label_link_info_small(self, obj):
        return self.format_label("Info", "info", size="small", link=True)

    @admin.display(description="Warning Default")
    def label_link_warning_default(self, obj):
        return self.format_label("Warning", "warning", link=True)

    @admin.display(description="Danger Default")
    def label_link_danger_default(self, obj):
        return self.format_label("Danger", "danger", link=True)

    @admin.display(description="Primary Big")
    def label_link_primary_big(self, obj):
        return self.format_label("Primary", "primary", size="big", link=True)

    @admin.display(description="Secondary Big")
    def label_link_secondary_big(self, obj):
        return self.format_label("Secondary", "secondary", size="big", link=True)

    @admin.display(description="Default Big")
    def label_link_default_big(self, obj):
        return self.format_label("Default", "default", size="big", link=True)

    @admin_boost_view("message", "Custom Message View")
    def custom_message_view(self, request):
        return {"message": "This is a custom message view"}

    @admin_boost_view("json", "Custom JSON View")
    def custom_json_view(self, request):
        return {
            "json_custom": [
                {"name": "Custom 1", "id": 1},
                {"name": "Custom 2", "id": 2},
                {"name": "Custom 3", "id": 3},
            ]
        }

    @admin_boost_view("list", "Custom List View")
    def custom_list_view(self, request):
        object_list = [
            {"name": "Custom 1", "id": 1},
            {"name": "Custom 2", "id": 2},
            {"name": "Custom 3", "id": 3},
        ]
        return {"object_list": object_list}

    @admin_boost_view("form", "Custom Form View")
    def custom_form_view(self, request):
        return {"form": "This is a custom form view"}

    @admin_boost_view("json", "Custom Json Object View")
    def custom_json_object_view(self, request, obj):
        return {"object_json": {"name": "Custom 1", "id": 1}}

    @admin_boost_view("message", "Custom Message Object View")
    def custom_message_object_view(self, request, obj):
        return {"message": f"This is a custom message object view for {obj}"}

    @admin_boost_view("list", "Custom List Object View")
    def custom_list_object_view(self, request, obj):
        object_list = [
            {"name": "Custom 1", "id": 1},
            {"name": "Custom 2", "id": 2},
            {"name": "Custom 3", "id": 3},
        ]
        return {"object_list": object_list}

    @admin_boost_view("form", "Custom Form Object View")
    def custom_form_object_view(self, request, obj):
        return {"form": "This is a custom form object view"}


class AlphabetAdmin(AdminBoostModel):
    list_display = ["name", "country", "status_example_1", "status_example_2"]
    search_fields = ["name", "country__name"]
    autocomplete_fields = ["country"]

    @admin.display(description="Status Example 1")
    def status_example_1(self, obj):
        return self.format_status("django", True)

    @admin.display(description="Status Example 2")
    def status_example_2(self, obj):
        return self.format_status("pytest", False)


admin.site.register(Country, CountryAdmin)
admin.site.register(Alphabet, AlphabetAdmin)

admin.site.site_header = (
    f"Django ({get_version()}) Admin boost ({admin_boost_version}) - Administration"
)
admin.site.site_title = f"Django ({get_version()}) Admin boost ({admin_boost_version})"
admin.site.index_title = "Administration"
