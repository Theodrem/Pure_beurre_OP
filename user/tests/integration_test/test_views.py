from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User


class TestLogViews(TestCase):
    def setUp(self):
        User.objects.create_user(username="user_test",
                                 password="password",
                                 email="email@outlook.fr")
        self.user = User.objects.get(username="user_test")

    def test_dashboard_view_GET(self):
        """
        Check the dashboard page.
        Check if the current user can get dashboard page.
        Check if the template is correct, if it contains the expected data and the status code
        """
        self.client.login(username='user_test', password='password')
        response = self.client.get(reverse("dashboard_view"),
                                   {'username': self.user.username,
                                    'email': self.user.email})
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, "Salut user_test")
        self.assertTemplateUsed(response, "user/dashboard.html")

    def test_logout_GET(self):
        """
        Check the current user can logout.
        """
        self.client.login(username='user_test', password='password')
        response = self.client.get(reverse("logout_view"))
        self.assertEquals(response.status_code, 302)


class TestAnonymousViews(TestCase):
    def setUp(self):
        User.objects.create_user(username="user_test",
                                 password="password",
                                 email="email@outlook.fr")

    def test_dashboard_view_GET(self):
        """
        Check the current user can get the dashboard page.
        """
        response = self.client.get(reverse("dashboard_view"),
                                   {'username': "username",
                                    'email': " email"})
        self.assertEquals(response.status_code, 302)

    def test_login_view_GET(self):
        """
        Check login page.
        Check if the template is correct, if it contains the expected data and the status code
        """
        response = self.client.get(reverse("login_view"))
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, "utilisateur")

    def test_login_view_POST(self):
        """
        Check if the form is correct.
        form  if the form is cor
        """
        form = {"username": "user_test",
                "password": "password"}
        response = self.client.post(reverse("login_view"), form)
        self.assertEquals(response.status_code, 302)
        self.assertIn('_auth_user_id', self.client.session)

    def test_login_view_password_false(self):
        """
        Check if user to input false password. Do not connect user.
        """
        user = User.objects.get(username="user_test")
        form = {"username": "user_test",
                "password": "pass"}
        response = self.client.post(reverse("login_view"), form)
        self.assertEquals(response.status_code, 200)
        self.assertNotIn('_auth_user_id', self.client.session)

    def test_register_view_GET(self):
        """
        Check Register page.
        Check if the template is correct, if it contains the expected data and the status code
        """
        response = self.client.get(reverse("register_view"))
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, "Prenom")

    def test_register_view_POST(self):
        """
        Check if form is valid, create user then log in user.
        """
        form = {"username": "user_test",
                "first_name": "",
                "last_name": "",
                "email": "email@outlook.fr",
                "password": "password",
                "repassword": "password"}

        response = self.client.post(reverse("register_view"), form)
        self.assertEquals(response.status_code, 200)
        user = User.objects.get(username="user_test")
        self.assertIsInstance(user, User)




