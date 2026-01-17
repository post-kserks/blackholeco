"""
Генератор заказов — создаёт случайные заказы на основе состояния игры.
"""

import random
from orders.order import Order


# Базовые данные для генерации
CARGO_TYPES = [
    "Медикаменты",
    "Электроника",
    "Продовольствие",
    "Топливо",
    "Запчасти",
    "Оружие",
    "Редкие металлы",
    "Научное оборудование",
    "Колонисты",
    "VIP-пассажир"
]

PLANETS = [
    "Station Alpha",
    "Марс-3",
    "Титан",
    "Europa Prime",
    "Вода",
    "Меза",
    "Новая Земля",
    "Kepler Station",
    "Outer Ring"
]

FACTIONS = ["BlackHoleCo", "Union", "Syndicate", None]

CONTRABAND_ITEMS = ["Оружие", "Контрабанда", "Редкие металлы", "Наркотики"]


def generate_order(state):
    """
    Сгенерировать случайный заказ.
    
    Args:
        state: GameState — влияет на сложность и награды
    
    Returns:
        Order или None
    """
    # Шанс что заказов нет
    if random.random() < 0.1:
        return None

    # Выбрать груз
    cargo = random.choice(CARGO_TYPES)

    # Выбрать пункт назначения (не текущая планета)
    available_planets = [p for p in PLANETS if p != state.current_planet]

    # Исключить опасные зоны если игрок осторожен
    for planet in available_planets[:]:
        if state.flags.get(f"dead_zone_{planet}"):
            if random.random() < 0.7:  # 70% шанс не предлагать опасный маршрут
                available_planets.remove(planet)

    if not available_planets:
        return None

    destination = random.choice(available_planets)

    # Рассчитать награду (зависит от дня и репутации)
    base_reward = random.randint(100, 500)
    day_multiplier = 1 + (state.day * 0.05)  # +5% за каждый день
    reward = int(base_reward * day_multiplier)

    # Дедлайн (опционально)
    deadline = None
    if random.random() < 0.3:  # 30% заказов с дедлайном
        deadline = state.day + random.randint(2, 5)
        reward = int(reward * 1.5)  # +50% за срочность

    # Фракция
    faction = random.choice(FACTIONS)

    is_contraband = cargo in CONTRABAND_ITEMS
    
    return Order(
        cargo=cargo,
        origin=state.current_planet,
        destination=destination,
        reward=reward,
        deadline=deadline,
        faction=faction,
        is_contraband=is_contraband
    )


def generate_special_order(state, order_type):
    """
    Сгенерировать специальный сюжетный заказ.
    
    Args:
        state: GameState
        order_type: тип заказа ("contraband", "rescue", "secret")
    """
    if order_type == "contraband":
        return Order(
            cargo="Контрабанда",
            origin=state.current_planet,
            destination="Outer Ring",
            reward=2000,
            faction="Syndicate",
            is_contraband=True
        )

    elif order_type == "rescue":
        return Order(
            cargo="Спасательная миссия",
            origin=state.current_planet,
            destination="X-17",
            reward=1500,
            deadline=state.day + 2,
            faction="Union"
        )

    elif order_type == "secret":
        return Order(
            cargo="Секретный груз",
            origin=state.current_planet,
            destination="Kepler Station",
            reward=3000,
            faction="BlackHoleCo"
        )

    return None
