from django.test import TestCase
from ..form import AskFoodform
from ..models import Category, Product


class TestForms(TestCase):
    def setUp(self):
        self.cat = Category.objects.create(name="test_cat")
        self.prod = Product.objects.create(name="prod_name",
                                           nutriscore="a",
                                           brand="brand",
                                           url_opff="http://url.com",
                                           ingredients="ingredient_test",
                                           image="http://image.com",
                                           opff_id=123,
                                           category_id=self.cat.id)

    def test_form_by_category_is_valid(self):
        form = AskFoodform(data={
            "food": "test_cat"
        })
        self.assertTrue(form.is_valid())

    def test_form_by_product_is_valid(self):
        form = AskFoodform(data={
            "food": "prod_name"
        })
        self.assertTrue(form.is_valid())

    def test_form_empty(self):
        form = AskFoodform(data={
            "food": ""
        })
        self.assertFalse(form.is_valid())

    def test_product_not_exist(self):
        form = AskFoodform(data={
            "food": "food_3"
        })
        self.assertTrue(form.is_valid())
