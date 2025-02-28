from django.urls import resolve, reverse
from recipes import views
from .test_recipe_base import RecipeTestBase
from unittest.mock import patch


class RecipeViewsTest(RecipeTestBase):
    def test_recipes_view_home(self):
        view = resolve(reverse('recipes:home'))
        self.assertIs(view.func, views.home)

    def test_recipe_view_details(self):
        view = resolve(reverse('recipes:details', kwargs={'id': 1}))
        self.assertIs(view.func, views.recipe)

    def test_recipes_view_category(self):
        view = resolve(reverse('recipes:category', kwargs={'id': 1}))
        self.assertIs(view.func, views.category)

    def test_recipes_home_loads_template_correct(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertTemplateUsed(response, 'recipes/pages/home.html')

    def test_recipe_home_template_loads_recipes(self):
        self.make_recipe()

        response = self.client.get(reverse('recipes:home'))
        content = response.content.decode('utf-8')
        response_context_recipes = response.context['recipes']

        self.assertIn('Recipe Title', content)
        self.assertIn('10 Minutos', content)
        self.assertIn('5 Porções', content)
        self.assertEqual(len(response_context_recipes), 1)

    def test_does_not_upload_unpublished_recipes(self):
        recipe = self.make_recipe(is_published=False)

        response = self.client.get(
            reverse('recipes:details', kwargs={'id': recipe.pk})
        )

        self.assertEqual(response.status_code, 404)

    def test_recipe_details_404(self):
        recipe_details = reverse('recipes:details', kwargs={'id': 9999})
        response = self.client.get(recipe_details)
        self.assertEqual(response.status_code, 404)

    def test_recipes_category_404(self):
        category = reverse('recipes:category', kwargs={'id': 9999})
        response = self.client.get(category)
        self.assertEqual(response.status_code, 404)

    def test_recipes_view_search(self):
        response = resolve(reverse('recipes:search'))
        self.assertIs(response.func, views.search)

    def test_recipes_template_search(self):
        url = reverse('recipes:search')
        response = self.client.get(f'{url}?q=test')
        self.assertTemplateUsed(response, 'recipes/pages/search.html')

    def test_recipes_search_404_querystr_no_param(self):
        response = self.client.get(reverse('recipes:search'))
        self.assertEqual(response.status_code, 404)

    def test_recipes_search_find_correct(self):
        mock_recipe = self.make_recipe()

        url = reverse('recipes:search')
        response = self.client.get(f'{url}?q=Recipe')

        self.assertIn(mock_recipe, response.context['recipes'])

    def test_recipe_home_is_paginated(self):
        for i in range(8):
            kwargs = {
                'slug': f'slug-{i}',
                'author_data': {'username': f'user-{i}'}
            }
            self.make_recipe(**kwargs)

        with patch('recipes.views.PER_PAGE', new=3):
            response = self.client.get(reverse('recipes:home'))
            recipes = response.context['recipes']
            paginator = recipes.paginator

            self.assertEqual(paginator.num_pages, 3)
            self.assertEqual(len(paginator.get_page(1)), 3)
            self.assertEqual(len(paginator.get_page(2)), 3)
            self.assertEqual(len(paginator.get_page(3)), 2)
