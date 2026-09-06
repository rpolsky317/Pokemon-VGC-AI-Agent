from models.pokemon_state import PokemonState
from models.field import Field


class BattleState:
    def __init__(
        self,
        my_pokemon: list[PokemonState],
        opponent_pokemon: list[PokemonState],
        field=None
    ):
        if len(my_pokemon) != 6:
            raise ValueError("my_pokemon must contain exactly 6 Pokemon.")


        self.my_side = my_pokemon

        self.opponent_side = opponent_pokemon

        self.field = field or Field()

    def get_my_pokemon(self, pokemon_name):
        """
        Get a Pokemon from my side by name.
        """
        return self._get_pokemon(self.my_side, pokemon_name)

    def get_opponent_pokemon(self, pokemon_name):
        """
        Get a Pokemon from the opponent's side by name.
        """
        return self._get_pokemon(self.opponent_side, pokemon_name)

    def _get_pokemon(self, side, pokemon_name):
        """
        Find a Pokemon in a side by name.
        """
        for pokemon in side:
            if pokemon.name.lower() == pokemon_name.lower():
                return pokemon

        raise ValueError(
            f"Pokemon '{pokemon_name}' not found."
        )
    
    def to_dict(self):
        return {
            "my_side": [
                pokemon.to_dict()
                for pokemon in self.my_side
            ],
            "opponent_side": [
                pokemon.to_dict()
                for pokemon in self.opponent_side
            ],
            "field": self.field.to_dict()
        }
    
    def add_opponent_pokemon(self, pokemon_names):
        for pokemon_name in pokemon_names:
            self.opponent_side.append(
                PokemonState(name=pokemon_name)
            )

    def update_pokemon(
        self,
        pokemon_name,
        side,
        **updates
    ):
        """
        Update known information about a Pokemon.

        Example:
            battle_state.update_pokemon(
                "Sneasler",
                "opponent",
                ability="Unburden",
                item="Life Orb"
            )
        """

        if side == "my":
            pokemon = self.get_my_pokemon(pokemon_name)

        elif side == "opponent":
            pokemon = self.get_opponent_pokemon(pokemon_name)

        else:
            raise ValueError(
                "side must be either 'my' or 'opponent'."
            )

        for attribute, value in updates.items():

            if not hasattr(pokemon, attribute):
                raise ValueError(
                    f"PokemonState has no attribute "
                    f"'{attribute}'."
                )

            setattr(pokemon, attribute, value)

    def update_hp(self, pokemon_name, side, hp_percent):
        """
        Update a Pokemon's current HP percentage.
        """

        if not 0 <= hp_percent <= 100:
            raise ValueError(
                "hp_percent must be between 0 and 100."
            )

        pokemon = (
            self.get_my_pokemon(pokemon_name)
            if side == "my"
            else self.get_opponent_pokemon(pokemon_name)
        )

        pokemon.hp_percent = hp_percent

    def update_boosts(self, pokemon_name, side, boosts):
        """
        Update a Pokemon's current stat boosts.

        Example:
            {
                "atk": 2,
                "spe": -1
            }
        """

        pokemon = (
            self.get_my_pokemon(pokemon_name)
            if side == "my"
            else self.get_opponent_pokemon(pokemon_name)
        )

        pokemon.boosts.update(boosts)

    def update_field(self, **updates):
        """
        Update the current battle field.

        Example:
            battle_state.update_field(
                weather="Rain",
                terrain="Electric"
            )
        """

        for attribute, value in updates.items():

            if not hasattr(self.field, attribute):
                raise ValueError(
                    f"Field has no attribute '{attribute}'."
                )

            setattr(self.field, attribute, value)