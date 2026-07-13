import secrets

import pytest
from django.contrib.auth import get_user_model
from django.test import Client as DjangoClient
from django.urls import reverse

from tests.app.models import Country


@pytest.fixture()
def superuser(db):
    User = get_user_model()
    return User.objects.create_superuser(
        username="admin",
        email="admin@example.com",
        password=secrets.token_urlsafe(16),
    )


@pytest.fixture()
def admin_client(superuser):
    client = DjangoClient()
    client.force_login(superuser)
    return client


@pytest.fixture()
def staff_user(db):
    User = get_user_model()
    return User.objects.create_user(
        username="staff",
        email="staff@example.com",
        password=secrets.token_urlsafe(16),
        is_staff=True,
    )


@pytest.fixture()
def plain_user(db):
    User = get_user_model()
    return User.objects.create_user(
        username="joe",
        email="joe@example.com",
        password=secrets.token_urlsafe(16),
    )


def _client(user):
    client = DjangoClient()
    client.force_login(user)
    return client


@pytest.mark.django_db()
def test_boost_view_renders_context(admin_client):
    country_obj = Country.objects.create(name="Alice")
    url = reverse(
        "admin:tests_app_country_custom_message_object_view", args=[country_obj.pk]
    )

    response = admin_client.get(url)

    assert response.status_code == 200
    content = response.content.decode()
    assert f"This is a custom message object view for {country_obj}" in content


@pytest.mark.django_db()
def test_redirect_view(admin_client):
    """Redirect view returns 302 and redirects to the expected URL."""
    country_obj = Country.objects.create(name="Bob")
    url = reverse(
        "admin:tests_app_country_custom_redirect_object_view", args=[country_obj.pk]
    )

    response = admin_client.get(url)

    assert response.status_code == 302
    changelist_url = reverse("admin:tests_app_country_changelist")
    assert response.url == changelist_url


@pytest.mark.django_db()
def test_object_tools_button_is_visible(admin_client):
    country_obj = Country.objects.create(name="Bob")
    change_url = reverse("admin:tests_app_country_change", args=[country_obj.pk])

    response = admin_client.get(change_url)

    assert response.status_code == 200
    content = response.content.decode()
    assert "Redirect to changelist" in content


@pytest.mark.django_db()
def test_index_panel_lists_global_views(superuser):
    response = _client(superuser).get(reverse("admin:index"))

    assert response.status_code == 200
    content = response.content.decode()
    assert 'id="boosted-index-views-module"' in content
    assert "Global action" in content
    assert "Global countries" in content
    assert "Global hello" in content  # discovered via boosted_views.py convention


@pytest.mark.django_db()
def test_global_adminform_view_renders_raw_id_fields(superuser):
    url = reverse("admin:django_boosted_boostedview_global_action_view")

    response = _client(superuser).get(url)

    assert response.status_code == 200
    content = response.content.decode()
    assert "vForeignKeyRawIdAdminField" in content
    assert 'id="lookup_id_user"' in content
    assert 'id="lookup_id_country"' in content


@pytest.mark.django_db()
def test_global_adminform_shows_default_save_button(superuser):
    url = reverse("admin:django_boosted_boostedview_global_action_view")

    response = _client(superuser).get(url)

    assert response.status_code == 200
    assert 'name="_save"' in response.content.decode()


@pytest.mark.django_db()
def test_global_adminform_can_rename_save_button(superuser):
    url = reverse("admin:django_boosted_boostedview_global_renamed_view")

    response = _client(superuser).get(url)

    assert response.status_code == 200
    assert 'value="Run it"' in response.content.decode()


@pytest.mark.django_db()
def test_global_adminform_supports_multiple_colored_buttons(superuser):
    url = reverse("admin:django_boosted_boostedview_global_multi_view")

    response = _client(superuser).get(url)

    assert response.status_code == 200
    content = response.content.decode()
    assert 'name="_apply"' in content
    assert 'class="success"' in content
    assert 'name="_danger"' in content
    assert 'class="danger"' in content


@pytest.mark.django_db()
def test_global_adminform_all_button_colors(superuser):
    url = reverse("admin:django_boosted_boostedview_global_colors_view")

    response = _client(superuser).get(url)

    assert response.status_code == 200
    content = response.content.decode()
    colors = ("default", "success", "info", "warning", "danger", "primary", "secondary")
    for color in colors:
        assert f'class="{color}"' in content


@pytest.mark.django_db()
def test_global_adminform_view_post_redirects(superuser):
    country = Country.objects.create(name="France")
    url = reverse("admin:django_boosted_boostedview_global_action_view")

    response = _client(superuser).post(
        url, {"user": superuser.pk, "country": country.pk}
    )

    assert response.status_code == 302
    assert response.url == reverse("admin:index")


@pytest.mark.django_db()
def test_global_list_view_renders(superuser):
    Country.objects.create(name="Zanzibar")
    url = reverse("admin:django_boosted_boostedview_global_countries_view")

    response = _client(superuser).get(url)

    assert response.status_code == 200
    assert "Zanzibar" in response.content.decode()


@pytest.mark.django_db()
def test_global_list_view_renders_boost_labels(superuser):
    Country.objects.create(name="Zanzibar")
    url = reverse("admin:django_boosted_boostedview_global_labels_view")

    response = _client(superuser).get(url)

    assert response.status_code == 200
    content = response.content.decode()
    assert 'class="boost-label success"' in content
    assert "boost-label danger small" in content


@pytest.mark.django_db()
def test_staff_user_can_access_global_view(staff_user):
    url = reverse("admin:django_boosted_boostedview_global_hello_view")

    response = _client(staff_user).get(url)

    assert response.status_code == 200
    assert "Hello from a global boosted view" in response.content.decode()


@pytest.mark.django_db()
def test_non_staff_cannot_access_global_view(plain_user):
    url = reverse("admin:django_boosted_boostedview_global_action_view")

    response = _client(plain_user).get(url)

    assert response.status_code in (302, 403)
