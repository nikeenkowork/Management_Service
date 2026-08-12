from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import User


class RegisterForm(UserCreationForm):

    email = forms.EmailField(label="Email", help_text="Введите ваш email")

    class Meta:
        model = User
        fields = (
            "email",
            "password1",
            "password2",
        )

    def save(self, commit=True):

        user = super().save(commit=False)

        user.username = None

        if commit:
            user.save()

        return user
