from django.http import HttpRequest
from django.shortcuts import render

# Create your views here.
def register(request: HttpRequest):
    return render(request, 'authors/pages/home.html')