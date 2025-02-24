# from django.test import TestCase
from django.urls import resolve, reverse
from recipes import views
from .test_recipe_base import RecipeTestBase
# from recipes.models import Category, Recipe, User


# class RecipeTestBase(TestCase):
#     def setUp(self) -> None:
#         category = Category.objects.create(name='Category')
#         author = User.objects.create_user(
#             first_name='user',
#             last_name='name',
#             username='username',
#             password='123456',
#             email='username@email.com',
#         )
#         recipe = Recipe.objects.create(
#             category=category,
#             author=author,
#             title='Recipe Title',
#             description='Recipe Description',
#             slug='recipe-slug',
#             preparation_time=10,
#             preparation_time_unit='Minutos',
#             servings=5,
#             servings_unit='Porções',
#             preparation_steps='Recipe Preparation Steps',
#             preparation_steps_is_html=False,
#             is_published=True,
#         )
#         return super().setUp()


class RecipeViewsTest(RecipeTestBase):
    # def tearDown(self) -> None:
    #     return super().tearDown()

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

    def test_recipe_details_404(self):
        recipe_details = reverse('recipes:details', kwargs={'id': 9999})
        response = self.client.get(recipe_details)
        self.assertEqual(response.status_code, 404)

    def test_recipes_category_404(self):
        category = reverse('recipes:category', kwargs={'id': 9999})
        response = self.client.get(category)
        self.assertEqual(response.status_code, 404)
