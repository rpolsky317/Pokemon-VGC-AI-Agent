import requests
import database.pokemon_database 

def get_pokemon_info(pokemon_name: str):
    """
    Retrieves information about a Pokemon including
    stats, typing, abilities, and moves.
    """

    pokemon_name = pokemon_name.lower()

    # Check database for info first


    #pokemon = database.get_pokemon(pokemon_name)

    # if pokemon:
    #     return pokemon

    # pokemon = pokeapi.get_pokemon(pokemon_name)

    # for move in pokemon["moves"]:
    #     if not database.get_move(move["name"]):
    #         move_data = pokeapi.get_move(move["name"])
    #         database.save_move(move_data)

    # database.save_pokemon(pokemon)

    # return pokemon

    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name}"

    response = requests.get(url)

    if response.status_code == 404:
        return {
            "error": f"Pokemon '{pokemon_name}' was not found."
        }

    response.raise_for_status()

    data = response.json()

    # Get stats
    stats = {
        stat["stat"]["name"]: stat["base_stat"]
        for stat in data["stats"]
    }

    # Get abilities
    abilities = [
        ability["ability"]["name"]
        for ability in data["abilities"]
    ]

    # Get typing
    types = [
        pokemon_type["type"]["name"]
        for pokemon_type in data["types"]
    ]

    # Get moves
    moves = []

    for move in data["moves"]:

        move_url = move["move"]["url"]

        move_response = requests.get(move_url)
        move_response.raise_for_status()

        move_data = move_response.json()

        moves.append({
            "name": move_data["name"],
            "type": move_data["type"]["name"],
            "category": move_data["damage_class"]["name"],
            "power": move_data["power"],
            "accuracy": move_data["accuracy"],
            "priority": move_data["priority"]
        })

    return {
        "name": data["name"],
        "types": types,
        "stats": stats,
        "abilities": abilities,
        "moves": moves
    }