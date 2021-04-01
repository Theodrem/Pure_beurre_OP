from django.test import TestCase
from django.contrib.auth.models import User
from ..models import Category, Substitute, Product


class TestModel(TestCase):
    def setUp(self):
        self.cat = Category.objects.create(name="name_cat")

        self.prod = Product.objects.create(name="name_prod",
                                           nutriscore="b",
                                           brand="brand",
                                           url_opff="https/opff/test.com",
                                           ingredients="ingredients",
                                           image="https/image/test.com",
                                           opff_id=1234)

        self.user = User.objects.create_user(username="username",
                                             email="email@outlook.fr",
                                             password="password")

        self.sub = Substitute.objects.create(user=self.user,
                                             product=self.prod)

    def test_model_category(self):
        self.assertEquals(self.cat.name, "name_cat")
        self.assertIsInstance(self.cat, Category)

    def test_model_product(self):
        self.assertEquals(self.prod.nutriscore, "b")
        self.assertIsInstance(self.prod, Product)

    def test_model_substitute(self):
        p = Product.objects.get(substitute__user=self.user, substitute__product=self.prod)
        self.assertEquals(p.name, "name_prod")
        self.assertIsInstance(self.sub, Substitute)
