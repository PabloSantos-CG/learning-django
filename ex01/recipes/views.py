from django.shortcuts import render, get_list_or_404, get_object_or_404
from recipes.models import Recipe
# from utils.recipes.factory import make_recipe


def home(request):
    recipes = Recipe.objects.filter(
        is_published=True
    ).order_by("-id")

    return render(
        request,
        'recipes/pages/home.html',
        context={
            'recipes': recipes
        }
    )


def recipe(request, id):
    recipe_details = get_object_or_404(Recipe, pk=id, is_published=True)

    return render(
        request,
        'recipes/pages/recipe.html',
        context={
            'recipe': recipe_details,
            'is_page_details': True,
            'title': recipe_details.title
        }
    )


def category(request, id):
    recipes = get_list_or_404(
        Recipe.objects.filter(
            category__id=id
        ).order_by("-id")
    )

    category_title = "Categoria não encontrada"
    if recipes[0].category is not None:
        category_title = recipes[0].category.name

    return render(
        request,
        'recipes/pages/category.html',
        context={
            'recipes': recipes,
            'title': category_title
        }
    )
