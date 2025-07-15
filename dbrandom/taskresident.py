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

# First loop: Assign tasks 8 days ago
i = 1
while i <= 5:
    today = date.today()
    assigned_at = today - timedelta(days=8)
    status = "completed"
    assigned_by_id = 1
    resident_id = i
    # Ensure task_id exists in tasks_tasktemplate (adjust range if needed)
    task_id = random.randint(2, 4)  # Replace with valid IDs from tasks_tasktemplate
    cursor.execute("""
                    INSERT INTO tasks_assignedtask (
                        assigned_at,
                        status,
                        assigned_by_id,
                        resident_id,
                        task_id
                    ) VALUES (%s, %s, %s, %s, %s)
                """, (assigned_at, status, assigned_by_id, resident_id, task_id))
    i += 1

# Second loop: Assign tasks 1 day ago
j = 1
while j <= 5:
    today = date.today()
    assigned_at = today - timedelta(days=1)
    status = "completed"
    assigned_by_id = 1
    resident_id = j
    # Ensure task_id exists in tasks_tasktemplate (adjust range if needed)
    task_id = random.randint(2, 4)  # Replace with valid IDs from tasks_tasktemplate
    cursor.execute("""
                    INSERT INTO tasks_assignedtask (
                        assigned_at,
                        status,
                        assigned_by_id,
                        resident_id,
                        task_id
                    ) VALUES (%s, %s, %s, %s, %s)
                """, (assigned_at, status, assigned_by_id, resident_id, task_id))
    j += 1

# Commit and close
conn.commit()
cursor.close()
conn.close()