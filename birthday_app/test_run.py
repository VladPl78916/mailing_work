from sheduler import scheduler, daily_check
import time

# 1. Запускаем проверку немедленно (имитация 6 утра)
print("Запуск тестовой проверки...")
daily_check()

# 2. Запускаем планировщик
print("\nЗапуск планировщика...")
scheduler.start()

# 3. После завершения работы планировщика
print("\nТестирование завершено. Проверьте результаты:")
print("- Получены ли сообщения в Telegram")
print("- Сгенерированы ли PDF в папке congratulations")
print("- Проверьте логи в консоли")