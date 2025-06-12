from time_utils import get_local_time

cities = {
    'Москва': 'Europe/Moscow',
    'Владивосток': 'Asia/Vladivostok',
    'Санкт-Петербург': 'Europe/Moscow'
}

for city, expected_tz in cities.items():
    local_time = get_local_time(city)
    print(f"{city}: {local_time.strftime('%Y-%m-%d %H:%M:%S %Z%z')}")
    assert local_time.tzinfo.zone == expected_tz, f"Ошибка для {city}"