from django.http import Http404, HttpRequest
from django.shortcuts import redirect, render
from .forms import RegisterForm


def register(request: HttpRequest):
    form = RegisterForm(request.session.get('register_form_data'))

    return render(request, 'authors/pages/register.html', {'form': form})

def create(request: HttpRequest):
    if not request.POST:
        raise Http404()

    POST = request.POST
    request.session['register_form_data'] = POST
    form = RegisterForm(POST)
    
    return redirect('authors:register')