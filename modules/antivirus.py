import hashlib
import os, sys, requests
from .logger import *

if getattr(sys, 'frozen', False):
    application_path = os.path.dirname(sys.executable)
elif __file__:
    application_path = os.path.dirname(__file__)

LIST_DATABASES_URL = "https://raw.githubusercontent.com/ZhenyaYoratt/nh-db/refs/heads/main/antivirus_dbs"
DATABASES_FORLDER = os.path.join(application_path, '..', 'databases')

def update_database(main_url=LIST_DATABASES_URL, databases_folder=DATABASES_FORLDER):
    """
    Обновляет базу данных, загружая файлы по ссылкам, полученным с главной ссылки.

    :param main_url: Главная ссылка для получения списка ссылок с файлами (в формате JSON).
    :param databases_folder: Папка, куда будут сохраняться файлы (по умолчанию 'databases').
    """
    if not os.path.exists(databases_folder):
        os.makedirs(databases_folder)

    try:
        # Загружаем список ссылок с JSON-формата
        response = requests.get(main_url)
        response.raise_for_status()  # Проверка успешности запроса
        file_links = response.text.split('\n') # Получаем JSON, который содержит ссылки на файлы

        # Скачиваем каждый файл по ссылке
        for file_url in file_links:
            try:
                file_name = file_url.split("/")[-1]  # Извлекаем имя файла из URL
                file_path = os.path.join(databases_folder, file_name)

                if not os.path.exists(file_path):

                    # Загружаем файл
                    file_response = requests.get(file_url)
                    file_response.raise_for_status()  # Проверка успешности запроса

                    with open(file_path, 'wb') as f:
                        f.write(file_response.content)

            except requests.RequestException as e:
                log(f"Ошибка при загрузке файла {file_url}: {e}", ERROR)
    except requests.RequestException as e:
        log(f"Ошибка при получении списка файлов: {e}", ERROR)

def load_database(databases_folder=DATABASES_FORLDER):
    """
    Загружает базу данных из файлов в папке `databases`, исключая строки, начинающиеся с #.

    :param databases_folder: Папка с файлами базы данных (по умолчанию 'databases').
    :return: Список строк из файлов, исключая строки, начинающиеся с '#'.
    """
    database_content = []

    # Проверяем, существует ли папка с файлами
    if not os.path.exists(databases_folder):
        print(f"Папка {databases_folder} не найдена.")
        return []

    # Проходим по всем файлам в папке
    for filename in os.listdir(databases_folder):
        file_path = os.path.join(databases_folder, filename)

        # Пропускаем директории
        if os.path.isdir(file_path):
            continue

        # Открываем и читаем файл
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                # Пропускаем строки, начинающиеся с '#'
                if not line.startswith('#'):
                    database_content.append(line.strip())

    return database_content

def scan_directory(directory):
    """Сканирует папку на наличие файлов с хешами из базы данных."""
    malicious_hashes = load_database()

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
