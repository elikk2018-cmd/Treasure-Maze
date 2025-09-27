"""
Главный модуль игры 'Лабиринт сокровищ'
"""

from labyrinth_game.utils import describe_current_room
from labyrinth_game.player_actions import get_input

def main():
    """Основная функция игры."""
    # Состояние игры
    game_state = {
        'player_inventory': [],
        'current_room': 'entrance',
        'game_over': False,
        'steps_taken': 0
    }
    
    print("=== Лабиринт сокровищ ===")
    print("Добро пожаловать в игру!")
    
    # Показываем стартовую комнату
    describe_current_room(game_state)
    
    # Основной игровой цикл
    while not game_state['game_over']:
        command = get_input("Что вы хотите сделать? ")
        
        if command in ['выход', 'quit', 'exit']:
            print("Спасибо за игру!")
            break
        elif command == 'осмотреться':
            describe_current_room(game_state)
        elif command == 'инвентарь':
            from labyrinth_game.player_actions import show_inventory
            show_inventory(game_state)
        else:
            print(f"Не понимаю команду '{command}'. Попробуйте 'осмотреться', 'инвентарь' или 'выход'")

if __name__ == "__main__":
    main()