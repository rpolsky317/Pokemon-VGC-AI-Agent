from database.pokemon_database import (
    get_pokemon,
    save_pokemon
)


class PokemonRepo:
    """
    Wrapper class around the pokemon database.
    """
    def get(self, pokemon_name: str):
        return get_pokemon(pokemon_name)

    def save(self, pokemon: dict):
        save_pokemon(pokemon)