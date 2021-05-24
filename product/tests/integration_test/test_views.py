from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from product.models import Category, Product, Substitute


class TestViews(TestCase):
    def setUp(self):
        cat = Category.objects.create(name="test_name")
        cat_two = Category.objects.create(name="test_name")

        p = Product.objects.create(name="pomme",
                                   nutriscore="a",
                                   brand="brand",
                                   url_opff="http://url.com",
                                   ingredients="ingredient_test",
                                   image="http://image.com",
                                   opff_id=123,
                                   category_id=cat.id)

        p_two = Product.objects.create(name="poire",
                                   nutriscore="b",
                                   brand="brand",
                                   url_opff="http://url_2.com",
                                   ingredients="ingredient_test",
                                   image="http://image_2.com",
                                   opff_id=1234,
                                   category_id=cat.id)
        p_three = Product.objects.create(name="nutella",
                                   nutriscore="d",
                                   brand="brand",
                                   url_opff="http://url_3.com",
                                   ingredients="ingredient_test",
                                   image="http://image_3.com",
                                   opff_id=12345,
                                   category_id=cat_two.id)

        user = User.objects.create_user(username="user_test",
                                        email="test@email.fr",
                                        password="passtest")

        Substitute.objects.create(user=user,
                                  product=p)

        self.user = User.objects.get(username='user_test')
        self.p = Product.objects.get(name="pomme")

    def test_index_page_GET(self):
        """
        Check the index page.
        Check if the template is correct, if it contains the expected data and the status code
        """
        response = self.client.get(reverse('index_view'))
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, "Colette et Remy")
        self.assertTemplateUsed(response, "product/inex.html")

    def test_research_results(self):
        """
        Check the results page.
        Check if the template is correct, if it contains the expected data and the status code
        """
        products = Product.objects.get(name="poire")
        categories = products.category
        food = products.name
        response = self.client.get(reverse('results_view'), {'p': products,
                                                             'food': food,
                                                             "c": categories})
        self.assertContains(response, "http://image.com")
        self.assertEquals(response.status_code, 200)

    def test_detail_page_GET(self):
        """
        Check the index page.
        Check if the template is correct, if it contains the expected data and the status code
        """
        response = self.client.get(reverse("food_detail", args=[self.p.id]))
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, "ingredient_test")
        self.assertTemplateUsed("product/food_detail.html")

    def test_legal_notice_GET(self):
        """
        Check the index page.
        Check if the template is correct, if it contains the expected data and the status code
        """
        response = self.client.get(reverse('legal_view'))
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, "Heroku")
        self.assertTemplateUsed(response, "product/legal_notice.html")


class TestViewAnonymousUser(TestCase):
    def test_save_substitute_anon_user_POST(self):
        """
        Check if the anonymous user can't save substitute.
        """
        response = self.client.post('/results/')
        self.assertEquals(response.status_code, 302)

    def test_my_products_anon_user_GET(self):
        """
        Check if the anonymous user can't get my_products page.
        """
        response = self.client.get(reverse('my_products'))
        self.assertEquals(response.status_code, 302)


class TestViewLogUser(TestCase):
    def setUp(self):
        cat = Category.objects.create(name="test_name")
        Product.objects.create(name="poire",
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
        self.p = Product.objects.get(name="poire")

    def test_save_substitute_POST(self):
        """
        Check if the logged in user can save substitute.
        Check page status code.
        Check if the substitute is created.
        """
        self.client.login(username='user_test', password='passtest')
        response = self.client.post('/results/', {"food_id": self.p.id})
        sub = Product.objects.all().filter(substitute__user=self.user)
        self.assertEquals(response.status_code, 302)
        self.assertEquals(len(sub), 1)

    def test_my_products_GET(self):
        """
        Check if the logged in user can get my_products page.
        Check if page contains the expected data and the status code.
        """
        Substitute.objects.create(user=self.user,
                                  product=self.p)
        self.client.login(username='user_test', password='passtest')
        products = Product.objects.all().filter(substitute__user=self.user)
        response = self.client.get(reverse('my_products'), {'products': products})
        self.assertContains(response, "http://image.com")
        self.assertEquals(response.status_code, 200)

    def test_save_substitute_already_ex_POST(self):
        """
        Check if substitute already saved. The same substitute is not created.
        """
        Substitute.objects.create(user=self.user,
                                  product=self.p)

        self.client.login(username='user_test', password='passtest')
        response = self.client.post('/results/', {"food_id": self.p.id})
        sub = Product.objects.all().filter(substitute__user=self.user)
        self.assertEquals(response.status_code, 302)
        self.assertEquals(len(sub), 1)


