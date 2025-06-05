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
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        password_form = CustomPasswordChangeForm(user=request.user, data=request.POST)

        if 'avatar_submit' in request.POST:
            if profile_form.is_valid():
                profile_form.save()
                messages.success(request, 'Аватар успешно обновлён.')
                return redirect('users:settings')
            else:
                messages.error(request, 'Ошибка при загрузке аватара.')

        elif 'password_submit' in request.POST:
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Пароль успешно изменён.')
                return redirect('users:settings')
            else:
                messages.error(request, 'Ошибка при смене пароля.')

        # Возвращаем шаблон с формами и ошибками
        context = {
            'profile_form': profile_form,
            'password_form': password_form,
        }
        return self.render_to_response(context)