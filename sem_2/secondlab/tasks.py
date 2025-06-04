from celery_app import celery_app
import itertools
import hashlib

def calculate_total(charset: str, max_length: int) -> int:
    return sum(len(charset) ** length for length in range(1, max_length + 1))

@celery_app.task(bind=True, name="bruteforce_task")
def bruteforce_task(self, hash_value: str, charset: str, max_length: int):
    total = calculate_total(charset, max_length)
    count = 0
    found = None
    
    # Перебор всех комбинаций
    for length in range(1, max_length + 1):
        for combo in itertools.product(charset, repeat=length):
            count += 1
            password = ''.join(combo)
            
            # Проверка пароля
            if hashlib.sha256(password.encode()).hexdigest() == hash_value:
                found = password
                break
                
            # Отправка прогресса каждые 1000 комбинаций
            if count % 1000 == 0:
                progress = count / total * 100
                self.update_state(
                    state='PROGRESS',
                    meta={'current': count, 'total': total, 'progress': f"{progress:.1f}%"}
                )
                
        if found:
            break
    
    return found if found else "Пароль не найден"
