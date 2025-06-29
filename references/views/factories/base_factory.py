from abc import ABC, abstractmethod

class BaseReferenceFactory(ABC):
    """
    Абстрактная фабрика, предоставляющая доступ к модели и форме справочника.
    """

    @abstractmethod
    def get_model(self):
        raise NotImplementedError

    @abstractmethod
    def get_form(self):
        raise NotImplementedError

    @abstractmethod
    def get_verbose_name(self):
        raise NotImplementedError

    def get_columns(self):
        """
        Список полей, отображаемых в таблице.
        """
        return ["name", "is_active"]  # по умолчанию

    def get_slug(self):
        """
        Уникальный slug, по умолчанию от имени модели.
        Можно переопределить в дочерних фабриках.
        """
        return self.get_model().__name__.lower()