"""
Новость — событие, влияющее на мир игры.
"""

from core.events import apply_effects
from utils.io import print_slow


class News:
    """Класс новости"""

    def __init__(self, data):
        self.title = data.get("title", "Без заголовка")
        self.text = data.get("text", "")
        self.effects = data.get("effects", [])
        self.day = data.get("day")  # На какой день показывать
        self.conditions = data.get("conditions", [])  # Условия показа

    def show(self, state):
        """Показать новость и применить эффекты"""
        print(f"\n╔{'═' * 40}╗")
        print(f"║ 📰 НОВОСТИ")
        print(f"╠{'═' * 40}╣")
        print(f"║ {self.title}")
        print(f"╚{'═' * 40}╝")
        print_slow(self.text)

        # Применить эффекты
        apply_effects(self.effects, state)

    def to_dict(self):
        return {
            "title": self.title,
            "text": self.text,
            "effects": self.effects,
            "day": self.day,
            "conditions": self.conditions
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data)
