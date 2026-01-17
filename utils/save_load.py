"""
Сохранение и загрузка игры.
"""

import json
import os

SAVE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "saves")
SAVE_FILE = os.path.join(SAVE_DIR, "savegame.json")


def ensure_save_dir():
    """Создать папку для сохранений если её нет"""
    if not os.path.exists(SAVE_DIR):
        os.makedirs(SAVE_DIR)


def save_game(state, filename=None):
    """
    Сохранить игру в файл.
    
    Args:
        state: GameState
        filename: имя файла (опционально)
    """
    ensure_save_dir()

    filepath = filename if filename else SAVE_FILE

    data = state.to_dict()

    try:
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"[ОШИБКА] Не удалось сохранить игру: {e}")
        return False


def load_game(filename=None):
    """
    Загрузить игру из файла.
    
    Args:
        filename: имя файла (опционально)
    
    Returns:
        GameState или None
    """
    filepath = filename if filename else SAVE_FILE

    if not os.path.exists(filepath):
        print("[ОШИБКА] Файл сохранения не найден.")
        return None

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

        from core.state import GameState
        state = GameState()
        state.from_dict(data)

        print("Игра загружена!")

        # Запустить игровой цикл
        from core.game import game_loop
        game_loop(state)

        return state

    except json.JSONDecodeError as e:
        print(f"[ОШИБКА] Повреждённый файл сохранения: {e}")
        return None
    except Exception as e:
        print(f"[ОШИБКА] Не удалось загрузить игру: {e}")
        return None


def list_saves():
    """Получить список сохранений"""
    ensure_save_dir()

    saves = []
    for filename in os.listdir(SAVE_DIR):
        if filename.endswith(".json"):
            filepath = os.path.join(SAVE_DIR, filename)
            saves.append({
                "name": filename,
                "path": filepath,
                "modified": os.path.getmtime(filepath)
            })

    return sorted(saves, key=lambda x: x["modified"], reverse=True)


def delete_save(filename):
    """Удалить сохранение"""
    filepath = os.path.join(SAVE_DIR, filename)
    if os.path.exists(filepath):
        os.remove(filepath)
        return True
    return False
