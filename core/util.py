# core/util.py

from datetime import date

def format_date(value: date | None) -> str:
    """
    Преобразует дату в строку по формату.
    Если дата не указана — возвращает прочерк.
    """
    date_format = "%d.%m.%Y"  # Например: 31.05.2025
    if not value:
        return "—"
    return value.strftime(date_format)