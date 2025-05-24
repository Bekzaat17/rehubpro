# users/views/auth.py

from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.views import View
from users.models import UserRole


class LoginView(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            if user.role == UserRole.ADMIN:
                return redirect('/admin-panel/')
            elif user.role == UserRole.CONSULTANT:
                return redirect('/consultant/')
            elif user.role == UserRole.PSYCHOLOGIST:
                return redirect('/psychologist/')
        else:
            return render(request, 'login.html', {'error': 'Неверный логин или пароль'})