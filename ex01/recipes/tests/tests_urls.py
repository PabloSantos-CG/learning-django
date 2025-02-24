from django.test import TestCase
from django.urls import reverse


class RecipeURLsTest(TestCase):
    def test_recipes_home_url_is_correct(self):
        home_url = reverse('recipes:home')
        self.assertEqual(home_url, '/')

    def test_recipe_details_url_is_correct(self):
        details_url = reverse('recipes:details', kwargs={'id': 1})
        self.assertEqual(details_url, '/recipe/1/')

    def test_recipes_category_url_is_correct(self):
        category_url = reverse('recipes:category', kwargs={'id': 1})
        self.assertEqual(category_url, '/recipes/category/1/')
