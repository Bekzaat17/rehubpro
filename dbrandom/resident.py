import random
from datetime import date, timedelta
import psycopg2

# Подключение к базе данных
conn = psycopg2.connect(
    dbname="rehabpro_db",
    user="rehabuser",              # ← замени на своего пользователя
    password="rehab123",  # ← замени на свой пароль
    host="localhost",
    port="5432"
)
cursor = conn.cursor()

# Имена резидентов
names = [
    "Иван Иванов",
    "Макс Максат",
    "Алекс Александр",
    "Али Алихан",
    "Нур Нурбек"
]

# Коды зависимостей
dependency_types = [
    "F10",  # Алкоголь
    "F11",  # Опиоиды
    "F12",  # Каннабиноиды
    "F13",  # Седативные
    "F14",  # Кокаин
    "F15",  # Психостимуляторы
    "F16",  # Галлюциногены
    "F17",  # Табак
    "F18",  # Летучие растворители
    "F19",  # Множественные
]
note_types = [
    "Вспылчивый",
    "Спокойный",
    "Срывник",
    "Обычный",
    "Умеренный",
]

def random_date(start_year, end_year):
    start_date = date(start_year, 1, 1)
    end_date = date(end_year, 12, 31)
    delta = end_date - start_date
    return start_date + timedelta(days=random.randint(0, delta.days))

def random_admission_date():
    today = date.today()
    min_days_ago = 30      # 1 месяц
    max_days_ago = 180     # 6 месяцев
    days_ago = random.randint(min_days_ago, max_days_ago)
    return today - timedelta(days=days_ago)



for name in names:
        dob = random_date(1980, 2005)
        admission_date = random_admission_date()
        dep_type = random.choice(dependency_types)
        notes = note_types[random.randint(0, len(note_types) - 1)]


        cursor.execute("""
            INSERT INTO residents_resident (
                full_name,
                date_of_birth,
                date_of_admission,
                dependency_type,
                notes,
                is_active
            ) VALUES (%s, %s, %s, %s, %s, %s)
        """, (name, dob, admission_date, dep_type, notes, True))





conn.commit()

# Close the cursor and connection
cursor.close()
conn.close()