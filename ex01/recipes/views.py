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
    try:
        data_recipe = Recipe.objects.get(id=id)

        return render(
            request,
            'recipes/pages/recipe.html',
            context={
                'recipe': data_recipe,
                'is_page_details': True,
                'title': data_recipe.title
            }
        )
    except:
        return render(request, 'recipes/pages/error.html', status=404)


def category(request, id):
    recipes = Recipe.objects.filter(
        category__id=id
    ).order_by("-id")

    if not recipes:
        return render(request, 'recipes/pages/error.html', status=404)

    first_recipe = recipes.first()
    if first_recipe and first_recipe.category:
        category_name = first_recipe.category.name 
    else:
        "Categoria não encontrada"

    return render(
        request,
        'recipes/pages/category.html',
        context={
            'recipes': recipes,
            'title': category_name
        }
    )
