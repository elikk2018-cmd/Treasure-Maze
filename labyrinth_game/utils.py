"""
Вспомогательные функции игры
"""

from labyrinth_game.constants import ROOMS

def describe_current_room(game_state):
    """Описание текущей комнаты."""
    room_name = game_state['current_room']
    room = ROOMS.get(room_name, {})
    
    print(f"\n=== {room_name.upper()} ===")
    print(room.get('description', 'Неизвестная комната.'))
    
    # Предметы в комнате
    items = room.get('items', [])
    if items:
        print("Заметные предметы:", ", ".join(items))
    
    # Выходы из комнаты
    exits = room.get('exits', {})
    if exits:
        print("Выходы:", ", ".join(exits.keys()))
    
    # Загадка
    if room.get('puzzle'):
        print("Кажется, здесь есть загадка (используйте команду 'решить').")