import time
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from django.urls import reverse
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
        passwd.send_keys("password")
        repasswd.send_keys("password")
        self.browser.execute_script("arguments[0].click();", button_form)

        url = self.live_server_url + reverse("dashboard_view")
        user = User.objects.get(username="new_username")
        all_users = User.objects.all()

        self.assertEquals(self.browser.current_url, url)
        self.assertEquals(user.username, "new_username")
        self.assertEquals(len(all_users), 2)

        time.sleep(5)