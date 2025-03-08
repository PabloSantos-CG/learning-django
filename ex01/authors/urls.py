from django.urls import path
from . import views

app_name = "authors"

urlpatterns = [
    path('register/', views.register_view, name='register_view'),
    path('register/create/', views.register_create, name='register_create'),
    path('login/', views.login_view, name='login'),
    path('login/auth/', views.login_auth, name='auth'),
    path('logout/', views.logout_view, name='logout'),
]
