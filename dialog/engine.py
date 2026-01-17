"""
Диалоговый движок — обработка JSON-диалогов с выборами и эффектами.
"""

from utils.io import print_slow
from core.events import apply_effects, check_conditions


def run_dialog(dialog_data, state, start_node="start"):
    """
    Запустить диалог.
    
    Args:
        dialog_data: dict с узлами диалога
        state: GameState
        start_node: начальный узел (по умолчанию "start")
    """
    if not dialog_data:
        return

    node_id = start_node
    
    # Поддержка новой структуры (meta + nodes)
    if "nodes" in dialog_data:
        nodes = dialog_data["nodes"]
        # Если start_node не передан явно (по умолчанию "start"),
        # пробуем взять стартовый узел из поля "start" в JSON
        if start_node == "start" and "start" in dialog_data:
            node_id = dialog_data["start"]
    else:
        # Старый формат (плоский словарь)
        nodes = dialog_data

    node = nodes.get(node_id)
    
    # Получить имя говорящего из метаданных, если есть
    default_speaker = dialog_data.get("meta", {}).get("character", "")

    while node:
        # Показать текст узла
        text = node.get("text", "")
        
        # Подстановка переменных из pending_order
        if state.pending_order:
            order = state.pending_order
            replacements = {
                "{cargo}": str(order.cargo),
                "{destination}": str(order.destination),
                "{reward}": str(order.reward),
                "{faction}": str(order.faction) if order.faction else "Частное лицо"
            }
            for key, val in replacements.items():
                text = text.replace(key, val)

        # Если у узла нет speaker, используем из метаданных
        speaker = node.get("speaker", default_speaker)

        if speaker:
            print_slow(f"\n[{speaker}]: {text}")
        else:
            print_slow(f"\n{text}")

        # Если нет выборов — конец диалога
        if "choices" not in node or not node["choices"]:
            break

        # Фильтровать выборы по условиям
        available_choices = []
        for choice in node["choices"]:
            conditions = choice.get("conditions", [])
            if check_conditions(conditions, state):
                available_choices.append(choice)

        if not available_choices:
            # Нет доступных выборов — конец
            break

        # Показать доступные выборы
        print()
        for i, choice in enumerate(available_choices, 1):
            print_slow(f"{i}. {choice['text']}", delay=0.015)

        # Получить выбор игрока
        while True:
            try:
                user_input = input("> ").strip()
                idx = int(user_input) - 1
                if 0 <= idx < len(available_choices):
                    break
                print("Неверный выбор.")
            except ValueError:
                print("Введите номер.")

        selected = available_choices[idx]

        # Применить эффекты выбора
        effects = selected.get("effects", [])
        apply_effects(effects, state)

        # Перейти к следующему узлу
        next_node = selected.get("next")
        if next_node is None:
            break

        node = nodes.get(next_node)
        if node is None:
            print(f"[ОШИБКА] Узел не найден: {next_node}")
            break


def run_simple_dialog(lines, speaker=None):
    """
    Показать простой линейный диалог (без выборов).
    
    Args:
        lines: список строк текста
        speaker: имя говорящего (опционально)
    """
    for line in lines:
        if speaker:
            print_slow(f"\n[{speaker}]: {line}")
        else:
            print_slow(f"\n{line}")
    
    input("\n[Нажмите Enter для продолжения]")
