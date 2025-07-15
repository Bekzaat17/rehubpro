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


def insert_sample_tasks():
    tasks = [
        ("+/- в употреблении", "Тестовое описание задании", "long_term"),
        ("Тест", "Тестовое описание задании", "test"),
        ("Потери", "Тестовое описание задании", "short_term")
    ]

    insert_query = """
    INSERT INTO tasks_tasktemplate (title, description, task_type)
    VALUES (%s, %s, %s)
    """
    cursor.executemany(insert_query, tasks)
    conn.commit()


# Основная функция
def main():
    try:
        insert_sample_tasks()
        print("Данные успешно вставлены в таблицу")

    except Exception as e:
        print(f"Произошла ошибка: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    main()