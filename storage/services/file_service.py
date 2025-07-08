from storage.models import StoredFile, Folder
from django.core.files.uploadedfile import UploadedFile
from django.contrib.auth import get_user_model

User = get_user_model()

class FileService:
    @staticmethod
    def upload(file: UploadedFile, folder: Folder, user: User) -> StoredFile:
        return StoredFile.objects.create(
            folder=folder,
            file=file,
            name=file.name,
            uploaded_by=user
        )

    @staticmethod
    def rename(stored_file: StoredFile, new_name: str) -> StoredFile:
        stored_file.name = new_name
        stored_file.save(update_fields=['name'])
        return stored_file

    @staticmethod
    def delete(stored_file: StoredFile) -> None:
        stored_file.file.delete(save=False)  # удалить физически
        stored_file.delete()