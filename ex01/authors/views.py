from django.http import HttpRequest
from django.shortcuts import render
from .forms import RegisterForm


def register(request: HttpRequest):
    if request.POST:
        form = RegisterForm(request.POST)
    else:
        form = RegisterForm()

    return render(request, 'authors/pages/home.html', {'form': form})
