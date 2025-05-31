# users/views/auth.py

from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse

from users.models import UserRole


class LoginView(View):
    def get(self, request):
        form = AuthenticationForm()
        return render(request, 'users/login.html', {'form': form})

    def post(self, request):
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)

            match user.role:
                # case UserRole.ADMIN:
                #     return redirect(reverse('admin:dashboard'))
                case UserRole.CONSULTANT:
                    return redirect(reverse('users:dashboard'))
                # case UserRole.PSYCHOLOGIST:
                #     return redirect(reverse('psychologist:dashboard'))

        # Если невалидно — снова рендерим форму с ошибками
        return render(request, 'users/login.html', {'form': form})