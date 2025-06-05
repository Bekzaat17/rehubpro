from django.contrib.auth import logout
from django.shortcuts import redirect
from django.views import View
from django.urls import reverse


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect(reverse('users:login'))