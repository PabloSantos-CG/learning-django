from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from utils.config_fields_form import ConfigFields


class RegisterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # dessa maneira não estou sobrescrevendo o widgets
        # self.fields['username'].widget.attrs['placeholder'] = 'novo valor'
        ConfigFields.add_placeholder(self.fields['username'], 'Seu username')
        ConfigFields.add_placeholder(self.fields['email'], 'Seu e-mail')
        ConfigFields.add_placeholder(self.fields['first_name'], 'Ex.: John')
        ConfigFields.add_placeholder(self.fields['last_name'], 'Ex.: Doe')
        ConfigFields.add_placeholder(
            self.fields['password'], 'Informe sua senha'
        )
        ConfigFields.add_placeholder(
            self.fields['password2'], 'Repita sua senha'
        )

    # ao fazer dessa maneira, estamos criando o campo ou sobrescrevendo se ele já existir
    password = forms.CharField(
        help_text=(
            'A senha deve ter pelo menos uma letra maiúscula, '
            'uma letra minúscula e um número.'
            'O comprimento deve ser de pelo menos 8 caracteres.'
        ),
        label='Senha:',
        widget=forms.PasswordInput(),
        validators=[ConfigFields.validate_password],
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(),
        label='Repita a senha:',
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']
        labels = {
            'first_name': 'Primeiro nome:',
            'last_name': 'Último sobrenome:',
            'username': 'Nome de Usuário:',
            'email': 'E-mail:',
        }
        widgets = {
            "first_name": forms.TextInput(attrs={"required": True}),
            "last_name": forms.TextInput(attrs={"required": True}),
            "username": forms.TextInput(attrs={"required": True}),
            "email": forms.EmailInput(attrs={"required": True}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email', '')
        user_exists = User.objects.filter(email=email).exists()

        if user_exists:
            raise ValidationError(
                'Já existe usuário cadastrado com este e-mail.',
                code='invalid'
            )
        return email

    def clean(self):
        cleaned_data = super().clean()

        first_password_input = cleaned_data.get('password')
        last_password_input = cleaned_data.get('password2')

        if first_password_input != last_password_input:
            raise ValidationError({
                'password': 'Os campos devem ser iguais',
                'password2': 'Os campos devem ser iguais',
            })

        first_name = cleaned_data.get('first_name', '').strip()
        last_name = cleaned_data.get('last_name', '').strip()

        if first_name == '' or last_name == '':
            raise ValidationError({
                'first_name': 'Este campo é obrigatório.',
                'last_name': 'Este campo é obrigatório.',
            })
