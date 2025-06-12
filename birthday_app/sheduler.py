from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.jobstores.memory import MemoryJobStore
from db import get_todays_birthday_recipients
from pdf_generator import create_congratulation_pdf
from time_utils import get_timezone_for_city
import datetime
import os
import pytz

# Добавьте в начало файла
import logging
from telegram_sender import send_pdf_via_telegram
from datetime import datetime as dt

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("birthday_bot.log"),
        logging.StreamHandler()
    ]
)

scheduler = BlockingScheduler(jobstores={'default': MemoryJobStore()})

def daily_check():

    print(f"\n[{datetime.datetime.now()}] Запуск ежедневной проверки")
    
    recipients = get_todays_birthday_recipients()
    print(f"Найдено именинников: {len(recipients)}")
    
    for recipient in recipients:
        user = recipient['user']
        send_time = recipient['send_time']
        
        tz = pytz.timezone(get_timezone_for_city(user['city']))
        utc_send_time = tz.localize(send_time).astimezone(pytz.utc)
        
        # Добавляем задачу в планировщик
        scheduler.add_job(
            send_congratulation,
            'date',
            run_date=utc_send_time,
            args=[user],
            id=f"bday_{user['id']}_{send_time.strftime('%Y%m%d')}",
            misfire_grace_time=300
        )
        logging.info(f"Запланирована отправка для {user['last_name']} в {send_time} ({utc_send_time} UTC)")

def send_congratulation(user):

    try:
        filename = f"congratulations/{user['id']}_{dt.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        create_congratulation_pdf(user, filename)
        logging.info(f"PDF создан: {filename}")
        
        caption = (
            f"Дорогой(ая) {user['first_name']} {user['last_name']}!\n\n"
            "Сердечно поздравляем Вас с Днём Рождения!\n"
            "Желаем здоровья, счастья и профессиональных успехов!"
        )

        telegram_id = user['telegram_id']
        if telegram_id:
            if telegram_id.startswith('@'):
                telegram_id = telegram_id[1:]
                
            if send_pdf_via_telegram(telegram_id, filename, caption):
                logging.info(f"Поздравление отправлено пользователю {telegram_id}")
            else:
                logging.error(f"Ошибка отправки пользователю {telegram_id}")
        else:
            logging.warning(f"У пользователя {user['id']} не указан telegram_id")
            
        try:
            os.remove(filename)
            logging.info(f"Временный файл удален: {filename}")
        except OSError as e:
            logging.error(f"Ошибка удаления файла: {e}")
            
    except Exception as e:
        logging.error(f"Ошибка при отправке поздравления: {e}")

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