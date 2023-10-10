from fastapi import FastAPI
from fastapi.responses import JSONResponse
import asyncio

app = FastAPI()

# Глобальный словарь для хранения информации, которую клиенты будут запрашивать
data = {"message": "Initial data"}


# Обработчик для long polling
@app.get("/poll")
async def poll_data():
    while True:
        await asyncio.sleep(1)  # Имитация ожидания новых данных
        if data.get("message"):
            return JSONResponse(content=data, )


# Маршрут для обновления данных
@app.post("/update")
async def update_data(new_message: dict):
    print(new_message)
    data["message"] = new_message["new_message"]
    return {"message": "Data updated successfully"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
