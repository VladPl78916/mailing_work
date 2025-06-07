import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

config = {
    'host': os.getenv('MYSQL_HOST'),
    'user': os.getenv('MYSQL_USER'),
    'password': os.getenv('MYSQL_PASSWORD'),
    'database': os.getenv('MYSQL_DB'),
    'auth_plugin': 'mysql_native_password'
}

try:
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    cursor.execute("SELECT version()")
    version = cursor.fetchone()
    print(f"Успешное подключение! Версия MySQL: {version[0]}")
    
    # Проверка таблицы
    cursor.execute("DESCRIBE users")
    print("\nСтруктура таблицы users:")
    for column in cursor:
        print(column)
        
except mysql.connector.Error as err:
    print(f"Ошибка подключения: {err}")
finally:
    if 'cursor' in locals(): cursor.close()
    if 'conn' in locals(): conn.close()