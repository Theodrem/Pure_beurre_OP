# coding=utf8
import requests

from .models import Category, Product
from .config import LIST_CATEGORIES

"""
API connection data
"""
post_data = {"name": "Theotim", "username": "theodrem", "password": "Intelligence97"}
responses = requests.get("https://fr.openfoodfacts.org/categories.json", data=post_data)
current = responses.json()


def convert_data(data):
    list_character = {
        'à': 'a',
        'é': 'e',
        'è': 'e',
        'ê': 'e',
        'â': 'a'
    }
    a = data
    for i in data:
        if i in list_character.keys():
            a = data.replace(i, list_character[i])
    return a


def insert_data_from_openfoodfacts():
    """
    Get the first fifteen categories and add them to our database
    """
    for category in range(200):
        name_category = current["tags"][category]["name"]
        if name_category in LIST_CATEGORIES:
            try:
                c = Category.objects.get(name=name_category)
            except Category.DoesNotExist:
                c = Category(name=name_category.lower())
                c.save()

        for page in range(40):
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
                        p = Product(name=name.lower(),
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
