import os
import logging
from dotenv import load_dotenv
from telegram import Bot
from telegram.error import TelegramError
import asyncio

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
if not TELEGRAM_BOT_TOKEN:
    logging.error("TELEGRAM_BOT_TOKEN не установлен в .env файле")
    raise RuntimeError("Missing Telegram token")

bot_instance = Bot(token=TELEGRAM_BOT_TOKEN)

async def async_send_pdf(chat_id, file_path, caption=""):
    try:
        with open(file_path, 'rb') as file:
            await bot_instance.send_document(
                chat_id=chat_id,
                document=file,
                caption=caption
            )
        logging.info(f"PDF успешно отправлен пользователю {chat_id}")
        return True
    except TelegramError as e:
        logging.error(f"Ошибка Telegram: {e}")
        return False
    except Exception as e:
        logging.error(f"Общая ошибка: {e}")
        return False

def send_pdf_via_telegram(chat_id, file_path, caption=""):
    return asyncio.run(async_send_pdf(chat_id, file_path, caption))
    
