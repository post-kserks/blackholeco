"""
Заказ — задание на доставку груза.
"""


class Order:
    """Класс заказа на доставку"""

    def __init__(self, cargo, origin, destination, reward, deadline=None, faction=None, is_contraband=False):
        self.cargo = cargo  # Название груза
        self.origin = origin  # Откуда
        self.destination = destination  # Куда
        self.reward = reward  # Награда в кредитах
        self.deadline = deadline  # Дедлайн (день) или None
        self.faction = faction  # От какой фракции заказ
        self.is_contraband = is_contraband # Является ли груз контрабандой

        self.is_completed = False
        self.is_failed = False

    def show(self):
        """Показать информацию о заказе"""
        print("\n=== ЗАКАЗ ===")
        print(f"Груз: {self.cargo}")
        if self.is_contraband:
             print("⚠️ [НЕЛЕГАЛЬНЫЙ ГРУЗ]")
        print(f"Откуда: {self.origin}")
        print(f"Куда: {self.destination}")
        print(f"Награда: {self.reward} кредитов")

        if self.deadline:
            print(f"Дедлайн: День {self.deadline}")

        if self.faction:
            print(f"Заказчик: {self.faction}")

    def check_deadline(self, current_day):
        """Проверить, просрочен ли заказ"""
        if self.deadline and current_day > self.deadline:
            self.is_failed = True
            return False
        return True

    def complete(self, state):
        """Завершить заказ"""
        self.is_completed = True
        state.add_money(self.reward)

        if self.faction:
            state.change_reputation(self.faction, 5)

        state.completed_orders.append({
            "cargo": self.cargo,
            "destination": self.destination,
            "reward": self.reward
        })
        state.current_order = None

    def fail(self, state):
        """Провалить заказ"""
        self.is_failed = True

        if self.faction:
            state.change_reputation(self.faction, -10)

        state.current_order = None

    def to_dict(self):
        return {
            "cargo": self.cargo,
            "origin": self.origin,
            "destination": self.destination,
            "reward": self.reward,
            "deadline": self.deadline,
            "faction": self.faction,
            "is_contraband": self.is_contraband
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            cargo=data["cargo"],
            origin=data["origin"],
            destination=data["destination"],
            reward=data["reward"],
            deadline=data.get("deadline"),
            faction=data.get("faction"),
            is_contraband=data.get("is_contraband", False)
        )
