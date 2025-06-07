import mysql.connector
import os
from dotenv import load_dotenv
from datetime import datetime
from time_utils import get_local_time

load_dotenv()

def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv('MYSQL_HOST'),
        user=os.getenv('MYSQL_USER'),
        password=os.getenv('MYSQL_PASSWORD'),
        database=os.getenv('MYSQL_DB')
    )

def get_todays_birthday_recipients():
    """Возвращает пользователей, у которых сегодня ДР в их часовом поясе"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users")
    all_users = cursor.fetchall()
    cursor.close()
    conn.close()
    
    recipients = []
    for user in all_users:
        local_time = get_local_time(user['city'])
        birth_date = user['birth_date']
        
        if isinstance(birth_date, str):
            birth_date = datetime.strptime(birth_date, '%Y-%m-%d').date()
        
        if (birth_date.month, birth_date.day) == (local_time.month, local_time.day):
            recipients.append({
                'user': user,
                'send_time': local_time.replace(hour=8, minute=0, second=0, microsecond=0)
            })
    
    return recipients