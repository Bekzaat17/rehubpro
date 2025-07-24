# views/lecture_detail_view.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from lectures.models.lecture import Lecture


@login_required
def lecture_detail_view(request, pk: int):
    """
    Отображает полную информацию о конкретной лекции.

    Параметры:
        pk (int): Идентификатор лекции.

    Возвращает:
        HTML-шаблон с полной лекцией, если она опубликована.
    """
    lecture = get_object_or_404(Lecture, pk=pk, is_published=True)
    return render(request, 'lectures/lecture_detail.html', {'lecture': lecture})