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
        button_form = self.browser.find_element_by_id('submit')

        username.send_keys("username_test")
        passwd.send_keys("pass_test")

        button_form.click()

        url = self.live_server_url + reverse("dashboard_view", args=["username_test"])
        self.assertEquals(self.browser.current_url, url)

        time.sleep(5)