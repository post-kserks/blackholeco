"""
Обработка эффектов из диалогов, новостей, заказов.
"""


from utils.io import print_slow

def apply_effects(effects, state):
    """
    Применить список эффектов к состоянию игры.
    
    Типы эффектов:
    - flag: установить сюжетный флаг
    - money: добавить/отнять деньги
    - reputation: изменить репутацию
    - end_game: завершить игру (смерть)
    - set_planet: переместить игрока
    - death_if_arrive: пометить планету как смертельную
    """
    for effect in effects:
        effect_type = effect.get("type")

        if effect_type == "flag":
            value = effect.get("value", True)
            state.flags.set(effect["name"], value)

        elif effect_type == "money":
            state.add_money(effect["amount"])

        elif effect_type == "reputation":
            faction = effect["faction"]
            amount = effect["amount"]
            state.change_reputation(faction, amount)

        elif effect_type == "end_game":
            reason = effect.get("reason", "Игра окончена")
            state.die(reason)

        elif effect_type == "set_planet":
            state.current_planet = effect["planet"]

        elif effect_type == "death_if_arrive":
            planet = effect["planet"]
            state.flags.set(f"dead_zone_{planet}")

        elif effect_type == "add_cargo":
            item = effect["item"]
            state.cargo.append(item)

        elif effect_type == "remove_cargo":
            item = effect["item"]
            if item in state.cargo:
                state.cargo.remove(item)

        elif effect_type == "give_order":
            from orders.order import Order
            state.current_order = Order(
                cargo=effect["cargo"],
                origin=state.current_planet,
                destination=effect["destination"],
                reward=effect["reward"],
                deadline=effect.get("deadline"),
                faction=effect.get("faction")
            )
            print(f"\n[ЗАДАНИЕ ОБНОВЛЕНО] Доставить {effect['cargo']} на {effect['destination']}")

        elif effect_type == "unlock_event":
            event_id = effect["id"]
            state.flags.set(f"event_unlocked_{event_id}")

        elif effect_type == "confirm_pending_order":
            if state.pending_order:
                state.current_order = state.pending_order
                state.pending_order = None
                print(f"\n[ЗАДАНИЕ ПРИНЯТО] Доставить {state.current_order.cargo} на {state.current_order.destination}")

        elif effect_type == "reject_pending_order":
            state.pending_order = None
            print("\n[ЗАДАНИЕ ОТКЛОНЕНО]")

        elif effect_type == "complete_order":
            if state.current_order:
                print_slow("\n📦 Вы доставили заказ!")
                reward = state.current_order.reward
                state.current_order.complete(state)
                print_slow(f"Получено: {reward} кредитов")


def check_condition(condition, state):
    """
    Проверить условие для отображения выбора/события.
    
    Типы условий:
    - flag: проверить флаг
    - money_gte: деньги >= значение
    - money_lte: деньги <= значение
    - reputation_gte: репутация >= значение
    - day_gte: день >= значение
    """
    cond_type = condition.get("type")

    if cond_type == "flag":
        expected = condition.get("value", True)
        return state.flags.get(condition["name"]) == expected

    elif cond_type == "flag_not":
        return not state.flags.get(condition["name"])

    elif cond_type == "money_gte":
        return state.money >= condition["value"]

    elif cond_type == "money_lte":
        return state.money <= condition["value"]

    elif cond_type == "reputation_gte":
        faction = condition["faction"]
        return state.get_reputation(faction) >= condition["value"]

    elif cond_type == "reputation_lte":
        faction = condition["faction"]
        return state.get_reputation(faction) <= condition["value"]

    elif cond_type == "day_gte":
        return state.day >= condition["value"]

    elif cond_type == "has_cargo":
        return condition["item"] in state.cargo

    return True  # Если условие неизвестно — пропускаем


def check_conditions(conditions, state):
    """Проверить все условия (AND логика)"""
    if not conditions:
        return True
    return all(check_condition(c, state) for c in conditions)
