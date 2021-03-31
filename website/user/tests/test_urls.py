from django.test import SimpleTestCase
from django.urls import reverse, resolve

from ..views import Login, Register, Logout, Dashboard


class TestUrls(SimpleTestCase):
    def test_login_url_is_resolves(self):
        url = reverse('login_view')
        self.assertEquals(resolve(url).func.view_class, Login)

    def test_register_url_is_resolves(self):
        url = reverse('register_view')
        self.assertEquals(resolve(url).func.view_class, Register)

    def test_detail_url_is_resolves(self):
        url = reverse('logout_view')
        self.assertEquals(resolve(url).func.view_class, Logout)

    def test_my_products_url_is_resolves(self):
        url = reverse('dashboard_view', args=["user_test"])
        self.assertEquals(resolve(url).func.view_class, Dashboard)
