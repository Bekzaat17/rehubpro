from django.urls import path

from storage.views.folder_view import FolderView
from storage.views.file_view import FileView

app_name = 'storage'

urlpatterns = [
    path("", FolderView.as_view(), name="root"),
    path("folder/<int:folder_id>/", FolderView.as_view(), name="folder_detail"),
    path("folder/<int:folder_id>/files/", FileView.as_view(), name="file_actions"),
    path("files/", FileView.as_view(), name="file_actions_root"),
]