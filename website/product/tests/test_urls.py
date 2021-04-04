from django.test import SimpleTestCase
from django.urls import reverse, resolve

from ..views import Index, Results, LegalNotice, MyProducts, DetailProduct


class TestUrls(SimpleTestCase):
    def test_index_url_is_resolves(self):
        url = reverse('index_view')
        self.assertEquals(resolve(url).func.view_class, Index)

    def test_results_url_is_resolves(self):
        url = reverse('results_view')
        self.assertEquals(resolve(url).func.view_class, Results)

    def test_detail_url_is_resolves(self):
        url = reverse('food_detail', args=[2])
        self.assertEquals(resolve(url).func.view_class, DetailProduct)

    def test_my_products_url_is_resolves(self):
        url = reverse('my_products')
        self.assertEquals(resolve(url).func.view_class, MyProducts)

    def test_legal_url_is_resolves(self):
        url = reverse('legal_view')
        self.assertEquals(resolve(url).func.view_class, LegalNotice)

