import requests
from django.core.management.base import BaseCommand

from ...models import Category, Product
from ...config import LIST_CATEGORIES


class Command(BaseCommand):
    help = "Update bdd"

    def add_arguments(self, parser):
        parser.add_argument('num_category', type=int)
        parser.add_argument('num_product', type=int)

    def handle(self, *args, **options):
        post_data = {"name": "Theotim", "username": "theodrem", "password": "Intelligence97"}
        responses = requests.get("https://fr.openfoodfacts.org/categories.json", data=post_data)
        current = responses.json()
        num_category = options['num_category']
        num_product = options['num_product']
        """
        Get the first fifteen categories and add them to our database
        """

        for category in range(num_category):

            name_category = current["tags"][category]["name"]
            if name_category in LIST_CATEGORIES:
                try:
                    Category.objects.get(name=name_category)
                except Category.DoesNotExist:
                    c = Category(name=name_category)
                    c.save()

            for page in range(num_product):
                url_category = "%s/%s.json" % (current["tags"][category]["url"], page + 1)
                products = requests.get(url_category)
                result = products.json()

                try:
                    name = result["products"][page]["product_name"]
                    url = result["products"][page]["url"]
                    nutriscore = result["products"][page]["nutrition_grades"]
                    image = result["products"][page]["selected_images"]['front']['small']['fr']
                    ingredient = result["products"][page]['ingredients_text_fr']
                    brand = result["products"][page]['brands_tags'][0]
                    opff_id = result["products"][page]["id"]

                    if name != "" and url != "" and nutriscore != "" and image != "" and ingredient != "" and opff_id != "":
                        try:
                            cat = Category.objects.get(name=name_category)
                            try:
                                Product.objects.get(opff_id=opff_id)
                            except Product.DoesNotExist:
                                p = Product(name=name,
                                            nutriscore=nutriscore,
                                            brand=brand,
                                            url_opff=url,
                                            ingredients=ingredient,
                                            image=image,
                                            opff_id=opff_id,
                                            category_id=cat.id)
                                p.save()
                        except Category.DoesNotExist:
                            pass
                except IndexError:
                    pass
                except KeyError:
                    pass
