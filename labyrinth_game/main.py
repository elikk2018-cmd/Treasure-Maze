"""
Главный модуль игры 'Лабиринт сокровищ'
"""

from labyrinth_game.utils import describe_room, show_help, solve_puzzle, attempt_open_treasure
from labyrinth_game.player_actions import get_player_input, move_player, take_item, use_item, show_inventory


def process_command(game_state, command):
    """
    Обработка команд игрока
    """
    parts = command.split()
    if not parts:
        return
    
    main_command = parts[0]
    
    # Движение по односложным командам
    if main_command in ['север', 'юг', 'восток', 'запад']:
        move_player(game_state, main_command)
    
    # Команда взять предмет
    elif main_command == 'взять' and len(parts) > 1:
        take_item(game_state, parts[1])
    
    # Команда использовать предмет
    elif main_command == 'использовать' and len(parts) > 1:
        use_item(game_state, parts[1])
    
    # Команда решить загадку
    elif main_command == 'решить':
        current_room = game_state['current_room']
        if current_room == 'зал':
            attempt_open_treasure(game_state)
        else:
            solve_puzzle(game_state)
    
    # Другие команды
    elif main_command == 'инвентарь':
        show_inventory(game_state)
    elif main_command in ['осмотреться', 'осмотреть']:
        describe_room(game_state['current_room'])
    elif main_command == 'помощь':
        show_help()
    elif main_command in ['выход', 'quit', 'exit']:
        game_state['game_over'] = True
    else:
        print(f"Не понимаю команду '{command}'. Напишите 'помощь' для списка команд.")


def main():
    """
    Основная функция игры
    """
    game_state = {
        'player_inventory': [],
        'current_room': 'start',
        'game_over': False,
        'steps_taken': 0
    }
    
    print("=== Лабиринт сокровищ ===")
    print("Добро пожаловать в игру! Найдите сокровище!")
    print("Напишите 'помощь' для списка команд.")
    
    describe_room(game_state['current_room'])
    
    # Основной игровой цикл
    while not game_state['game_over']:
        command = get_player_input("\nЧто вы хотите сделать? ")
        process_command(game_state, command)
    
    print("Спасибо за игру!")


if __name__ == "__main__":
    main()