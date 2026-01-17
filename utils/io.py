"""
Утилиты для ввода/вывода.
"""

import time
import os


def print_slow(text, delay=0.02):
    """
    Печатать текст с задержкой между символами.
    Создаёт эффект "печатной машинки".
    """
    for char in text:
        print(char, end="", flush=True)
        time.sleep(delay)
    print()


def print_header(text):
    """Напечатать заголовок в рамке"""
    width = len(text) + 4
    print()
    print("╔" + "═" * width + "╗")
    print(f"║  {text}  ║")
    print("╚" + "═" * width + "╝")


def print_box(title, lines):
    """Напечатать текст в рамке"""
    max_len = max(len(title), max(len(line) for line in lines) if lines else 0)
    width = max_len + 4

    print()
    print("╔" + "═" * width + "╗")
    print(f"║  {title.ljust(max_len)}  ║")
    print("╠" + "═" * width + "╣")
    for line in lines:
        print(f"║  {line.ljust(max_len)}  ║")
    print("╚" + "═" * width + "╝")


def clear_screen():
    """Очистить экран терминала"""
    os.system('cls' if os.name == 'nt' else 'clear')


def wait_for_enter(message="[Нажмите Enter для продолжения]"):
    """Ждать нажатия Enter"""
    input(f"\n{message}")


def get_choice(options, prompt="> "):
    """
    Получить выбор пользователя из списка опций.
    
    Args:
        options: список строк
        prompt: приглашение для ввода
    
    Returns:
        int: индекс выбранной опции (0-based)
    """
    for i, option in enumerate(options, 1):
        print(f"{i}. {option}")

    while True:
        try:
            choice = int(input(prompt)) - 1
            if 0 <= choice < len(options):
                return choice
            print("Неверный выбор.")
        except ValueError:
            print("Введите номер.")


def confirm(prompt="Вы уверены?"):
    """Запросить подтверждение (да/нет)"""
    print(f"{prompt} (д/н)")
    answer = input("> ").lower().strip()
    return answer in ["д", "да", "y", "yes"]
