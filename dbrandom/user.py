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

# Insert user data into the users_user table
insert_user_query = """
    INSERT INTO users_user (password, last_login, is_superuser, username, email, role, is_active, is_staff, avatar)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

# Values for the user
user_values = (
    'password',
    '2025-07-13 21:17:00+05',  # Current time based on your provided date and time
    True,
    'user_consultant',
    'email@mail.ru',
    'consultant',
    True,
    True,
    None
)

# Execute the query
cursor.execute(insert_user_query, user_values)
conn.commit()

# Close the cursor and connection
cursor.close()
conn.close()