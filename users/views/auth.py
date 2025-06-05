# users/views/auth.py

from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect

from users.models import UserRole


class LoginView(View):
    template_name = 'users/login.html'
    form_class = AuthenticationForm

    def dispatch(self, request, *args, **kwargs):
        """
        Перенаправление, если пользователь уже вошёл в систему.
        """
        if request.user.is_authenticated:
            return redirect(reverse('users:dashboard'))
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        """
        Отображение формы входа.
        """
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    @method_decorator(csrf_protect)
    def post(self, request):
        """
        Обработка формы входа.
        """
        form = self.form_class(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return self.redirect_by_role(user)

        return render(request, self.template_name, {'form': form})

    def redirect_by_role(self, user):
        """
        Перенаправление в зависимости от роли пользователя.
        """
        match user.role:
            case UserRole.CONSULTANT:
                return redirect(reverse('users:dashboard'))
            # case UserRole.ADMIN:
            #     return redirect(reverse('admin:dashboard'))
            # case UserRole.PSYCHOLOGIST:
            #     return redirect(reverse('psychologist:dashboard'))
            case _:
                return redirect(reverse('home'))