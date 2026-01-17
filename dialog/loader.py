"""
Загрузка JSON-диалогов из файлов.
"""

import json
import os

# Базовый путь к данным
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")


def load_dialog(name):
    """
    Загрузить диалог по имени.
    
    Args:
        name: имя диалога (без расширения, например "intro")
    
    Returns:
        dict: данные диалога или None если не найден
    """
    path = os.path.join(DATA_DIR, "dialogs", f"{name}.json")

    if not os.path.exists(path):
        print(f"[ОШИБКА] Диалог не найден: {path}")
        return None

    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        print(f"[ОШИБКА] Ошибка парсинга JSON: {e}")
        return None


def load_all_dialogs():
    """Загрузить все диалоги из папки"""
    dialogs = {}
    dialogs_dir = os.path.join(DATA_DIR, "dialogs")

    if not os.path.exists(dialogs_dir):
        return dialogs

    for filename in os.listdir(dialogs_dir):
        if filename.endswith(".json"):
            name = filename[:-5]  # Убрать .json
            dialogs[name] = load_dialog(name)

    return dialogs
