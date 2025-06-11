from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.jobstores.memory import MemoryJobStore
from db import get_todays_birthday_recipients
from pdf_generator import create_congratulation_pdf
from time_utils import get_timezone_for_city
import datetime
import os
import pytz

scheduler = BlockingScheduler(jobstores={'default': MemoryJobStore()})

def daily_check():

    print(f"\n[{datetime.datetime.now()}] Запуск ежедневной проверки")
    
    recipients = get_todays_birthday_recipients()
    print(f"Найдено именинников: {len(recipients)}")
    
    for recipient in recipients:
        user = recipient['user']
        send_time = recipient['send_time']
        
        # Рассчитываем время выполнения по UTC
        tz = pytz.timezone(get_timezone_for_city(user['city']))
        utc_send_time = tz.localize(send_time).astimezone(pytz.utc)
        
        # Добавляем задачу в планировщик
        scheduler.add_job(
            send_congratulation,
            'date',
            run_date=utc_send_time,
            args=[user],
            id=f"bday_{user['id']}_{send_time.date()}"
        )
        print(f"Запланировано поздравление для {user['last_name']} в {send_time} ({utc_send_time} UTC)")

def send_congratulation(user):
    """Отправка поздравления (генерация PDF)"""
    print(f"\nОтправка поздравления для {user['last_name']} {user['first_name']}")
    os.makedirs('congratulations', exist_ok=True)
    filename = f"congratulations/{user['id']}_{datetime.date.today()}.pdf"
    create_congratulation_pdf(user, filename)
    print(f"Файл сохранён: {filename}")
    
    # Здесь будет код отправки по email/Telegram
    # send_email(user['email'], filename)
    # send_telegram(user['telegram_id'], filename)

if __name__ == '__main__':

    scheduler.add_job(
        daily_check,
        'cron',
        hour=6,
        minute=0,
        timezone='Europe/Moscow'
    )
    
    print("Сервис запущен. Ожидание 6:00 по Москве...")
    scheduler.start()