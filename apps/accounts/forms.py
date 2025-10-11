from django import forms
from django.contrib.auth import get_user_model


User = get_user_model()


class LoginForm(forms.Form):
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
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already in use.")
        return email

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already in use.")
        return username

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_repeat = cleaned_data.get("password_repeat")

        if password and len(password) < 8:
            self.add_error("password", "Password must be at least 6 characters")

        if password and password_repeat and password != password_repeat:
            self.add_error("password_repeat", "Password does not match")
        return cleaned_data
