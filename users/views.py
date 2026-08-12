from django.contrib import messages
from django.shortcuts import redirect, render

from .forms import RegisterForm


def register(request):

    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)

            user.is_active = True
            user.save()

            messages.success(request, "Регистрация прошла успешно.")

            return redirect("login")

    else:
        form = RegisterForm()

    return render(request, "users/register.html", {"form": form})
