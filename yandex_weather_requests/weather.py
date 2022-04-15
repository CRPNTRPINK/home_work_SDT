from datetime import datetime
from typing import Dict
from aiohttp import ClientSession
from fastapi import HTTPException

x_yandex_api_key = '692e1361-21cd-42be-98f1-426e0c3c9fc0'
icon_url = 'https://yastatic.net/weather/i/icons/funky/dark/{}.svg'


def get_weather_by_day(name: str, data: Dict):
    days = {0: 'понедельник',
            1: 'вторник',
            2: 'среда',
            3: 'четверг',
            4: 'пятница',
            5: 'суббота',
            6: 'воскресенье'}
    for i, date in enumerate(data['forecasts']):
        weekday = days[datetime.strptime(date['date'], '%Y-%m-%d').weekday()]
        result = date['parts'], date['date']

        if i in (0, 1):
            if i == 0 and name == 'сегодня':
                return result
            elif i == 1 and name == 'завтра':
                return result
        if weekday == name:
            return result


async def get_weather(day: str = 'сегодня'):
    async with ClientSession() as session:
        request = await session.get('https://api.weather.yandex.ru/v2/forecast?lat=55.753215&lon=37.622504&lang=ru_RU',
                                    headers={'X-Yandex-API-Key': x_yandex_api_key})

        try:
            result = get_weather_by_day(day, await request.json())
            data = result[0]
            date = result[1]
        except TypeError:
            raise HTTPException(status_code=404, detail='такой даты нет')

        return {
            'днем': {
                'средняя температура': data['day']['temp_avg'],
                'иконка': icon_url.format(data['day']['icon']),
                'дата': date
            },
            'ночью': {
                'средняя температура': data['night']['temp_avg'],
                'иконка': icon_url.format(data['night']['icon']),
                'дата': date
            }
        }
