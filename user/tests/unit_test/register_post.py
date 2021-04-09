from django.test import TestCase, RequestFactory
from ...views import Register
from ...form import RegisterForm
from unittest import mock
from unittest.mock import patch, MagicMock
from django.urls import reverse

class TestRegisterView(TestCase):
    """
    Test class for AuthenticationView.
    """
    def setUp(self):
        self.factory = RequestFactory()

    def test_registerview_post(self):
        print("\nTEST - REGISTERVIEW --> def post()\n")
        with mock.patch('user.views.Register.RegisterForm.is_valid') as mocked_form:
            mocked_form.return_value = True
            request = self.factory.post(reverse('register'), data={})
            response = Register.as_view()(request)
            self.assertEqual(response.status_code, 200)