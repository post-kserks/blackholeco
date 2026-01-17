"""
Сюжетные флаги — сердце ветвлений.
Используются в диалогах, новостях, заказах, финалах.
"""


class Flags:
    def __init__(self):
        self.flags = {}

    def set(self, name, value=True):
        """Установить флаг"""
        self.flags[name] = value

    def get(self, name):
        """Получить значение флага (False по умолчанию)"""
        return self.flags.get(name, False)

    def has(self, name):
        """Проверить, установлен ли флаг"""
        return name in self.flags and self.flags[name]

    def remove(self, name):
        """Удалить флаг"""
        if name in self.flags:
            del self.flags[name]

    def all(self):
        """Вернуть все флаги"""
        return self.flags.copy()

    def to_dict(self):
        """Для сохранения"""
        return self.flags.copy()

    def from_dict(self, data):
        """Для загрузки"""
        self.flags = data.copy()
