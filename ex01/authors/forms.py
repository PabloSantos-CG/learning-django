from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import re


class ConfigInputs:
    """Classe criada para configuração/personalização dos inputs do formulário."""

    @staticmethod
    def add_attr(field, attr_name, new_attr):
        """
        Este método adiciona ou modifica um atributo dentro do widget de um campo de formulário Django.

        🔹 **Contexto**: 
        - No Django, os widgets dos formulários podem ter atributos HTML personalizados (como `placeholder`, `class`, `id`).
        - Normalmente, para definir um atributo, fazemos: `field.widget.attrs['placeholder'] = 'Digite seu nome'`.
        - No entanto, se quisermos adicionar um valor a um atributo existente (sem sobrescrevê-lo), precisaríamos obter o valor atual e concatenar o novo valor.
        - Esse método automatiza esse processo.

        🔹 **Funcionamento**:
        - Ele primeiro verifica se o atributo já existe (`field.widget.attrs.get(attr_name, '')`).
        - Se existir, ele **concatena** o novo valor ao antigo.
        - Se não existir, ele simplesmente cria o atributo com o novo valor.

        🔹 **Parâmetros**:
        - `field` (*django.forms.Field*): Campo do formulário que receberá o atributo.
        - `attr_name` (*str*): Nome do atributo HTML (exemplo: `"class"`, `"placeholder"`).
        - `new_attr` (*str*): Novo valor a ser adicionado ao atributo.

        🔹 **Exemplo de uso**:
        ```python
        # Adiciona uma classe CSS personalizada ao campo 'username'
        ConfigInputs.add_attr(my_form.fields['username'], 'class', 'form-control')

        # Adiciona um placeholder ao campo 'email'
        ConfigInputs.add_attr(my_form.fields['email'], 'placeholder', 'Digite seu e-mail')
        ```

        🔹 **Resultado esperado**:
        Se o campo `username` já tiver `class="input-large"`, e chamarmos:
        ```python
        ConfigInputs.add_attr(my_form.fields['username'], 'class', 'form-control')
        ```
        O resultado será:
        ```html
        <input class="input-large form-control">
        ```
        Em vez de sobrescrever o atributo, ele mantém o valor antigo e adiciona o novo.
        """
        previous_attr = field.widget.attrs.get(attr_name, '')
        field.widget.attrs[attr_name] = f'{previous_attr} {new_attr}'.strip()

    @staticmethod
    def add_placeholder(field, new_value):
        ConfigInputs.add_attr(field, 'placeholder', new_value)

    @staticmethod
    def validate_password(password):
        regex = re.compile(
            r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[$*&@#])[A-Za-z\d$*&@#]{8,}$'
        )

        if not regex.match(password):
            raise ValidationError((
                'Mínimo de 8 caracteres: A senha deve ter pelo menos 8 caracteres.'
                'Pelo menos uma letra minúscula: Deve conter ao menos uma letra de "a" a "z".'
                'Pelo menos uma letra maiúscula: Deve conter ao menos uma letra de "A" a "Z".'
                'Pelo menos um dígito: Deve conter ao menos um número de "0" a "9".'
                'Pelo menos um caractere especial: Deve incluir ao menos um dos seguintes caracteres especiais:'
                '"$", "*", "&", "@", "#"'
            ),
                code='invalid',
            )


class RegisterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # dessa maneira não estou sobrescrevendo o widgets
        # self.fields['username'].widget.attrs['placeholder'] = 'novo valor'
        ConfigInputs.add_placeholder(self.fields['username'], 'Seu username')
        ConfigInputs.add_placeholder(self.fields['email'], 'Seu e-mail')
        ConfigInputs.add_placeholder(self.fields['first_name'], 'Ex.: John')
        ConfigInputs.add_placeholder(self.fields['last_name'], 'Ex.: Doe')
        ConfigInputs.add_placeholder(self.fields['password'], 'Informe sua senha')
        ConfigInputs.add_placeholder(self.fields['password2'], 'Repita sua senha')

    # ao fazer dessa maneira, estamos criando o campo ou sobrescrevendo se ele já existir
    password = forms.CharField( 
        required=True,
        error_messages={
            'required': 'A senha não deve estar vazia'
        },
        help_text=(
            'A senha deve ter pelo menos uma letra maiúscula, '
            'uma letra minúscula e um número.'
            'O comprimento deve ser de pelo menos 8 caracteres.'
        ),
        widget= forms.PasswordInput(),
        validators=[ConfigInputs.validate_password]
    )
    password2 = forms.CharField(
        required=True,
        widget= forms.PasswordInput(),
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password']
        labels = {
            'first_name': 'First name:',
            'last_name': 'Último sobrenome:',
            'username': 'Nome de Usuário:',
            'email': 'E-mail:',
            'password': 'Senha:',
        }
        # help_texts = {
        #     'username': 'O nome de usuário deveria ser válido',
        # }
        # error_messages = {
        #     'username': {
        #         'required': 'Campo obrigatório.',
        #     },
        #     'password': {
        #         'max_length': 'Tamanho insuficiente.',
        #     }
        # }

        # widgets = {
        #     'username': forms.TextInput(attrs={
        #         'placeholder': 'Informe o nome do usuário'
        #     }),
        #     'password': forms.PasswordInput(attrs={
        #         'placeholder': 'Informe sua senha aqui'
        #     })
        # }
    # def clean_username(self):
    #     data = self.cleaned_data.get('username')

    #     if data is not None and 'fulano' in data:
    #         raise ValidationError(
    #             'Não digite %(value)s no campo first name',
    #             code='invalid',
    #             params={'value': 'fulano'}
    #         )

    #     return data

    def clean(self):
        cleaned_data = super().clean()

        first_password_input = cleaned_data.get('password')
        last_password_input = cleaned_data.get('password2')

        if first_password_input != last_password_input:
            raise ValidationError({
                'password': 'Os campos devem ser iguais',
                'password2': 'Os campos devem ser iguais',
            })

        return super().clean()
