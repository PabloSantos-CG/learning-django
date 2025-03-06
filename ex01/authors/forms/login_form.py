from django import forms

from utils.config_fields_form import ConfigFields


class LoginForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        ConfigFields.add_placeholder(self.fields['username'], 'John_doe')
        ConfigFields.add_placeholder(self.fields['password'], 'Senha****')

    username = forms.CharField(
        label='Informe seu nome de usuário:',
        widget=forms.TextInput(),
    )

    password = forms.CharField(
        label='Senha:',
        widget=forms.PasswordInput(),
    )
