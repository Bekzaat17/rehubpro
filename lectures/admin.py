from django.contrib import admin
from .models.lecture import Lecture
from .models.lecture_category import LectureCategory

@admin.register(Lecture)
class LectureAdmin(admin.ModelAdmin):
    """
    Админ-панель для управления лекциями.
    Позволяет фильтровать, искать и просматривать лекции.
    """
    list_display = ('title', 'category', 'created_by', 'created_at')  # Добавлено отображение категории
    search_fields = ('title', 'description')                          # Поля для поиска
    list_filter = ('created_at', 'category',)                         # Фильтр по дате и категории

@admin.register(LectureCategory)
class LectureCategoryAdmin(admin.ModelAdmin):
    """
    Админ-панель для управления категориями лекций.
    """
    list_display = ('name',)
    search_fields = ('name',)