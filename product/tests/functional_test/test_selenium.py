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

        self.browser = webdriver.Chrome(executable_path="C:\exec\chromedriver.exe")

    def tearDown(self):
        self.browser.close()

    def test_research(self):
        self.browser.get(self.live_server_url)
        # find the elements you need to submit form
        url = self.live_server_url + reverse("results_view") + '?food=fruit'

        index_form = self.browser.find_element_by_xpath('/html/body/div/header/div/div/div[2]/form/input')
        button_form = self.browser.find_element_by_id('submit')

        index_form.send_keys("fruit")
        button_form.click()

        cat = Category.objects.get(name="fruit")
        prods = Product.objects.all().filter(category=cat)

        for p in prods:
            self.assertTrue(p.name in self.browser.page_source)
        self.assertEquals(self.browser.current_url, url)

        time.sleep(5)

    def test_save_substitute(self):
        self.browser.get(self.live_server_url + "/login/")

        username = self.browser.find_element_by_xpath('//*[@id="id_username"]')
        passwd = self.browser.find_element_by_xpath('//*[@id="id_password"]')
        button_form = self.browser.find_element_by_xpath('//*[@id="submit"]')

        username.send_keys("username_test")
        passwd.send_keys("pass_test")

        self.browser.execute_script("arguments[0].click();", button_form)

        form = self.browser.find_element_by_xpath('//*[@id="logo"]')
        self.browser.execute_script("arguments[0].click();", form)



        index_form = self.browser.find_element_by_xpath('/html/body/div/header/div/div/div[2]/form/input')
        button_form_index = self.browser.find_element_by_id('submit')

        index_form.send_keys("fruit")
        button_form_index.click()

        save = self.browser.find_element_by_xpath('/ html / body / div[2] / div[2] / div[1] / div / div[2] / form / button')
        self.browser.execute_script("arguments[0].click();", save)

        url = self.live_server_url + reverse("my_products")
        subs = Product.objects.all().filter(substitute__user=self.user).order_by("nutriscore")

        self.assertEquals(self.browser.current_url, url)
        self.assertEquals(len(subs), 1)
        for sub in subs:
            self.assertTrue(sub.name in self.browser.page_source)
        self.assertEquals(self.browser.current_url, url)

        time.sleep(10)
