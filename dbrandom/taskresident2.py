import random
from datetime import date, timedelta
import psycopg2

# Подключение к базе данных
conn = psycopg2.connect(
    dbname="rehabpro_db",
    user="rehabuser",
    password="rehab123",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()

comment_types = [
    "Молодец",
    "Сдал успешно 1 пример",
    "Еле сдал",
    "Сдал 3 примера",
    "Неплохо",
]

i = 1
while i <= 10:
    today = date.today()
    if i >= 5:
        created_at = today - timedelta(days=8)
    else:
        created_at = today - timedelta(days=1)
    stage = "completed"
    updated_by_id = 1
    assigned_task_id = i
    comment = random.choice(comment_types)
    cursor.execute("""
                    INSERT INTO tasks_taskprogress (
                        stage,
                        created_at,
                        comment,
                        assigned_task_id,
                        updated_by_id,
                    ) VALUES (%s, %s, %s, %s, %s)
                """, (stage, created_at, comment, assigned_task_id, updated_by_id))
    i += 1
