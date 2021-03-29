from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Category, Product, Substitute


class IndexPageTestCase(TestCase):
    def setUp(self):
        cat = Category.objects.create(name="name")
        product = Product.objects.create(name="name",
                                         nutriscore="a",
                                         brand="brand",
                                         url_opff="http://url.com",
                                         ingredients="ingredient",
                                         image="http://image.com",
                                         opff_id=123,
                                         category_id=cat.id)

        self.product = Product.objects.get(name="name")

    def test_index_page(self):
        response = self.client.get(reverse('index_view'))
        self.assertEqual(response.status_code, 200)

    def test_send_data(self):
        form = {"food": "food"}
        response = self.client.get(reverse('results_view'), form)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "name")


class DetailProductPageTestCase(TestCase):
    def setUp(self):
        cat = Category.objects.create(name="name")
        product = Product.objects.create(name="name",
                                         nutriscore="a",
                                         brand="brand",
                                         url_opff="http://url.com",
                                         ingredients="ingredient",
                                         image="http://image.com",
                                         opff_id=123,
                                         category_id=cat.id)

        self.product = Product.objects.get(name="name")

    def test_detail_page_returns_200(self):
        product_id = self.product.id
        response = self.client.get(reverse("food_detail", args=[product_id]))
        self.assertEqual(response.status_code, 200)

    def test_detail_page_returns_404(self):
        product_id = self.product.id + 1
        response = self.client.get(reverse("food_detail", args=[product_id]))
        self.assertEqual(response.status_code, 404)


class ResultsTestPage(TestCase):
    def setUp(self):
        cat = Category.objects.create(name="name")
        product = Product.objects.create(name="name",
                                         nutriscore="a",
                                         brand="brand",
                                         url_opff="http://url.com",
                                         ingredients="ingredient",
                                         image="http://image.com",
                                         opff_id=123,
                                         category_id=cat.id)

        user = User.objects.create_user(username="username",
                                        email="user@live.fr",
                                        password="password")

        self.category = Category.objects.get(name="name")
        self.product = Product.objects.get(name="name")
        self.user = User.objects.get(username="username")

    def test_found_category(self):
        product = ""
        category = self.category
        food = "food"
        list_product = Product.objects.all().filter(category=category).order_by("nutriscore")

        response = self.client.get(reverse('results_view'),
                                   {"products": list_product,
                                    "c": category,
                                    "p": product,
                                    "food": food})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(list_product), 1)

    def test_found_product(self):
        product = self.product
        category = product.id
        food = "food"
        list_product = Product.objects.all().filter(category=category, nutriscore__lte=product.nutriscore).order_by("nutriscore")
        response = self.client.get(reverse('results_view'),
                                   {"products": list_product,
                                    "c": category,
                                    "p": product,
                                    "food": food})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(list_product), 1)

    def test_results_no_found_product(self):
        product = ""
        category = ""
        food = "food"

        list_product = Product.objects.all().order_by("nutriscore")

        response = self.client.get(reverse('results_view'),
                                   {"products": list_product,
                                    "c": category,
                                    "p": product,
                                    "food": food})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(list_product), 1)

    def test_save_substitute(self):
        data = {"food_id": self.product.id}
        p = Product(id=data['food_id'])

        sub = Substitute(product=p,
                         user=self.user)
        sub.save()
        substitute = Substitute.objects.get(product=p)

        self.assertEqual(substitute.user, self.user)


class MyProductsTest(TestCase):
    def setUp(self):
        cat = Category.objects.create(name="name")
        product = Product.objects.create(name="name",
                                         nutriscore="a",
                                         brand="brand",
                                         url_opff="http://url.com",
                                         ingredients="ingredient",
                                         image="http://image.com",
                                         opff_id=123,
                                         category_id=cat.id)

        user = User.objects.create_user(username="username",
                                        email="user@live.fr",
                                        password="password")

        self.category = Category.objects.get(name="name")
        self.product = Product.objects.get(name="name")
        self.user = User.objects.get(username="username")

        sub = Substitute(product=self.product,
                         user=self.user)
        sub.save()
        self.substitute = Substitute.objects.get(product=self.product)

    def test_my_product_page(self):
        self.client.login(username='username',
                               password='password')
        list_product = Product.objects.all().filter(substitute__user=self.user)
        response = self.client.get(reverse('my_products'),
                                   {"products": list_product})

        self.assertEqual(len(list_product), 1)
        self.assertEqual(response.status_code, 200)








