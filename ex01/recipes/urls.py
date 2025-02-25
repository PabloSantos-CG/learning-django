from django.urls import path
from . import views

app_name = "recipes"

urlpatterns = [
   path('', views.home, name='home'),
   path('recipes/search/', views.search, name='search'),
   path('recipe/<int:id>/', views.recipe, name='details'),
   path('recipes/category/<int:id>/', views.category, name='category'),
]
