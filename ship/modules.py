"""
Модули корабля — компоненты, которые можно улучшать и ремонтировать.
"""


class Module:
    """Базовый модуль корабля"""

    def __init__(self, name, level=1, max_health=100):
        self.name = name
        self.level = level
        self.max_health = max_health
        self.health = max_health
        self.is_broken = False

    def damage(self, amount):
        """Нанести урон модулю"""
        self.health = max(0, self.health - amount)
        if self.health == 0:
            self.is_broken = True

    def repair(self, amount=None):
        """Починить модуль"""
        if amount is None:
            self.health = self.max_health
        else:
            self.health = min(self.max_health, self.health + amount)
        self.is_broken = False

    def upgrade(self):
        """Улучшить модуль"""
        self.level += 1
        self.max_health += 20
        self.health = self.max_health

    def get_status(self):
        """Получить статус модуля"""
        status = "СЛОМАН" if self.is_broken else f"{self.health}/{self.max_health}"
        return f"{self.name} (Ур.{self.level}): {status}"

    def to_dict(self):
        return {
            "name": self.name,
            "level": self.level,
            "max_health": self.max_health,
            "health": self.health,
            "is_broken": self.is_broken
        }

    @classmethod
    def from_dict(cls, data):
        module = cls(data["name"], data["level"], data["max_health"])
        module.health = data["health"]
        module.is_broken = data["is_broken"]
        return module


class EngineModule(Module):
    """Двигатель — влияет на скорость перемещения"""

    def __init__(self, level=1):
        super().__init__("Двигатель", level)
        self.speed = 1.0 + (level * 0.2)

    def upgrade(self):
        super().upgrade()
        self.speed = 1.0 + (self.level * 0.2)


class ShieldModule(Module):
    """Щит — защита от урона"""

    def __init__(self, level=1):
        super().__init__("Щит", level)
        self.protection = 0.1 * level  # 10% защиты за уровень

    def upgrade(self):
        super().upgrade()
        self.protection = 0.1 * self.level


class CargoModule(Module):
    """Грузовой отсек — влияет на максимальный груз"""

    def __init__(self, level=1):
        super().__init__("Грузовой отсек", level)
        self.capacity = 5 + (level * 5)  # Базовая вместимость 10

    def upgrade(self):
        super().upgrade()
        self.capacity = 5 + (self.level * 5)


class ScannerModule(Module):
    """Сканер — обнаружение опасностей и ресурсов"""

    def __init__(self, level=1):
        super().__init__("Сканер", level)
        self.range = level  # Дальность сканирования

    def upgrade(self):
        super().upgrade()
        self.range = self.level
