"""
Главный игровой цикл.
"""

from core.state import GameState
from dialog.engine import run_dialog
from dialog.loader import load_dialog
from news.feed import get_daily_news
from orders.generator import generate_order
from utils.io import print_slow, print_header, clear_screen
from utils.save_load import save_game
from core.map import GALAXY_GRAPH, get_path, get_max_reachable_path
from core.encounters import check_police_encounter
import random


def start_game():
    """Начать новую игру"""
    clear_screen()
    state = GameState()

    # Запустить вступительный диалог
    intro = load_dialog("intro")
    if intro:
        run_dialog(intro, state)

    if not state.alive:
        print_slow("\n[ИГРА ОКОНЧЕНА]")
        return

    # Показать приветствие на корабле
    welcome = load_dialog("welcome")
    if welcome:
        run_dialog(welcome, state)

    # Основной игровой цикл
    game_loop(state)


def game_loop(state):
    """Основной цикл игры"""
    while state.alive:
        print_header(f"День {state.day} | {state.current_planet} | Кредиты: {state.money}")

        # Показать меню дня
        print("\nЧто вы хотите сделать?")
        print("1. Проверить новости")
        print("2. Взять заказ")
        print("3. Лететь на планету")
        print("4. Управление кораблём")
        print("5. Статус")
        print("6. Завершить день")
        print("7. Сохранить игру")
        print("8. Карта галактики")
        print("9. Проложить маршрут")
        print("10. Выйти в меню")

        choice = input("> ").strip()

        if choice == "1":
            show_news(state)
        elif choice == "2":
            take_order(state)
        elif choice == "3":
            travel_to_planet(state)
        elif choice == "4":
            manage_ship(state)
        elif choice == "5":
            show_status(state)
        elif choice == "6":
            end_day(state)
        elif choice == "7":
            save_game(state)
            print_slow("Игра сохранена.")
        elif choice == "8":
            show_map(state)
        elif choice == "8":
            show_map(state)
        elif choice == "9":
            plan_route(state)
        elif choice == "10":
            print_slow("Возврат в меню...")
            break
        else:
            print("Неверный ввод.")


def show_news(state):
    """Показать новости дня"""
    news_list = get_daily_news(state)

    if not news_list:
        print_slow("\nНовостей нет.")
        return

    for news in news_list:
        news.show(state)

    input("\n[Нажмите Enter для продолжения]")


def take_order(state):
    """Взять новый заказ"""
    if state.current_order:
        print_slow("\nУ вас уже есть активный заказ!")
        print(f"Доставить груз на {state.current_order.destination}")
        return

    # Сюжетный квест: Робот 001 (День 1-2)
    if state.day <= 2 and not state.flags.get("heard_about_robot_001") and not state.flags.get("warned_about_water"):
        quest_dialog = load_dialog("client_water_001")
        if quest_dialog:
            run_dialog(quest_dialog, state)
            return

    order = generate_order(state)
    if order:
        # Установить заказ как ожидающий принятия
        state.pending_order = order
        
        # Выбрать шаблон диалога
        # Если фракция Black Hole Co., то скорее всего корпоративный клиент
        if order.faction == "Black Hole Co.":
            template_id = "client_type_corporate"
        elif order.faction == "Syndicate":
             template_id = "client_type_rude"
        else:
             template_id = random.choice(["client_type_standard", "client_type_rude"])

        client_dialog = load_dialog(template_id)
        if client_dialog:
             run_dialog(client_dialog, state)
    else:
        print_slow("\nНет доступных заказов.")


def travel_to_planet(state):
    """Полёт на другую планету"""
    
    print("\n=== НАВИГАЦИЯ ===")
    print(f"Текущее положение: {state.current_planet}")
    print(f"Топливо: {state.ship.fuel}/{state.ship.max_fuel}")
    print(f"Очки действий (AP): {state.action_points}")

    # Показать доступные планеты (все, кроме текущей)
    available = [p for p in GALAXY_GRAPH.keys() if p != state.current_planet]
    
    for i, planet in enumerate(available, 1):
        # Проверка пути и дистанции
        path, dist = get_path(state.current_planet, planet)
        if path:
            print(f"{i}. {planet} (Дистанция: {dist})")
        else:
             print(f"{i}. {planet} [НЕДОСТУПНО]")

    print(f"{len(available) + 1}. Отмена")

    try:
        choice = int(input("> ").strip())
        if choice == len(available) + 1:
            return

        if 1 <= choice <= len(available):
            destination = available[choice - 1]
            perform_travel(state, destination)
    
    except ValueError:
        print("Неверный ввод.")


def perform_travel(state, destination):
    """Выполнить перелёт к пункту назначения"""
    # Рассчет маршрута
    path, dist = get_path(state.current_planet, destination)
    if not path:
        print_slow("Нет доступного маршрута до этой планеты.")
        return

    # Рассчет затрат
    engine_level = state.ship.engine.level
    fuel_cost = int(dist * 0.5 * (1 + (engine_level * 0.2)))
    ap_cost = int(25 / engine_level)
    
    # Проверка ресурсов
    if state.action_points < ap_cost:
        print_slow(f"\nНедостаточно очков действий! Нужно {ap_cost}, у вас {state.action_points}.")
        print_slow("Завершите день, чтобы восстановить силы.")
        return

    max_fuel = state.ship.fuel
    # Если топлива не хватает на полный путь
    if fuel_cost > max_fuel:
         reachable_path, reachable_dist, reached = get_max_reachable_path(state.current_planet, destination, max_fuel / (0.5 * (1 + (engine_level * 0.2))))
         print_slow(f"\n⚠️ ВНИМАНИЕ: Недостаточно топлива для полного маршрута!")
         print(f"Требуется: {fuel_cost}, у вас: {state.ship.fuel}")
         print("Вы остановитесь на полпути.")

    print(f"\nМаршрут: {' -> '.join(path)}")
    print(f"Затраты: {fuel_cost} топлива, {ap_cost} AP")
    print("1. Начать полёт")
    print("2. Отмена")
    
    if input("> ").strip() != "1":
        return

    # Начало полёта
    state.action_points -= ap_cost
    current_node_index = 0
    
    print_slow("\nСистемы корабля: НОРМА.")
    print_slow("Двигатели: ЗАПУСК...")
    
    for i in range(len(path) - 1):
        start_node = path[i]
        next_node = path[i+1]
        
        segment_dist = GALAXY_GRAPH[start_node][next_node]
        segment_fuel = int(segment_dist * 0.5 * (1 + (engine_level * 0.2)))

        if not state.ship.use_fuel(segment_fuel):
            print_slow("\n⚠️ ТОПЛИВО НА ИСХОДЕ!")
            print_slow("Двигатели глохнут...")
            state.ship.fuel = 0
            state.current_planet = start_node # Остаемся на предыдущей точке
            print_slow(f"Аварийная остановка в системе {state.current_planet}.")
            return

        print_slow(f"Перелёт: {start_node} -> {next_node}...", delay=0.5)
        
        # Проверка полиции
        if not check_police_encounter(state):
             # Если полёт прерван (тюрьма/смерть) - стоп
             return 
             
        state.current_planet = next_node

        # Проверка опасных зон (после прибытия)
        dead_zone_check(state, next_node)
        if not state.alive:
            return

    print_slow(f"\nВы прибыли на {state.current_planet}.")
    
    # Проверка доставки
    if state.current_order and state.current_order.destination == state.current_planet:
         # В диалоге будет кнопка "Завершить заказ"
         template_id = random.choice([
             "recipient_standard", 
             "recipient_rude", 
             "recipient_grateful", 
             "recipient_foreigner"
         ])
         
         recipient_dialog = load_dialog(template_id)
         if recipient_dialog:
              run_dialog(recipient_dialog, state)


def dead_zone_check(state, planet):
    """Проверка на смерть в опасной зоне"""
    if planet == "Меза" and state.flags.get("meza_invasion") and not state.flags.get("dead_zone_Меза_cleared"): # flag cleared checking assumption
         # Assuming death unless specific condition... user logic was simple previously
         if state.flags.get("dead_zone_Меза"):
             print_slow("\nВнезапно ваш корабль окружают неизвестные объекты...")
             state.die("Уничтожен пришельцами в системе Меза")

    if planet == "Вода" and state.flags.get("voda_alert_1995"):
         if state.flags.get("dead_zone_Вода"):
             print_slow("\nГигантский робот замечает ваш корабль...")
             state.die("Уничтожен во время инцидента на планете Вода")


def manage_ship(state):
    """Управление кораблём"""
    print_slow("\n[Функция в разработке]")
    # TODO: Добавить управление модулями корабля


def show_status(state):
    """Показать статус игрока"""
    print("\n=== СТАТУС ===")
    print(f"День: {state.day}")
    print(f"Кредиты: {state.money}")
    print(f"Планета: {state.current_planet}")
    print("\nРепутация:")
    for faction, rep in state.reputation.items():
        print(f"  {faction}: {rep}")

    if state.cargo:
        print("\nГруз:")
        for item in state.cargo:
            print(f"  - {item}")

    input("\n[Нажмите Enter для продолжения]")



def show_map(state):
    """Показать карту галактики"""
    print("\n=== КАРТА ГАЛАКТИКИ ===")
    for planet, neighbors in GALAXY_GRAPH.items():
        prefix = "📍 " if planet == state.current_planet else "   "
        print(f"{prefix}{planet}")
        for neighbor, dist in neighbors.items():
             print(f"      -> {neighbor}: {dist}")
    input("\n[Нажмите Enter для продолжения]")


def plan_route(state):
    """Интерактивный планировщик маршрутов"""
    print("\n=== ПРОЛОЖИТЬ МАРШРУТ ===")
    print("Куда летим?")
    
    available = [p for p in GALAXY_GRAPH.keys() if p != state.current_planet]
    for i, planet in enumerate(available, 1):
        print(f"{i}. {planet}")
    print(f"{len(available) + 1}. Отмена")

    try:
        choice = int(input("> ").strip())
        if choice == len(available) + 1:
            return

        if 1 <= choice <= len(available):
            destination = available[choice - 1]
            path, dist = get_path(state.current_planet, destination)
            
            if not path:
                print_slow("Нет доступного маршрута.")
                return

            # Расчет стоимости
            engine_level = state.ship.engine.level
            fuel_cost = int(dist * 0.5 * (1 + (engine_level * 0.2)))
            ap_cost = int(len(path) - 1) * int(25 / engine_level) # Примерный расчет по сегментам?
            # В travel_to_planet ap_cost считается за *перелет*. 
            # Но подождите, в travel_to_planet ap_cost считается ОДИН раз за весь вызов travel_to_planet.
            # А travel_to_planet летит по сегментам.
            # Давайте посмотрим travel_to_planet.
            # Там ap_cost = 25 / level. И это вычитается ОДИН раз.
            # Значит и здесь должно быть так же.
            ap_cost = int(25 / engine_level)

            days = 1
            if ap_cost > 100: 
                # Если стоимость больше 100 за раз (невозможно при нынешнем балансе),
                # но если бы была...
                days = (ap_cost // 100) + 1
            
            # А если мы хотим показать, что при полете на дальние дистанции
            # мы можем потратить несколько дней?
            # Сейчас travel_to_planet делает все за один раз.
            # Если топлива не хватает, мы останавливаемся.
            # Пользователь просит показать "Время: 3 дня".
            # Это подразумевает, что долгий путь занимает время.
            # Пока у нас мгновенное перемещение, но давайте симулировать,
            # что если AP > state.action_points, нам придется "ждать".
            # Но фактически сейчас мы тратим 1 "тик" AP.
            # Давайте пока оставим "Время: <1 дня" или просто "Время: Мгновенно" 
            # пока не переделаем систему времени.
            # А, пользователь просит "Время: 3 дня" для Outer Ring.
            # Outer Ring далеко.
            # Похоже пользователь хочет механику длительных путешествий?
            # Или это просто "флейвор"?
            # Давайте сделаем флейвор текст "Примерное время в пути".
            estimated_days = max(1, int(dist / 300)) # Грубая прикидка
            
            print(f"\nОптимальный маршрут:")
            print(f"{' -> '.join(path)}")
            print(f"Стоимость: {fuel_cost} топлива") # Уберем "1000", оставим топливо
            print(f"Энергия: {ap_cost} AP")
            print(f"Примерное время: {estimated_days} дн.")
            
            print("\n[1] Лететь")
            print("[2] Отменить")
            
            if input("> ").strip() == "1":
                # Запускаем существующую функцию путешествия
                # Но нам нужно передать выбор... 
                # travel_to_planet сама спрашивает ввод.
                # Мы не можем просто вызвать её и заставить лететь туда.
                # Нам придется дублировать логику или рефакторить travel_to_planet.
                # Для простоты сейчас, мы можем просто сказать "Используйте меню полета".
                # НО пользователь просил "[1] Лететь".
                # Значит нам нужно уметь запускать полет с параметрами.
                # Рефакторинг travel_to_planet чтобы принимать destination аргумент.
                # Рефакторинг travel_to_planet чтобы принимать destination аргумент.
                perform_travel(state, destination)

    except ValueError:
        print("Неверный ввод.")


def end_day(state):
    """Завершить день"""
    state.next_day()
    print_slow(f"\nНаступил день {state.day}...")

    # Здесь можно добавить случайные события
    # check_random_events(state)
