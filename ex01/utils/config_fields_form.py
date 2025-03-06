import re
from django.forms import ValidationError


class ConfigFields:
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
        ConfigFields.add_attr(my_form.fields['username'], 'class', 'form-control')

        # Adiciona um placeholder ao campo 'email'
        ConfigFields.add_attr(my_form.fields['email'], 'placeholder', 'Digite seu e-mail')
        ```

        🔹 **Resultado esperado**:
        Se o campo `username` já tiver `class="input-large"`, e chamarmos:
        ```python
        ConfigFields.add_attr(my_form.fields['username'], 'class', 'form-control')
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
        ConfigFields.add_attr(field, 'placeholder', new_value)

    @staticmethod
    def validate_password(password):
        regex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).{8,}$')

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
