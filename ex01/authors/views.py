from django.http import Http404, HttpRequest
from django.shortcuts import redirect, render
from django.urls import reverse
from .forms import RegisterForm
from django.contrib import messages


def register(request: HttpRequest):
    form = RegisterForm(request.session.get('register_form_data'))

    return render(
        request,
        'authors/pages/register.html',
        {
            'form': form,
            'form_action': reverse('authors:create')
        }
    )


def create(request: HttpRequest):
    if not request.POST:
        raise Http404()

    POST = request.POST
    request.session['register_form_data'] = POST
    form = RegisterForm(POST)

    if form.is_valid():
        user = form.save(commit=False)
        user.set_password(user.password)
        user.save()

        messages.success(request, 'Usuário criado com sucesso. Faça o Login.')

        del request.session['register_form_data']

    return redirect('authors:register')
