import time
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from django.urls import reverse
from product.models import Product, Category
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

        self.browser = webdriver.Edge(executable_path="C:\exec\msedgedriver.exe")

    def tearDown(self):
        self.browser.close()

    def test_research(self):
        self.client.login(username='username_test', password='pass_test')
        self.browser.get(self.live_server_url)
        # find the elements you need to submit form
        url = self.live_server_url + reverse("results_view") + '?food=fruit'
        index_form = self.browser.find_element_by_xpath('//*[@id="id_food"]')
        button_form = self.browser.find_element_by_id('submit')
        index_form.send_keys("fruit")
        button_form.click()
        self.assertEquals(self.browser.current_url, url)

        time.sleep(3)


        #add register

        #add save

        #plan de test

        #generer test

        #nettoyer repo








