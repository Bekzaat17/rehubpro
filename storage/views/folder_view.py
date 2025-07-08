from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from storage.models import Folder
from storage.services.folder_service import FolderService

class FolderView(LoginRequiredMixin, View):
    def get(self, request, folder_id=None):
        query = request.GET.get("q", "").strip()

        current_folder = get_object_or_404(Folder, id=folder_id) if folder_id else None
        subfolders = current_folder.subfolders.all() if current_folder else Folder.objects.filter(parent=None)
        files = current_folder.files.all() if current_folder else []

        if query:
            subfolders = subfolders.filter(name__icontains=query)
            files = files.filter(name__icontains=query)

        return render(request, "storage/folder_list.html", {
            "current_folder": current_folder,
            "subfolders": subfolders,
            "files": files,
            "query": query,
        })

    def post(self, request, folder_id=None):
        action = request.POST.get("action")
        name = request.POST.get("name")
        target_id = request.POST.get("target_id")

        if action == "create":
            parent = get_object_or_404(Folder, id=folder_id) if folder_id else None
            FolderService.create(name=name, parent=parent)

        elif action == "rename":
            folder = get_object_or_404(Folder, id=target_id)
            FolderService.rename(folder, new_name=name)

        elif action == "delete":
            folder = get_object_or_404(Folder, id=target_id)
            FolderService.delete(folder)

        return redirect(request.path)