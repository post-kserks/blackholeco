"""
Лента новостей — генерация и загрузка новостей.
"""

import json
import os
import random
from news.news import News
from core.events import check_conditions

# Путь к данным
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")


def load_news_from_file(filename):
    """Загрузить новость из JSON-файла"""
    path = os.path.join(DATA_DIR, "news", filename)

    if not os.path.exists(path):
        return None

    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return News(data)
    except json.JSONDecodeError:
        return None


def load_all_news():
    """Загрузить все новости из папки"""
    news_list = []
    news_dir = os.path.join(DATA_DIR, "news")

    if not os.path.exists(news_dir):
        return news_list

    for filename in os.listdir(news_dir):
        if filename.endswith(".json"):
            news = load_news_from_file(filename)
            if news:
                news_list.append(news)

    return news_list


def get_daily_news(state):
    """
    Получить новости для текущего дня.
    
    Args:
        state: GameState
    
    Returns:
        list[News]: список новостей для показа
    """
    all_news = load_all_news()
    daily_news = []

    for news in all_news:
        # Проверить день
        if news.day is not None and news.day != state.day:
            continue

        # Проверить условия
        if not check_conditions(news.conditions, state):
            continue

        daily_news.append(news)

    # Добавить случайную новость (если нет запланированных)
    if not daily_news and random.random() < 0.3:
        random_news = generate_random_news(state)
        if random_news:
            daily_news.append(random_news)

    return daily_news


def generate_random_news(state):
    """Сгенерировать случайную новость"""
    templates = [
        {
            "title": "Рост цен на топливо",
            "text": "Стоимость топлива выросла на 15% из-за конфликта в секторе Омега.",
            "effects": []
        },
        {
            "title": "Новый торговый маршрут",
            "text": "Открыт безопасный маршрут через астероидный пояс.",
            "effects": []
        },
        {
            "title": "Пиратская активность",
            "text": "В секторе Outer Ring замечена повышенная активность пиратов.",
            "effects": [{"type": "flag", "name": "pirates_active"}]
        },
        {
            "title": "Технологический прорыв",
            "text": "Учёные с Kepler Station сообщают о прорыве в технологии гиперпривода.",
            "effects": []
        },
        {
            "title": "Забастовка докеров",
            "text": "На Титане началась забастовка. Загрузка грузов может занять больше времени.",
            "effects": [{"type": "flag", "name": "titan_strike"}]
        }
    ]

    template = random.choice(templates)
    return News(template)
