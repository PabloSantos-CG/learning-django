from django.http import HttpRequest
from django.http.response import Http404
from django.shortcuts import render, get_list_or_404, get_object_or_404
from .models import Recipe
# from utils.recipes.factory import make_recipe


def home(request: HttpRequest):
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


def recipe(request: HttpRequest, id):
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


def category(request: HttpRequest, id):
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


def search(request: HttpRequest):
    query_str = request.GET.get('q')

    if query_str is None:
        raise Http404()

    return render(request, 'recipes/pages/search.html')
