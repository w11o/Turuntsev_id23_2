import subprocess
def extract_hash(rar_path, output_file='hash.txt'):
    try:
        result = subprocess.run(['john/run/rar2john', rar_path], capture_output=True, text=True)
        
        if result.returncode != 0 or not result.stdout:
            print("rar2john завершился с ошибкой:")
            print(result.stderr)
            return False
        
        with open(output_file, 'w') as f:
            f.write(result.stdout)
        
        print(f"Хеш успешно извлечён и сохранён в {output_file}")
        return True

    except FileNotFoundError:
        print("rar2john не найден. Убедитесь, что вы указали правильный путь: ./run/rar2john")
        return False

rar_file = 'flag_1.rar'
extract_hash(rar_file)
