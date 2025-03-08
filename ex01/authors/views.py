from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .forms import LoginForm, RegisterForm


def register_view(request: HttpRequest):
    form = RegisterForm(request.session.get('register_form_data'))

    return render(
        request,
        'authors/pages/register.html',
        {
            'form': form,
            'form_action': reverse('authors:register_create')
        }
    )


def register_create(request: HttpRequest):
    if not request.POST:
        raise Http404()

    POST = request.POST
    request.session['register_form_data'] = POST
    form = RegisterForm(POST)

    if form.is_valid():
        user = form.save(commit=False)

        user.set_password(form.cleaned_data['password'])
        user.save()

        messages.success(request, 'Usuário criado com sucesso. Faça o Login.')

        del request.session['register_form_data']

    return redirect('authors:login')


def login_view(request: HttpRequest):
    form = LoginForm()
    return render(
        request,
        'authors/pages/login.html',
        {
            'form': form,
            'form_action': reverse('authors:auth')
        }
    )


def login_auth(request: HttpRequest):
    if not request.POST:
        raise Http404()

    form = LoginForm(request.POST)

    if not form.is_valid():
        messages.error(request, 'Nome de usuário ou senha inválido(a).')
        return redirect('authors:login')

    authenticate_user = authenticate(
        username=form.cleaned_data.get('username', ''),
        password=form.cleaned_data.get('password', ''),
    )
    
    if not authenticate_user:
        messages.error(request, 'Usuário inexistente.')
        return redirect('authors:login')

    login(request, authenticate_user)
    messages.success(request, 'Login feito com sucesso!')
    return redirect('authors:login')

@login_required(login_url='authors:login')
def logout_view(request: HttpRequest):
    if not request.POST:
        raise Http404()
    
    logout(request)
    return redirect(reverse('authors:login'))