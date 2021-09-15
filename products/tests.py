import pytest

from django.urls import reverse

from products.models.cart import Cart


@pytest.fixture
def test_password():
    return 'strong-new-password'


@pytest.fixture
def create_user(db, django_user_model, test_password):
    def make_user(**kwargs):
        kwargs['password'] = test_password
        if 'username' not in kwargs:
            kwargs['username'] = 'test_username'
        user = django_user_model.objects.create_user(**kwargs)
        return user

    return make_user


@pytest.fixture
def auto_login_user(db, client, create_user, test_password):
    def make_auto_login(user=None):
        if user is None:
            user = create_user()
        client.login(username=user.username, password=test_password)
        return client, user

    return make_auto_login


# Auto-creates user and logs in,
# checks 2 views with login_required
@pytest.mark.django_db
@pytest.mark.parametrize('view', [
    'products:cart', 'products:index'
])
def test_auth_view(auto_login_user, view):
    client, user = auto_login_user()
    url = reverse(view)
    response = client.get(url)
    assert response.status_code == 200
