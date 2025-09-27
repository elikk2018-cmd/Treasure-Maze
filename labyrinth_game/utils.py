"""
Вспомогательные функции игры
"""

import math
from labyrinth_game.constants import (
    ROOMS, ITEMS, MESSAGES, COMMANDS,
    EVENT_PROBABILITY, TRAP_DAMAGE_THRESHOLD,
    RANDOM_SEED_MULTIPLIER, RANDOM_SEED_MODIFIER,
    EVENT_FIND_COIN, EVENT_HEAR_NOISE, EVENT_TRAP_TRIGGER
)


def pseudo_random(seed, modulo):
    """
    Псевдослучайный генератор на основе синуса
    Возвращает целое число в диапазоне [0, modulo)
    """
    x = math.sin(seed * RANDOM_SEED_MULTIPLIER) * RANDOM_SEED_MODIFIER
    fraction = x - math.floor(x)
    return math.floor(fraction * modulo)


def trigger_trap(game_state):
    """
    Активация ловушки - негативные последствия для игрока
    """
    print(MESSAGES['trap_activated'])
    inventory = game_state['player_inventory']
    
    if inventory:
        item_index = pseudo_random(game_state['steps_taken'], len(inventory))
        lost_item = inventory[item_index]
        inventory.remove(lost_item)
        print(MESSAGES['item_lost'].format(lost_item))
    else:
        chance = pseudo_random(game_state['steps_taken'], EVENT_PROBABILITY)
        if chance < TRAP_DAMAGE_THRESHOLD:
            print(MESSAGES['game_over'])
            game_state['game_over'] = True
        else:
            print(MESSAGES['survived'])


def random_event(game_state):
    """
    Случайное событие при перемещении
    """
    event_chance = pseudo_random(game_state['steps_taken'], EVENT_PROBABILITY)
    
    if event_chance == 0:
        event_type = pseudo_random(game_state['steps_taken'] + 1, 3)
        current_room = game_state['current_room']
        inventory = game_state['player_inventory']
        
        if event_type == EVENT_FIND_COIN:
            print(MESSAGES['found_coin'])
            ROOMS[current_room]['items'].append('монетка')
        elif event_type == EVENT_HEAR_NOISE:
            print(MESSAGES['heard_noise'])
            if 'меч' in inventory:
                print(MESSAGES['scared_away'])
        elif event_type == EVENT_TRAP_TRIGGER:
            room = ROOMS.get(current_room, {})
            if room.get('is_trap') and 'факел' not in inventory:
                print("💀 Опасность! Вы не видите ловушку в темноте!")
                trigger_trap(game_state)


def solve_puzzle(game_state):
    """
    Решение загадки в текущей комнате
    """
    current_room = game_state['current_room']
    room = ROOMS.get(current_room, {})
    puzzle = room.get('puzzle')
    
    if not puzzle:
        print("Здесь нет загадки для решения.")
        return
    
    question, correct_answer = puzzle
    print(f"Загадка: {question}")
    
    from labyrinth_game.player_actions import get_player_input
    player_answer = get_player_input("Ваш ответ: ").strip().lower()
    
    correct_answers = [correct_answer]
    if correct_answer == '10':
        correct_answers.extend(['десять', '10'])
    
    if player_answer in correct_answers:
        print("✅ Правильно! Загадка решена!")
        
        if current_room == 'зал':
            game_state['player_inventory'].append('ключ')
            print("🗝️ Вы получаете ключ от сокровищницы!")
        elif current_room == 'коридор':
            game_state['player_inventory'].append('ключ')
            print("🗝️ Вы находите ключ!")
        
        room['puzzle'] = None
    else:
        print("❌ Неверно. Попробуйте снова.")
        if room.get('is_trap'):
            trigger_trap(game_state)


def attempt_open_treasure(game_state):
    """
    Попытка открыть сундук с сокровищами
    """
    current_room = game_state['current_room']
    room = ROOMS.get(current_room, {})
    inventory = game_state['player_inventory']
    
    if 'сундук' not in room.get('items', []):
        print("Сундук уже открыт или отсутствует.")
        return
    
    if 'ключ' in inventory:
        print("🔑 Вы используете ключ! Сундук открыт!")
        room['items'].remove('сундук')
        room['items'].append('сокровище')
        print(MESSAGES['victory'])
        game_state['game_over'] = True
        return
    
    from labyrinth_game.player_actions import get_player_input
    answer = get_player_input("Сундук заперт. Попробовать ввести код? (да/нет): ")
    
    if answer == 'да':
        code = get_player_input("Введите код: ")
        if code in ['10', 'десять']:
            print("✅ Код верный! Сундук открыт!")
            room['items'].remove('сундук')
            room['items'].append('сокровище')
            print(MESSAGES['victory'])
            game_state['game_over'] = True
        else:
            print("❌ Неверный код.")
    else:
        print("Вы отступаете от сундука.")


def describe_room(room_name):
    """
    Описание текущей комнаты
    """
    room = ROOMS.get(room_name, {})
    
    print(f"\n=== {room.get('name', 'Неизвестная комната')} ===")
    print(room.get('description', 'Описание отсутствует.'))
    
    items = room.get('items', [])
    if items:
        print("📦 Предметы здесь:", ", ".join(items))
    
    exits = room.get('exits', {})
    if exits:
        directions = list(exits.keys())
        print("🚪 Выходы:", ", ".join(directions))
    
    if room.get('puzzle'):
        print("❓ Здесь есть загадка (команда 'решить')")
    
    if room.get('locked'):
        print("🔒 Дверь заперта.")


def show_help():
    """
    Показать справку по командам
    """
    print("\n=== Доступные команды ===")
    for command, description in COMMANDS.items():
        print(f"  {command:<16} - {description}")


def get_item_description(item_name):
    """
    Получить описание предмета
    """
    return ITEMS.get(item_name, {}).get('description', 'Странный предмет.')


def can_use_item(item_name):
    """
    Проверить, можно ли использовать предмет
    """
    return ITEMS.get(item_name, {}).get('usable', False)