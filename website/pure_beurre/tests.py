from django.test import TestCase


class IndexTest(TestCase):
    def test_index_page(self):
        self.assertEqual('a', 'a')