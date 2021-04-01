from django.test import TestCase
from django.contrib.auth.models import User
from ..form import LoginForm, RegisterForm


class TestForms(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="username_test",
                                             email="email@outlook.fr",
                                             password="pass_test")

    def test_login_form_is_valid(self):
        form = LoginForm(data={
            "username": "username_test",
            "password": "pass_test"
        })

        self.assertTrue(form.is_valid())

    def test_login_username_false(self):
        form = LoginForm(data={
            "username": "username",
            "password": "pass_test"
        })

        self.assertFalse(form.is_valid())

    def test_register_form_is_valid(self):
        form = RegisterForm(data={
            "username": "usernames",
            "first_name": "",
            "last_name": "",
            "email": "email@hotmail.fr",
            "password": "password",
            "repassword": "password"
        })
        self.assertTrue(form.is_valid())

    def test_register_username_exist(self):
        form = RegisterForm(data={
            "username": "username_test",
            "first_name": "",
            "last_name": "",
            "email": "email@hotmail.fr",
            "password": "password",
            "repassword": "password"
        })
        self.assertFalse(form.is_valid())

    def test_register_email_exist(self):
        form = RegisterForm(data={
            "username": "username",
            "first_name": "",
            "last_name": "",
            "email": "email@outlook.fr",
            "password": "password",
            "repassword": "password"
        })
        self.assertFalse(form.is_valid())

    def test_register_password_not_match(self):
        form = RegisterForm(data={
            "username": "username",
            "first_name": "",
            "last_name": "",
            "email": "email@hotmail.fr",
            "password": "password",
            "repassword": "pass"
        })
        self.assertFalse(form.is_valid())
