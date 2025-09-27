"""
Константы и данные игры
"""

ROOMS = {
    'entrance': {
        'description': 'Вы стоите у входа в древний лабиринт. Каменные стены покрыты мхом.',
        'exits': {'north': 'hall'},
        'items': ['torch'],
        'puzzle': None
    },
    'hall': {
        'description': 'Большой зал с эхом. По центру стоит пьедестал.',
        'exits': {'south': 'entrance', 'east': 'library'},
        'items': [],
        'puzzle': ('На пьедестале надпись: "Сколько будет 2+2?"', '4')
    }
}