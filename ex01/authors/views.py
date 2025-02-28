from django.http import HttpRequest
from django.shortcuts import render
from .forms import RegisterForm


def register(request: HttpRequest):
    form = RegisterForm()

    return render(request, 'authors/pages/home.html', {'form': form})
