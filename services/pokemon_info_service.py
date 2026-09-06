

class PokemonInfoService:
    """
    A service to handle retrieving information about a Pokemon including
    stats, typing, abilities, and moves.
    """
    def __init__(self, pokemon_repository, pokeapi_client, move_service):
        self.pokemon_repository = pokemon_repository
        self.pokeapi_client = pokeapi_client
        self.move_service = move_service

    def get_pokemon_info(self, pokemon_name):

        pokemon = self.pokemon_repository.get(pokemon_name)

        if pokemon is None:

            pokemon = self.pokeapi_client.get_pokemon(
                pokemon_name
            )

            if pokemon is None:
                return {
                    "error": f"Pokemon '{pokemon_name}' was not found."
                }

            self.pokemon_repository.save(pokemon)

        move_names = pokemon["moves"]

        moves = []

        for move_name in move_names:

            move = self.move_service.get_move_info(
                move_name
            )

            if move is not None:
                moves.append(move)

        pokemon_info = pokemon.copy()
        pokemon_info["moves"] = moves

        return pokemon_info