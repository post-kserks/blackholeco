"""
Универсальный загрузчик JSON-файлов.
"""

import json
import os

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")


def load_json(path):
    """
    Загрузить JSON-файл.
    
    Args:
        path: путь к файлу (относительно data/ или абсолютный)
    
    Returns:
        dict или list или None
    """
    # Если путь относительный — добавить DATA_DIR
    if not os.path.isabs(path):
        path = os.path.join(DATA_DIR, path)

    if not os.path.exists(path):
        print(f"[ОШИБКА] Файл не найден: {path}")
        return None

    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        print(f"[ОШИБКА] Ошибка парсинга JSON: {e}")
        return None


def save_json(data, path):
    """
    Сохранить данные в JSON-файл.
    
    Args:
        data: данные для сохранения
        path: путь к файлу
    
    Returns:
        bool: успех
    """
    # Создать директорию если нужно
    dir_path = os.path.dirname(path)
    if dir_path and not os.path.exists(dir_path):
        os.makedirs(dir_path)

    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"[ОШИБКА] Не удалось сохранить: {e}")
        return False


def list_json_files(subdir):
    """
    Получить список JSON-файлов в поддиректории data/.
    
    Args:
        subdir: поддиректория (например "dialogs", "news")
    
    Returns:
        list[str]: список имён файлов без расширения
    """
    path = os.path.join(DATA_DIR, subdir)

    if not os.path.exists(path):
        return []

    files = []
    for filename in os.listdir(path):
        if filename.endswith(".json"):
            files.append(filename[:-5])  # Убрать .json

    return files
