import pytz
from datetime import datetime
from timezonefinder import TimezoneFinder
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

tf = TimezoneFinder()
timezone_cache = {}

RUSSIAN_CITIES_TZ = {
    'Москва': 'Europe/Moscow',
    'Санкт-Петербург': 'Europe/Moscow',
    'Новосибирск': 'Asia/Novosibirsk',
    'Екатеринбург': 'Asia/Yekaterinburg',
    'Казань': 'Europe/Moscow',
    'Нижний Новгород': 'Europe/Moscow',
    'Челябинск': 'Asia/Yekaterinburg',
    'Омск': 'Asia/Omsk',
    'Самара': 'Europe/Samara',
    'Ростов-на-Дону': 'Europe/Moscow',
    'Уфа': 'Asia/Yekaterinburg',
    'Красноярск': 'Asia/Krasnoyarsk',
    'Владивосток': 'Asia/Vladivostok',
    'Иркутск': 'Asia/Irkutsk',
    'Хабаровск': 'Asia/Vladivostok'
}

def get_timezone_for_city(city):
    """Определяем часовой пояс с приоритетом для российских городов"""
    city_normalized = city.strip().title()
    
    # Проверка кэша
    if city_normalized in timezone_cache:
        return timezone_cache[city_normalized]
    
    # Сначала проверяем российские города
    if city_normalized in RUSSIAN_CITIES_TZ:
        tz = RUSSIAN_CITIES_TZ[city_normalized]
        timezone_cache[city_normalized] = tz
        return tz
    
    # Для международных городов
    try:
        tz_name = tf.timezone_at(city=city_normalized)
        if not tz_name:
            tz_name = 'Europe/Moscow'
        
        timezone_cache[city_normalized] = tz_name
        return tz_name
    except Exception as e:
        logger.error(f"Ошибка определения пояса для {city}: {e}")
        return 'Europe/Moscow'

def get_local_time(city):
    """Текущее время в городе с обработкой ошибок"""
    tz_name = get_timezone_for_city(city)
    try:
        return datetime.now(pytz.timezone(tz_name))
    except pytz.UnknownTimeZoneError:
        logger.warning(f"Неизвестный пояс: {tz_name}. Используем Москву")
        return datetime.now(pytz.timezone('Europe/Moscow'))