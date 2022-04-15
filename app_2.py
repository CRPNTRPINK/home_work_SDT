from fastapi import FastAPI, Query
import uvicorn
from aiohttp import  ClientSession

app = FastAPI(description='app_2')


@app.get('/weather', description='запрос для получения данных о погоде')
async def weather(day: str = Query(..., description='День недели')):
    async with ClientSession() as session:
        request = await session.get(f'http://127.0.0.1:5000/weather?day={day}')
    return await request.json()


if __name__ == '__main__':
    uvicorn.run('app_2:app', port=3000, reload=True)
