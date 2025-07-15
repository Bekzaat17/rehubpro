# users/views/settings_view.py

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import update_session_auth_hash
from django.views.generic import TemplateView
from django.contrib import messages
from django.shortcuts import redirect

from users.forms.profile import ProfileUpdateForm
from users.forms.password import CustomPasswordChangeForm


class UserSettingsView(LoginRequiredMixin, TemplateView):
    template_name = 'users/settings.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile_form'] = ProfileUpdateForm(instance=self.request.user)
        context['password_form'] = CustomPasswordChangeForm(user=self.request.user)
        return context

    def post(self, request, *args, **kwargs):
        # Флаг для понимания, какую форму обрабатываем
        is_avatar_submit = 'avatar_submit' in request.POST
        is_password_submit = 'password_submit' in request.POST

        if is_avatar_submit:
            profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
            password_form = CustomPasswordChangeForm(user=request.user)  # не обрабатываем
            if profile_form.is_valid():
                profile_form.save()
                messages.success(request, 'Аватар успешно обновлён.')
                return redirect('users:settings')
            else:
                messages.error(request, 'Ошибка при загрузке аватара.')

        elif is_password_submit:
            profile_form = ProfileUpdateForm(instance=request.user)  # не обрабатываем
            password_form = CustomPasswordChangeForm(user=request.user, data=request.POST)
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Пароль успешно изменён.')
                return redirect('users:settings')
            else:
                messages.error(request, 'Ошибка при смене пароля.')

        else:
            profile_form = ProfileUpdateForm(instance=request.user)
            password_form = CustomPasswordChangeForm(user=request.user)

        return self.render_to_response({
            'profile_form': profile_form,
            'password_form': password_form,
        })