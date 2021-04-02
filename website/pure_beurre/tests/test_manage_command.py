from django.test import TestCase
from unittest import mock
from unittest.mock import patch
from ..management.commands.fill_db import Command
from ..models import Category, Product

DATA_CATEGORY = {'tags':
                     {0:
                          {'name': 'Snacks', 'products': 53871, 'known': 1, 'id': 'en:snacks',
                           'url': 'https://fr.openfoodfacts.org/categorie/snacks'}
                      }}
DATA_PRODUCT = {"products":
                    {0:
                         {"product_name": "Milk chocolate",
                          "url": "https://fr.openfoodfacts.org/produit/25387643/milk-chocolate-dairyfine",
                          "nutrition_grades": "e",
                          "selected_images":
                              {'front':
                                   {'small':
                                        {'fr':
                                             "https://static.openfoodfacts.org/images/products/25387643/front_fr.4.200.jpg"}}},
                          'brands_tags': {0: "dairyfine"},
                          "opff_id ": 25387643,
                          'ingredients_text_fr': "chocolate:90%"}}}


class MockResponseCat:
    def json(self):
        """
        Return json expected values
        """
        return DATA_CATEGORY


class MockResponseProd:
    def json(self):
        """
        Return json expected values
        """
        return DATA_PRODUCT


class TestMangement(TestCase):
    def setUp(self):
        self.params = {"name": "name",
                       "username": "username",
                       "password": "password"}

        self.url = "https://fr.openfoodfacts.org/categories.json"
        self.url_product = "%s/%s.json" % (
            "https://fr.openfoodfacts.org/categorie/snacks", 1)

    def test_insert_category(self):
        with patch('pure_beurre.management.commands.fill_db.requests.get') as mock_requests:
            command = Command()
            mock_requests.return_values = MockResponseCat(), MockResponseProd()

            command.handle(num_category=1, num_product=1)
            mock_requests.side_effect = mock_requests.return_values

            cat = Category.objects.all()
            category = Category.objects.get(name="Snacks")

            self.assertEquals(len(cat), 1)
            self.assertEquals(category.name, "Snacks")

            prod = Product.objects.all()
            self.assertEquals(len(prod), 1)
