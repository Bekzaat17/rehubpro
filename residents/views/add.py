from django.views import View
from django.shortcuts import redirect
from residents.forms import ResidentForm

class AddResidentView(View):
    def post(self, request):
        form = ResidentForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect(request.META.get('HTTP_REFERER', '/'))