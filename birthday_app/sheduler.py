from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.jobstores.memory import MemoryJobStore
from db import get_todays_birthday_recipients
from pdf_generator import create_congratulation_pdf
from time_utils import get_timezone_for_city
from datetime import datetime, timedelta
import os
import pytz

import logging
from telegram_sender import send_pdf_via_telegram
from datetime import datetime as dt

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("birthday_bot.log"),
        logging.StreamHandler()
    ]
)

scheduler = BlockingScheduler(timezone=pytz.utc, jobstores={'default': MemoryJobStore()})

TEST_MODE = True

def daily_check():
    """Задача, выполняемая каждый день в 6 утра по Москве (или немедленно в тестовом режиме)"""
    if TEST_MODE:
        print("\n" + "="*50)
        print("РЕЖИМ ТЕСТИРОВАНИЯ АКТИВИРОВАН")
        print("="*50 + "\n")
    
    # Имитация времени запуска
    now = datetime.now(pytz.timezone('Europe/Moscow'))
    print(f"[{'ТЕСТ: ' if TEST_MODE else ''}Запуск проверки ДР в {now.strftime('%Y-%m-%d %H:%M:%S')}]")
    
    # Получаем именинников
    birthday_people = get_todays_birthday_recipients()
    
    if not birthday_people:
        print("Сегодня нет именинников")
        return
    
    print(f"Найдено {len(birthday_people)} именинников")
    
    for recipient in birthday_people:
        user = recipient['user']
        send_time = recipient['send_time']
        
        if TEST_MODE:
            # В тестовом режиме отправляем через 1 минуту
            test_send_time = datetime.now(pytz.utc) + timedelta(minutes=1)
            print(f"[ТЕСТ] Переназначено время отправки для {user['last_name']} на {test_send_time} UTC")
        else:
             # Исправленная версия работы с часовыми поясами
            tz = pytz.timezone(get_timezone_for_city(user['city']))
            # Создаем datetime с указанием часового пояса
            localized_time = tz.localize(send_time, is_dst=False)
            # Конвертируем в UTC
            test_send_time = localized_time.astimezone(pytz.utc)
        
        # Добавляем задачу в планировщик
        scheduler.add_job(
            send_congratulation,
            'date',
            run_date=test_send_time,
            args=[user],
            id=f"bday_{user['id']}_{send_time.date()}" + ("_TEST" if TEST_MODE else ""),
            misfire_grace_time=300
        )
        print(f"Запланировано поздравление для {user['last_name']} в {test_send_time} UTC")

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


def list_scheduled_jobs():
    print("\nСписок запланированных задач:")
    jobs = scheduler.get_jobs()
    for job in jobs:
        print(f"- ID: {job.id}, Время запуска: {job.next_run_time}, Аргументы: {job.args}")
    if not jobs:
        print("Нет запланированных задач")

if __name__ == '__main__':

    scheduler.add_job(
        daily_check,
        'cron',
        hour=6,
        minute=0,
        timezone='Europe/Moscow'
    )
    
    list_scheduled_jobs()

    print("Сервис запущен. Ожидание 6:00 по Москве...")
    scheduler.start()