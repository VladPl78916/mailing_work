import os
import logging
from dotenv import load_dotenv
import asyncio
from telegram import Bot
from telegram.error import TelegramError

load_dotenv()

def send_pdf_via_telegram(chat_id, file_path, caption=""):
    """Отправляет PDF-файл через Telegram бота (синхронная обертка)"""
    async def _async_send():
        """Асинхронная отправка документа"""
        try:
            bot = Bot(token=token)
            async with bot:
                await bot.send_document(
                    chat_id=chat_id,
                    document=open(file_path, 'rb'),
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
        finally:
            # Закрываем файл явно, так asyncio может не сразу закрыть его
            if 'file' in locals():
                locals()['file'].close()

    token = os.getenv('TELEGRAM_BOT_TOKEN')
    if not token:
        logging.error("TELEGRAM_BOT_TOKEN не установлен в .env файле")
        return False

    return asyncio.run(_async_send())

send_pdf_via_telegram(1108285300, "test.pdf", "some caption")