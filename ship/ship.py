"""
Корабль игрока — управление модулями и состоянием.
"""

from ship.modules import EngineModule, ShieldModule, CargoModule, ScannerModule


class Ship:
    """Космический корабль игрока"""

    def __init__(self, name="Стандартный грузовик"):
        self.name = name

        # Модули корабля
        self.engine = EngineModule()
        self.shield = ShieldModule()
        self.cargo = CargoModule()
        self.scanner = ScannerModule()

        # Топливо
        self.fuel = 100
        self.max_fuel = 100

    def get_all_modules(self):
        """Получить список всех модулей"""
        return [self.engine, self.shield, self.cargo, self.scanner]

    def take_damage(self, amount):
        """
        Получить урон. Щит поглощает часть урона.
        Возвращает реальный урон.
        """
        if self.shield.is_broken:
            real_damage = amount
        else:
            absorbed = int(amount * self.shield.protection)
            real_damage = amount - absorbed
            self.shield.damage(absorbed // 2)  # Щит тоже получает урон

        # Случайный модуль получает урон
        import random
        modules = [m for m in self.get_all_modules() if not m.is_broken]
        if modules:
            target = random.choice(modules)
            target.damage(real_damage)

        return real_damage

    def use_fuel(self, amount):
        """Использовать топливо"""
        if self.fuel >= amount:
            self.fuel -= amount
            return True
        return False

    def refuel(self, amount=None):
        """Заправить корабль"""
        if amount is None:
            self.fuel = self.max_fuel
        else:
            self.fuel = min(self.max_fuel, self.fuel + amount)

    def can_carry(self, items_count):
        """Проверить, можно ли взять груз"""
        return items_count <= self.cargo.capacity

    def repair_all(self):
        """Починить все модули"""
        for module in self.get_all_modules():
            module.repair()

    def get_status(self):
        """Получить полный статус корабля"""
        lines = [
            f"=== {self.name} ===",
            f"Топливо: {self.fuel}/{self.max_fuel}",
            "",
            "Модули:"
        ]
        for module in self.get_all_modules():
            lines.append(f"  {module.get_status()}")
        return "\n".join(lines)

    def show_status(self):
        """Показать статус корабля"""
        print(self.get_status())

    def to_dict(self):
        """Для сохранения"""
        return {
            "name": self.name,
            "fuel": self.fuel,
            "max_fuel": self.max_fuel,
            "engine": self.engine.to_dict(),
            "shield": self.shield.to_dict(),
            "cargo": self.cargo.to_dict(),
            "scanner": self.scanner.to_dict()
        }

    @classmethod
    def from_dict(cls, data):
        """Для загрузки"""
        from ship.modules import Module
        ship = cls(data["name"])
        ship.fuel = data["fuel"]
        ship.max_fuel = data["max_fuel"]
        ship.engine = Module.from_dict(data["engine"])
        ship.shield = Module.from_dict(data["shield"])
        ship.cargo = Module.from_dict(data["cargo"])
        ship.scanner = Module.from_dict(data["scanner"])
        return ship
