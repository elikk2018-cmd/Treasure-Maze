"""
Действия игрока
"""

def get_input(prompt="> "):
    """Получить ввод от пользователя."""
    try:
        return input(prompt).strip().lower()
    except (KeyboardInterrupt, EOFError):
        print("\nВыход из игры.")
        return "quit"

def show_inventory(game_state):
    """Показать инвентарь игрока."""
    inventory = game_state['player_inventory']
    if not inventory:
        print("Ваш инвентарь пуст.")
    else:
        print("Ваш инвентарь:", ", ".join(inventory))