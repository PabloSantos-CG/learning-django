from unittest import TestCase
from django.test import TestCase as DjangoTestCase
from django.urls import reverse
from parameterized import parameterized
from authors.forms import RegisterForm


class AuthorRegisterFromTestCase(TestCase):
    @parameterized.expand([
        ('username', 'Seu username'),
        ('email', 'Seu e-mail'),
        ('first_name', 'Ex.: John'),
        ('last_name', 'Ex.: Doe'),
        ('password', 'Informe sua senha'),
        ('password2', 'Repita sua senha'),
    ])
    def test_fields_placeholder(self, field, placeholder):
        form = RegisterForm()
        current_placecholder = form[field].field.widget.attrs['placeholder']

        self.assertEqual(current_placecholder, placeholder)

    def test_error_messages_password(self):
        form = RegisterForm()
        message = 'Este campo é obrigatório.'
        error_messages = form['password'].field.error_messages['required']

        self.assertEqual(error_messages, message)

    def test_help_text_password(self):
        form = RegisterForm()
        message = (
            'A senha deve ter pelo menos uma letra maiúscula, '
            'uma letra minúscula e um número.'
            'O comprimento deve ser de pelo menos 8 caracteres.'
        )
        help_text_message = form['password'].field.help_text

        self.assertEqual(help_text_message, message)

    @parameterized.expand([
        ('first_name', 'Primeiro nome:'),
        ('last_name', 'Último sobrenome:'),
        ('username', 'Nome de Usuário:'),
        ('email', 'E-mail:'),
        ('password', 'Senha:'),
        ('password2', 'Repita a senha:'),
    ])
    def test_fields_label(self, field, label):
        form = RegisterForm()
        current_label = form[field].field.label

        self.assertEqual(current_label, label)


class AuthorRegisterFromIntegrationTest(DjangoTestCase):
    def setUp(self) -> None:
        self.form_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'username': 'john_doe',
            'email': 'john_doe@email.com',
            'password': 'John.doe1234',
            'password2': 'John.doe1234',
        }
        return super().setUp()

    @parameterized.expand([
        ('username', 'Este campo é obrigatório.'),
    ])
    def test_fields_cannot_be_empty(self, field, msg):
        self.form_data[field] = ''
        url = reverse('authors:create')
        response = self.client.post(url, self.form_data, follow=True)

        self.assertIn(msg, response.content.decode('utf-8'))