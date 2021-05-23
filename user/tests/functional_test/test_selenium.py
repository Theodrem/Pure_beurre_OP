import time
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from selenium import webdriver
from django.urls import reverse
from django.core import mail
from django.contrib.auth.models import User


class MySeleniumTests(StaticLiveServerTestCase):
    def setUp(self):

        self.user = User.objects.create_user(username="username_test",
                                             email="email@outlook.fr",
                                             password="pass_test")

        self.browser = webdriver.Edge(executable_path="C:\exec\msedgedriver.exe")

    def test_login_user(self):
        self.browser.get(self.live_server_url + "/login/")

        username = self.browser.find_element_by_xpath('//*[@id="id_username"]')
        passwd = self.browser.find_element_by_xpath('//*[@id="id_password"]')
        button_form = self.browser.find_element_by_xpath('//*[@id="submit"]')

        username.send_keys("username_test")
        passwd.send_keys("pass_test")

        self.browser.execute_script("arguments[0].click();", button_form)

        url = self.live_server_url + reverse("dashboard_view")
        self.assertEquals(self.browser.current_url, url)

        time.sleep(5)

    def test_register_user(self):
        self.browser.get(self.live_server_url + "/register/")

        username = self.browser.find_element_by_xpath('//*[@id="id_username"]')
        email = self.browser.find_element_by_xpath('//*[@id="id_email"]')
        passwd = self.browser.find_element_by_xpath('//*[@id="id_password"]')
        repasswd = self.browser.find_element_by_xpath('//*[@id="id_repassword"]')
        button_form = self.browser.find_element_by_xpath('//*[@id="submit"]')

        username.send_keys("new_username")
        email.send_keys("email@hotmail.fr")
        passwd.send_keys("test_pass_word12")
        repasswd.send_keys("test_pass_word12")
        self.browser.execute_script("arguments[0].click();", button_form)

        url = self.live_server_url + reverse("dashboard_view")
        user = User.objects.get(username="new_username")
        all_users = User.objects.all()

        self.assertEquals(self.browser.current_url, url)
        self.assertEquals(user.username, "new_username")
        self.assertEquals(len(all_users), 2)

        time.sleep(5)

    def test_reset_password(self):
        mail.send_mail(
            'Réinitialisation du mot de passe sur pure-beurre-th.herokuapp.com',
            'Vous recevez ce message en réponse à votre demande de réinitialisation du mot de passe de votre compte '
            'sur pure-beurre-th.herokuapp.com.',
            'from@example.com', ["to_email@example.fr"],
            fail_silently=False,
        )

        self.browser.get(self.live_server_url + "/reset_password/")
        email = self.browser.find_element_by_xpath('//*[@id="id_email"]')
        button_form = self.browser.find_element_by_xpath('//*[@id="submit"]')

        email.send_keys("to_email@example.fr")
        self.browser.execute_script("arguments[0].click();", button_form)

        url = self.live_server_url + reverse("password_reset_done")

        self.assertEquals(self.browser.current_url, url)
        self.assertEqual(len(mail.outbox), 1)

        time.sleep(5)

    def test_password_reset_from_key(self):
        uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        token = default_token_generator.make_token(self.user)
        self.browser.get(f"{self.live_server_url}/reset/{uid}/{token}")

        self.browser.find_element_by_xpath('// *[ @ id = "id_new_password1"]').send_keys("pologne102")
        self.browser.find_element_by_xpath('//*[@id="id_new_password2"]').send_keys("pologne102")

        button_form = self.browser.find_element_by_xpath('//*[@id="submit"]')
        self.browser.execute_script("arguments[0].click();", button_form)

        time.sleep(5)







