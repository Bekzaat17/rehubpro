from storage.models import Folder

class FolderService:
    @staticmethod
    def create(name: str, parent: Folder | None = None) -> Folder:
        return Folder.objects.create(name=name, parent=parent)

    @staticmethod
    def rename(folder: Folder, new_name: str) -> Folder:
        folder.name = new_name
        folder.save(update_fields=['name'])
        return folder

    @staticmethod
    def delete(folder: Folder) -> None:
        folder.delete()