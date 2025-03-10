from django.http import HttpRequest
from django.http.response import Http404
from django.shortcuts import render, get_list_or_404, get_object_or_404
from django.db.models import Q
from .models import Recipe
from utils.pagination import make_pagination

import os


PER_PAGE = int(os.environ.get('PER_PAGE', 6))


def home(request: HttpRequest):
    recipes = Recipe.objects.filter(
        is_published=True
    ).order_by("-id")

    paginator_obj, pagination_range = make_pagination(
        request, recipes, PER_PAGE)

    return render(
        request,
        'recipes/pages/home.html',
        context={
            'recipes': paginator_obj,
            'pagination_range': pagination_range
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

    paginator_obj, pagination_range = make_pagination(
        request, recipes, PER_PAGE)

    return render(
        request,
        'recipes/pages/category.html',
        context={
            'recipes': paginator_obj,
            'pagination_range': pagination_range,
            'title': category_title
        }
    )


def search(request: HttpRequest):
    query_str = request.GET.get('q', '').strip()

    if not query_str:
        raise Http404()

    recipes = Recipe.objects.filter(
        Q(
            Q(title__contains=query_str) |
            Q(description__contains=query_str)
        ),
        is_published=True
    ).order_by("-id")

    paginator_obj, pagination_range = make_pagination(
        request, recipes, PER_PAGE)

    return render(
        request,
        'recipes/pages/search.html',
        context={
            'title': f'Search for "{query_str}"',
            'recipes': paginator_obj,
            'pagination_range': pagination_range,
            'additional_url_query': f'&q={query_str}'
        }
    )
