"""
Карта Галактики и навигация.
"""

# Граф Галактики
# Ключ: планета
# Значение: словарь {сосед: расстояние}
# Расстояния условные (км / 1000 или просто единицы топлива)

GALAXY_GRAPH = {
    "Station Alpha": {
        "Марс-3": 85,
        "Титан": 85,
        "Вода": 85,
        "Новая Земля": 120
    },
    "Марс-3": {
        "Station Alpha": 85,
        "Europa Prime": 200,
        "Вода": 100
    },
    "Титан": {
        "Station Alpha": 85,
        "Europa Prime": 150,
        "Kepler Station": 250
    },
    "Europa Prime": {
        "Марс-3": 400,
        "Титан": 300,
        "Меза": 250,
        "Outer Ring": 700
    },
    "Вода": {
        "Station Alpha": 85,
        "Марс-3": 100,
        "Меза": 150
    },
    "Меза": {
        "Europa Prime": 250,
        "Вода": 300,
        "Kepler Station": 450
    },
    "Новая Земля": {
        "Station Alpha": 120,
        "Kepler Station": 150
    },
    "Kepler Station": {
        "Новая Земля": 150,
        "Титан": 350,
        "Меза": 350,
        "Outer Ring": 500
    },
    "Outer Ring": {
        "Europa Prime": 700,
        "Kepler Station": 600
    }
}


def get_path(start, end, max_dist=None):
    """
    Найти кратчайший путь от start до end.
    Использует алгоритм Дейкстры.
    
    Args:
        start: Начальная планета
        end: Конечная планета
        max_dist: (не используется в базовом поиске, но может быть полезен)
        
    Returns:
        (path, distance): Список планет и общая дистанция. 
                          Если пути нет, возвращает (None, infinity).
    """
    if start not in GALAXY_GRAPH or end not in GALAXY_GRAPH:
        return None, float('inf')

    # Инициализация
    distances = {node: float('inf') for node in GALAXY_GRAPH}
    distances[start] = 0
    previous_nodes = {node: None for node in GALAXY_GRAPH}
    unvisited = list(GALAXY_GRAPH.keys())

    while unvisited:
        # Выбрать узел с наименьшим расстоянием
        current_node = min(unvisited, key=lambda node: distances[node])
        
        if distances[current_node] == float('inf'):
            break # Остальные узлы недостижимы
            
        if current_node == end:
            break
            
        unvisited.remove(current_node)
        
        # Обновить расстояния до соседей
        for neighbor, weight in GALAXY_GRAPH[current_node].items():
            possible_new_dist = distances[current_node] + weight
            if possible_new_dist < distances[neighbor]:
                distances[neighbor] = possible_new_dist
                previous_nodes[neighbor] = current_node

    # Восстановление пути
    path = []
    current = end
    if previous_nodes[current] is None and current != start:
        return None, float('inf') # Путь не найден
        
    while current is not None:
        path.append(current)
        current = previous_nodes[current]
        
    path = path[::-1] # Развернуть
    return path, distances[end]


def get_max_reachable_path(start, end, max_fuel):
    """
    Найти путь к end, который позволяет пройти максимально возможное расстояние,
    не превышая max_fuel. Если полный путь недостижим, возвращает путь
    до самой дальней достижимой точки по маршруту к цели.
    
    Args:
        start: Начало
        end: Цель
        max_fuel: Максимальное расстояние (топливо)
        
    Returns:
        (path, distance, reached_target): 
        - path: список планет
        - distance: затраченное расстояние
        - reached_target: bool (достигли ли цели)
    """
    full_path, full_dist = get_path(start, end)
    
    if not full_path:
        return None, 0, False
        
    if full_dist <= max_fuel:
        return full_path, full_dist, True
        
    # Если не хватает топлива на полный путь, идем сколько сможем
    current_fuel = 0
    reachable_path = [start]
    
    for i in range(len(full_path) - 1):
        u = full_path[i]
        v = full_path[i+1]
        dist = GALAXY_GRAPH[u][v]
        
        if current_fuel + dist <= max_fuel:
            reachable_path.append(v)
            current_fuel += dist
        else:
            break
            
    return reachable_path, current_fuel, False
