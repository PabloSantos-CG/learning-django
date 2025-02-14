from django.shortcuts import render
from recipes.models import Recipe
# from utils.recipes.factory import make_recipe


def home(request):
    recipes = Recipe.objects.all().order_by("-id")

    return render(
        request,
        'recipes/pages/home.html',
        context={
            'recipes': recipes
        }
    )
# mock
    # return render(
    #     request,
    #     'recipes/pages/home.html',
    #     context={
    #         'recipes': [make_recipe() for _ in range(9)]
    #     }
    # )


def recipe(request, id):
    data_recipe = Recipe.objects.get(id=id)

    return render(
        request,
        'recipes/pages/recipe.html',
        context={
            'recipe': data_recipe,
            'is_page_details': True
        }
    )


def category(request, id):
    recipes = Recipe.objects.filter(
        category__id=id
    ).order_by("-id")

    return render(
        request,
        'recipes/pages/home.html',
        context={
            'recipes': recipes
        }
    )
