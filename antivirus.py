import hashlib
import os

def scan_directory(directory, hash_database="MD5 Hashes.txt"):
    """Сканирует папку на наличие файлов с хешами из базы данных."""
    if not os.path.exists(hash_database):
        return []

    with open(hash_database, "r") as file:
        malicious_hashes = set(line.strip() for line in file)

    suspicious_files = []
    for root, _, files in os.walk(directory):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            file_hash = calculate_md5(file_path)
            if file_hash in malicious_hashes:
                suspicious_files.append(file_path)

    return suspicious_files

def calculate_md5(file_path):
    """Вычисляет MD5 хеш файла."""
    try:
        with open(file_path, "rb") as file:
            file_hash = hashlib.md5()
            while chunk := file.read(4096):
                file_hash.update(chunk)
            return file_hash.hexdigest()
    except Exception as e:
        return None

def delete_file(file_path):
    """Удаляет файл."""
    try:
        os.remove(file_path)
        return f"Удалён файл: {file_path}"
    except Exception as e:
        return f"Ошибка удаления {file_path}: {e}"
