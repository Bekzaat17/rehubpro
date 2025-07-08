from django.views import View
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from storage.models import Folder, StoredFile
from storage.services.file_service import FileService

class FileView(LoginRequiredMixin, View):
    def post(self, request, folder_id=None):
        action = request.POST.get("action")
        name = request.POST.get("name")
        target_id = request.POST.get("target_id")

        if action == "upload":
            folder = get_object_or_404(Folder, id=folder_id) if folder_id else None
            FileService.upload(
                file=request.FILES["file"],
                folder=folder,
                user=request.user,
            )

        elif action == "rename":
            stored_file = get_object_or_404(StoredFile, id=target_id)
            FileService.rename(stored_file, new_name=name)

        elif action == "delete":
            stored_file = get_object_or_404(StoredFile, id=target_id)
            FileService.delete(stored_file)

        return redirect(request.META.get("HTTP_REFERER", "/storage/"))