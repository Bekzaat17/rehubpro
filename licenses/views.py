from django.shortcuts import render

def license_expired_view(request):
    return render(request, "licenses/expired.html", status=403)