from database.pokemon_database import (
    get_move,
    save_move
)

class MoveRepo:
    """
    Wrapper class around the pokemon database.
    """
    def get(self, move_name: str):
        return get_move(move_name)

    def save(self, move: dict):
        save_move(move)