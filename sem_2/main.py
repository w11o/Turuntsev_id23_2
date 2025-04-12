
#source myenv/bin/activate - wsl

from fastapi.responses import JSONResponse
from fastapi import FastAPI
import subprocess
import itertools
from typing import Dict
import asyncio
from concurrent.futures import ThreadPoolExecutor

app = FastAPI()
tasks: Dict[str, Dict] = {}
task_id = -1

def run_task(task_id: str, hash_value: str, charset: str, max_length: int):
    generate_passwords(task_id, charset, max_length)
    crack_pass(task_id, hash_value)


@app.post("/brut_hash")
async def create_task(hash_value: str, charset: str, max_length: int):
    global task_id

    if max_length > 8:
        return JSONResponse(content={"error": "Максимальная длина не должна превышать 8 символов"}, status_code=400)
    task_id+=1
    
    # generate_passwords(charset, max_length)
    # pswd = crack_pass(hash_value)
    tasks[task_id] = {
        "status": "running",
        "hash_value": hash_value,
        "charset": charset,
        "progress": 0,
        "result": None
    }
    loop = asyncio.get_running_loop()
    with ThreadPoolExecutor() as pool:
        await loop.run_in_executor(pool, run_task, task_id, hash_value, charset, max_length)

    return JSONResponse(content={"task_id": task_id}, status_code=200)

@app.get("/get_status")
async def get_status(id: int):
    return tasks[id]



def generate_passwords(task_id, charset: str, max_length: int, output_file: str = "passwords.txt"):
    with open(str(task_id) + output_file, "w") as f:
        for length in range(1, max_length + 1):
            for combo in itertools.product(charset, repeat=length):
                password = ''.join(combo)
                f.write(password + '\n')



def crack_pass(task_id, hash_str):
    hash_str = hash_str.split(':', 1)[1]

    wordlist = str(task_id) + 'passwords.txt'

    with open('rar5_hash.txt', 'w') as f:
        f.write(hash_str)

    subprocess.run([
        'hashcat',
        '-m', '13000',
        '-a', '0',
        'rar5_hash.txt',
        wordlist,
        '--force'
    ])

    result = subprocess.check_output([
        'hashcat',
        '-m', '13000',
        'rar5_hash.txt',
        '--show'
    ]).decode()

    if ':' in result:
        password = result.strip().split(':', 1)[1]
        with open('found.txt', 'w') as f:
            f.write(password + '\n')
        print(f'[+] Пароль найден и сохранён в found.txt: {password}')
        tasks[task_id]["status"] = "completed"
        tasks[task_id]["result"] = password
        tasks[task_id]["progress"] = "100%"
    else:
        print('[-] Пароль не найден.')
        tasks[task_id]["status"] = "failed"
        tasks[task_id]["result"] = "пароль не найден"
        tasks[task_id]["progress"] = "0% "


