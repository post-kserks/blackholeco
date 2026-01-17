"""
Базовый интерфейс мини-игр и примеры реализаций.
"""

import random
from utils.io import print_slow


class MiniGame:
    """Базовый класс мини-игры"""

    def __init__(self, name):
        self.name = name

    def play(self, state):
        """Запустить мини-игру. Возвращает True при успехе."""
        raise NotImplementedError

    def get_reward(self, success, state):
        """Применить награду/штраф"""
        pass


class RepairMiniGame(MiniGame):
    """
    Мини-игра: Починка системы
    Нужно ввести правильную последовательность цифр.
    """

    def __init__(self):
        super().__init__("Починка системы")

    def play(self, state):
        # Генерируем случайный код
        code = "".join([str(random.randint(1, 9)) for _ in range(3)])

        print("\n=== ПОЧИНКА СИСТЕМЫ ===")
        print("Модуль повреждён! Введите код для перезагрузки.")
        print(f"[Подсказка: код состоит из цифр {code[0]}, ? и {code[2]}]")

        attempts = 3
        while attempts > 0:
            user_input = input(f"Код ({attempts} попыток): ").strip()

            if user_input == code:
                print_slow("✓ Система восстановлена!")
                return True
            else:
                attempts -= 1
                if attempts > 0:
                    print(f"✗ Неверный код.")

        print_slow("✗ Ошибка. Модуль повреждён ещё больше.")
        return False


class MeteorFieldMiniGame(MiniGame):
    """
    Мини-игра: Метеоритное поле
    Выбор правильного действия на каждом этапе.
    """

    def __init__(self):
        super().__init__("Метеоритное поле")

    def play(self, state):
        print("\n=== МЕТЕОРИТНОЕ ПОЛЕ ===")
        print_slow("Вы вошли в опасную зону. Множество метеоритов!")

        damage = 0
        stages = 3

        for i in range(stages):
            situation = random.choice(["big", "swarm", "sneak"])

            if situation == "big":
                print(f"\n[Этап {i+1}] Огромный метеорит прямо по курсу!")
                correct = "2"  # Манёвр
            elif situation == "swarm":
                print(f"\n[Этап {i+1}] Рой мелких метеоритов!")
                correct = "1"  # Лететь напролом
            else:
                print(f"\n[Этап {i+1}] Метеорит подкрадывается сбоку!")
                correct = "3"  # Стрелять

            print("1. Лететь напролом")
            print("2. Манёвр уклонения")
            print("3. Стрелять")

            choice = input("> ").strip()

            if choice == correct:
                print_slow("✓ Отличный выбор!")
            else:
                damage += 20
                print_slow(f"✗ Неудачно! Получено {20} урона.")

        if damage == 0:
            print_slow("\n★ Вы прошли поле без единой царапины!")
            return True
        elif damage < 60:
            print_slow(f"\n✓ Вы прошли поле. Общий урон: {damage}")
            return True
        else:
            print_slow(f"\n✗ Критические повреждения! Урон: {damage}")
            return False


class ContrabandMiniGame(MiniGame):
    """
    Мини-игра: Досмотр на контрабанду
    Решение: проверить или игнорировать подозрительный груз.
    """

    def __init__(self):
        super().__init__("Досмотр")

    def play(self, state):
        print("\n=== ДОСМОТР ===")
        print_slow("Патруль Black Hole Co. требует досмотра вашего груза.")

        has_contraband = state.flags.get("carrying_contraband")

        print("\nЧто делать?")
        print("1. Разрешить досмотр")
        print("2. Предложить взятку (500 кредитов)")
        print("3. Попытаться сбежать")

        choice = input("> ").strip()

        if choice == "1":
            if has_contraband:
                print_slow("✗ Контрабанда обнаружена! Вы арестованы.")
                state.change_reputation("BlackHoleCo", -20)
                state.spend_money(1000)  # Штраф
                return False
            else:
                print_slow("✓ Досмотр пройден. Всё чисто.")
                state.change_reputation("BlackHoleCo", 2)
                return True

        elif choice == "2":
            if state.spend_money(500):
                if random.random() < 0.8:  # 80% успех
                    print_slow("✓ Патруль принял взятку. Вы свободны.")
                    return True
                else:
                    print_slow("✗ Они отказались и вызвали подкрепление!")
                    state.change_reputation("BlackHoleCo", -15)
                    return False
            else:
                print_slow("✗ Недостаточно денег!")
                return self.play(state)  # Повторить выбор

        elif choice == "3":
            if random.random() < 0.4:  # 40% успех
                print_slow("✓ Вам удалось скрыться!")
                state.flags.set("wanted_by_bhc")
                return True
            else:
                print_slow("✗ Вас догнали. Арест неизбежен.")
                state.change_reputation("BlackHoleCo", -25)
                return False

        return False


class HackingMiniGame(MiniGame):
    """
    Мини-игра: Взлом системы
    Угадать последовательность символов.
    """

    def __init__(self):
        super().__init__("Взлом")

    def play(self, state):
        print("\n=== ВЗЛОМ СИСТЕМЫ ===")

        target = [random.choice("ABCD") for _ in range(4)]
        attempts = 6

        print("Угадайте 4-символьный код (A, B, C, D)")
        print("После каждой попытки вы узнаете:")
        print("  ● = правильный символ на правильном месте")
        print("  ○ = правильный символ на неправильном месте")

        while attempts > 0:
            guess = input(f"\nПопытка ({attempts}): ").upper().strip()

            if len(guess) != 4 or not all(c in "ABCD" for c in guess):
                print("Введите 4 символа (A, B, C, D)")
                continue

            if list(guess) == target:
                print_slow("✓ ВЗЛОМ УСПЕШЕН!")
                return True

            # Подсчёт подсказок
            exact = sum(g == t for g, t in zip(guess, target))
            wrong_place = 0
            target_copy = target.copy()

            for i, g in enumerate(guess):
                if g != target[i] and g in target_copy:
                    wrong_place += 1
                    target_copy.remove(g)

            print(f"{'●' * exact}{'○' * wrong_place}")
            attempts -= 1

        print_slow(f"✗ Взлом провален. Код был: {''.join(target)}")
        return False
