import requests
import json
import asyncio
import websockets

async def track_task(task_id: str):
    async with websockets.connect(f"ws://localhost:8000/ws/{task_id}") as websocket:
        while True:
            message = await websocket.recv()
            data = json.loads(message)
            print(f"Статус: {data.get('status')}, Прогресс: {data.get('progress', 'N/A')}")
            
            if data.get('status') in ['SUCCESS', 'FAILURE']:
                print(f"Результат: {data.get('result')}")
                break

def main():
    # Пример хэша SHA-256 для "1234"
    hash_value = "03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4"
    
    # Отправка запроса
    response = requests.post(
        "http://localhost:8000/brut_hash",
        json={"hash_value": hash_value, "charset": "0123456789", "max_length": 4}
    )
    
    if response.status_code != 200:
        print(f"Ошибка: {response.text}")
        return
    
    task_id = response.json()["task_id"]
    print(f"Задача создана. ID: {task_id}")
    
    # Подключение к WebSocket
    asyncio.run(track_task(task_id))

if __name__ == "__main__":
    main()