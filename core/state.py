"""
Состояние игры — хранит все данные о прогрессе игрока.
"""

from core.flags import Flags
from ship.ship import Ship


class GameState:
    def __init__(self):
        self.day = 1
        self.money = 1000
        self.alive = True
        self.current_planet = "Station Alpha"
        self.action_points = 100 # Очки действий на день

        # Репутация у разных фракций
        self.reputation = {
            "BlackHoleCo": 0,
            "Union": 0,
            "Syndicate": 0
        }

        # Сюжетные флаги
        self.flags = Flags()

        # Текущий заказ (если есть)
        self.current_order = None
        self.pending_order = None # Временное хранение заказа до принятия

        # История выполненных заказов
        self.completed_orders = []

        # Инвентарь (груз)
        self.cargo = []
        
        # Корабль игрока
        self.ship = Ship()

    def next_day(self):
        """Перейти к следующему дню"""
        self.day += 1
        self.action_points = 100
        self.ship.refuel() # Восстановить топливо

    def add_money(self, amount):
        """Добавить деньги"""
        self.money += amount

    def spend_money(self, amount):
        """Потратить деньги"""
        if self.money >= amount:
            self.money -= amount
            return True
        return False

    def change_reputation(self, faction, amount):
        """Изменить репутацию у фракции"""
        if faction in self.reputation:
            self.reputation[faction] += amount

    def get_reputation(self, faction):
        """Получить репутацию у фракции"""
        return self.reputation.get(faction, 0)

    def die(self, reason="Неизвестная причина"):
        """Игрок погиб"""
        self.alive = False
        self.death_reason = reason

    def to_dict(self):
        """Для сохранения игры"""
        return {
            "day": self.day,
            "money": self.money,
            "alive": self.alive,
            "current_planet": self.current_planet,
            "reputation": self.reputation.copy(),
            "flags": self.flags.to_dict(),
            "completed_orders": self.completed_orders.copy(),
            "completed_orders": self.completed_orders.copy(),
            "cargo": self.cargo.copy(),
            "ship": self.ship.to_dict()
        }

    def from_dict(self, data):
        """Для загрузки игры"""
        self.day = data.get("day", 1)
        self.money = data.get("money", 1000)
        self.alive = data.get("alive", True)
        self.current_planet = data.get("current_planet", "Station Alpha")
        self.reputation = data.get("reputation", {
            "BlackHoleCo": 0,
            "Union": 0,
            "Syndicate": 0
        })
        self.flags.from_dict(data.get("flags", {}))
        self.completed_orders = data.get("completed_orders", [])
        self.cargo = data.get("cargo", [])
        if "ship" in data:
            self.ship = Ship.from_dict(data["ship"])
        else:
            self.ship = Ship()
