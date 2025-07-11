from django.views import View
from django.shortcuts import render
from django.contrib.auth import get_user_model

User = get_user_model()

class DevPanelView(View):
    def get(self, request):
        return render(request, "test/dev_panel.html")

    def post(self, request):
        action = request.POST.get("action")
        result = "test123"
        error = None
        result += "456"

        return render(request, "test/dev_panel.html", {
            "result": result,
            "error": error
        })