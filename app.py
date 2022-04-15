from fastapi import FastAPI, Query
import uvicorn
from yandex_weather_requests.weather import get_weather

app = FastAPI(description='app_1')


@app.get('/weather')
async def weather(day: str):
    return await get_weather(day.lower())


if __name__ == '__main__':
    uvicorn.run('app:app', port=5000, reload=True)
