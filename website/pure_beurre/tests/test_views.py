from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.contrib.auth.models import User, AnonymousUser
from ..models import Category, Product, Substitute


class TestViews(TestCase):
    def setUp(self):
        cat = Category.objects.create(name="test_name")
        p = Product.objects.create(name="prod_name",
                                   nutriscore="a",
                                   brand="brand",
                                   url_opff="http://url.com",
                                   ingredients="ingredient_test",
                                   image="http://image.com",
                                   opff_id=123,
                                   category_id=cat.id)

        user = User.objects.create_user(username="user_test",
                                        email="test@email.fr",
                                        password="passtest")
        Substitute.objects.create(user=user,
                                  product=p)

        self.user = User.objects.get(username='user_test')
        self.p = Product.objects.get(name="prod_name")

    def test_index_page_GET(self):
        response = self.client.get(reverse('index_view'))
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, "Colette et Remy")
        self.assertTemplateUsed(response, "pure_beurre/index.html")

    def test_research_results(self):
        products = Product.objects.get(name="prod_name")
        categories = Category.objects.get(name="test_name")
        food = categories.name
        response = self.client.get(reverse('results_view'), {'p': products,
                                                             'food': food})
        self.assertContains(response, "http://image.com")
        self.assertEquals(response.status_code, 200)

    def test_detail_page_GET(self):
        response = self.client.get(reverse("food_detail", args=[self.p.id]))
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, "ingredient_test")
        self.assertTemplateUsed("pure_beurre/food_detail.html")

    def test_legal_notice_GET(self):
        response = self.client.get(reverse('legal_view'))
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, "Heroku")
        self.assertTemplateUsed(response, "pure_beurre/legal_notice.html")


class TestViewAnonymousUser(TestCase):
    def setUp(self):
        self.user = AnonymousUser

    def test_save_substitute_anon_user_POST(self):
        response = self.client.post('/results/')
        self.assertEquals(response.status_code, 302)

    def test_my_products_anon_user_GET(self):
        response = self.client.get(reverse('my_products'))
        self.assertEquals(response.status_code, 302)


class TestViewLogUser(TestCase):
    def setUp(self):
        cat = Category.objects.create(name="test_name")
        Product.objects.create(name="prod_name",
                               nutriscore="a",
                               brand="brand",
                               url_opff="http://url.com",
                               ingredients="ingredient_test",
                               image="http://image.com",
                               opff_id=123,
                               category_id=cat.id)

        User.objects.create_user(username="user_test",
                                 email="test@email.fr",
                                 password="passtest")

        self.user = User.objects.get(username='user_test')
        self.p = Product.objects.get(name="prod_name")

    def test_save_substitute_user_login_POST(self):
        self.client.login(username='user_test', password='passtest')
        response = self.client.post('/results/', {"food_id": self.p.id})
        sub = Product.objects.all().filter(substitute__user=self.user)
        self.assertEquals(response.status_code, 302)
        self.assertEquals(len(sub), 1)

    def test_my_products_GET(self):
        Substitute.objects.create(user=self.user,
                                  product=self.p)
        self.client.login(username='user_test', password='passtest')
        products = Product.objects.all().filter(substitute__user=self.user)
        response = self.client.get(reverse('my_products'), {'products': products})
        self.assertContains(response, "http://image.com")
        self.assertEquals(response.status_code, 200)

    def test_save_substitute_already_ex_POST(self):

        Substitute.objects.create(user=self.user,
                                  product=self.p)

        self.client.login(username='user_test', password='passtest')
        response = self.client.post('/results/', {"food_id": self.p.id})
        sub = Product.objects.all().filter(substitute__user=self.user)
        self.assertEquals(response.status_code, 302)
        self.assertEquals(len(sub), 1)

