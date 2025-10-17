from django import forms
from django.contrib.auth import get_user_model


User = get_user_model()


class LoginForm(forms.Form):
    """
        Форма для авторизації користувача в системі.

        Поля:
            email: Email адреса користувача
            password: Пароль користувача
            remember: Чекбокс для запам'ятовування сесії користувача
    """
    email = forms.CharField(
        label="Email",
        required=True,
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "id": "email",
                "placeholder": " ",
            }
        ),
    )
    password = forms.CharField(
        label="Password",
        required=True,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "id": "password-field",
                "placeholder": " ",
            }
        ),
    )
    remember = forms.BooleanField(
        required=False,
        initial=True,
        widget=forms.CheckboxInput(
            attrs={
                "class": "checkbox-primary",
                "value": "remember",
            }
        ),
    )


class RegisterForm(forms.ModelForm):
    """
        Форма для реєстрації нового користувача в системі.

        Поля:
            email: Email адреса користувача (має бути унікальною)
            username: Ім'я користувача (має бути унікальним)
            password: Пароль користувача (мінімум 8 символів)
            password_repeat: Повторення пароля для підтвердження
    """
    email = forms.CharField(
        label="Email",
        required=True,
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "id": "email",
                "placeholder": " ",
            }
        ),
    )
    username = forms.CharField(
        label="Username",
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "id": "username",
                "placeholder": " ",
            }
        ),
    )
    password = forms.CharField(
        label="Password",
        required=True,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "id": "password-field",
                "placeholder": " ",
            }
        ),
    )

    password_repeat = forms.CharField(
        label="Repeat Password",
        required=True,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "id": "repeat-password-field",
                "placeholder": " ",
            }
        ),
    )

    class Meta:
        model = User
        fields = ["username", "email", "password", "password_repeat"]

    def clean_email(self):
        """
            Перевіряє унікальність email адреси.

            Returns:
                str: Валідована email адреса

            Raises:
                forms.ValidationError: Якщо email вже використовується
        """
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already in use.")
        return email

    def clean_username(self):
        """
            Перевіряє унікальність імені користувача.

            Returns:
                str: Валідоване ім'я користувача

            Raises:
                forms.ValidationError: Якщо ім'я користувача вже використовується
        """
        username = self.cleaned_data.get("username")
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already in use.")
        return username

    def clean(self):
        """
            Виконує валідацію всієї форми.

            Перевіряє:
            - Мінімальну довжину пароля (8 символів)
            - Збіг паролів у полях password та password_repeat

            Returns:
                dict: Словник з очищеними даними форми

            Raises:
                forms.ValidationError: Якщо пароль занадто короткий або паролі не збігаються
        """
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_repeat = cleaned_data.get("password_repeat")

        if password and len(password) < 8:
            self.add_error("password", "Password must be at least 8 characters")

        if password and password_repeat and password != password_repeat:
            self.add_error("password_repeat", "Password does not match")
        return cleaned_data
