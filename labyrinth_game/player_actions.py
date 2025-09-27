"""
Действия игрока
"""

from labyrinth_game.constants import ROOMS
from labyrinth_game.utils import describe_room, get_item_description, random_event, can_use_item


def move_player(game_state, direction):
    """
    Переместить игрока в указанном направлении
    """
    current_room = game_state['current_room']
    room = ROOMS.get(current_room, {})
    exits = room.get('exits', {})
    
    if direction in exits:
        new_room_name = exits[direction]
        new_room = ROOMS.get(new_room_name, {})
        
        if new_room.get('locked'):
            if 'ключ' in game_state['player_inventory']:
                print("🔑 Вы использовали ключ! Дверь открыта.")
                new_room['locked'] = False
            else:
                print("🔒 Дверь заперта. Нужен ключ.")
                return False
        
        game_state['current_room'] = new_room_name
        game_state['steps_taken'] += 1
        print(f"Вы пошли на {direction}.")
        describe_room(new_room_name)
        
        random_event(game_state)
        return True
    else:
        print(f"Нельзя пойти на {direction}.")
        return False


def take_item(game_state, item_name):
    """
    Взять предмет из комнаты
    """
    current_room = game_state['current_room']
    room = ROOMS.get(current_room, {})
    items = room.get('items', [])
    
    if item_name in items:
        game_state['player_inventory'].append(item_name)
        room['items'].remove(item_name)
        print(f"✅ Вы взяли: {item_name}")
        return True
    else:
        print(f"❌ Предмет '{item_name}' не найден здесь.")
        return False


def use_item(game_state, item_name):
    """
    Использовать предмет из инвентаря
    """
    inventory = game_state['player_inventory']
    
    if item_name not in inventory:
        print(f"❌ У вас нет предмета '{item_name}'.")
        return
    
    if not can_use_item(item_name):
        print(f"❌ Предмет '{item_name}' нельзя использовать.")
        return
    
    current_room = game_state['current_room']
    
    if item_name == 'факел':
        print("🔥 Факел освещает путь. Теперь вы видите лучше!")
    elif item_name == 'ключ':
        print("🔑 Ключ блестит. Наверное, что-то открывает.")
        if current_room == 'сокровищница':
            room = ROOMS.get(current_room, {})
            if room.get('locked'):
                room['locked'] = False
                print("🎉 Вы открыли дверь в сокровищницу!")
    else:
        print(f"Вы используете {item_name}, но ничего не происходит.")


def show_inventory(game_state):
    """
    Показать инвентарь игрока
    """
    inventory = game_state['player_inventory']
    if not inventory:
        print("🎒 Ваш инвентарь пуст.")
    else:
        print("🎒 Ваш инвентарь:")
        for item in inventory:
            description = get_item_description(item)
            print(f"  - {item}: {description}")


def get_player_input(prompt="> "):
    """
    Получить ввод от игрока с обработкой ошибок
    """
    try:
        return input(prompt).strip().lower()
    except (KeyboardInterrupt, EOFError):
        print("\nВыход из игры.")
        return "выход"