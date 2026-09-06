import requests


class PokeApiClient:

    BASE_URL = "https://pokeapi.co/api/v2"

    def get_pokemon(self, pokemon_name: str):
        """
        Retrieves basic Pokemon information from PokeAPI.

        Moves are returned as names only. Detailed move information
        is retrieved separately through get_move().
        """

        pokemon_name = pokemon_name.lower()

        url = f"{self.BASE_URL}/pokemon/{pokemon_name}"

        response = requests.get(url)

        if response.status_code == 404:
            return None

        response.raise_for_status()

        data = response.json()

        return {
            "name": data["name"],

            "types": [
                pokemon_type["type"]["name"]
                for pokemon_type in data["types"]
            ],

            "stats": {
                stat["stat"]["name"]: stat["base_stat"]
                for stat in data["stats"]
            },

            "abilities": [
                ability["ability"]["name"]
                for ability in data["abilities"]
            ],

            # Only store the move names here
            "moves": [
                move["move"]["name"]
                for move in data["moves"]
            ]
        }

    def get_move(self, move_name: str):
        """
        Retrieves detailed move information from PokeAPI.
        """

        move_name = move_name.lower()

        url = f"{self.BASE_URL}/move/{move_name}"

        response = requests.get(url)

        if response.status_code == 404:
            return None

        response.raise_for_status()

        data = response.json()

        return {
            "name": data["name"],
            "type": data["type"]["name"],
            "category": data["damage_class"]["name"],
            "power": data["power"],
            "accuracy": data["accuracy"],
            "priority": data["priority"]
        }