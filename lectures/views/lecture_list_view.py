# views/lecture_list_view.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from lectures.models.lecture import Lecture

@login_required
def lecture_list_view(request):
    """
    Отображает список всех опубликованных лекций.

    Лекции упорядочены по дате публикации (от новых к старым).
    Доступны всем пользователям.
    """
    lectures = Lecture.objects.filter(is_published=True).order_by('-created_at')
    return render(request, 'lectures/lecture_list.html', {'lectures': lectures})