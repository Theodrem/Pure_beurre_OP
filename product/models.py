# coding=utf8
from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(verbose_name='Nom de la categorie', max_length=100)


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=300, null=True)
    nutriscore = models.CharField(verbose_name='Nutriscore', max_length=1, null=True)
    brand = models.CharField(verbose_name="Marque", max_length=300, null=True)
    url_opff = models.URLField(verbose_name='Lien Openfoodfact', max_length=300, null=True)
    ingredients = models.TextField(verbose_name='Ingredients du produit', null=True)
    image = models.URLField(max_length=300, null=True)
    opff_id = models.BigIntegerField(null=True)


class Substitute(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


