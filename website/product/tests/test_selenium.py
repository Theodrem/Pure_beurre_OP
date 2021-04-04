import time
import pytest
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from ..models import Product, Category
from django.contrib.auth.models import User


class MySeleniumTests(StaticLiveServerTestCase):
    def setUp(self):
        self.cat = Category.objects.create(name="fruit")
        self.prod = Product.objects.create(name="Poire",
                                           nutriscore="b",
                                           brand="brand",
                                           url_opff="https/opff/test.com",
                                           ingredients="ingredients",
                                           image="https/image/test.com",
                                           opff_id=1234,
                                           category=self.cat)

        self.prod_two = Product.objects.create(name="Pomme",
                                               nutriscore="a",
                                               brand="brand",
                                               url_opff="https/opff/test.com",
                                               ingredients="ingredients du deuxieme produit",
                                               image="https/image/test.com",
                                               opff_id=12554,
                                               category=self.cat)

        self.user = User.objects.create_user(username="username_test",
                                             email="email@outlook.fr",
                                             password="pass_test")

        self.browser = webdriver.Chrome(ChromeDriverManager().install())

    def tearDown(self):
        self.browser.close()

    def test_no_project_errors(self):
        a = self.browser.get(self.live_server_url)
        self.assertEquals(a, "http://127.0.0.1:8000/")



