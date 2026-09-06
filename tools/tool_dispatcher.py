class ToolDispatcher:
    """
    Provides a list of tools available to the AI agent.
    """

    def __init__(self, pokemon_service, battle_state_service, damage_calc_service):
        self.pokemon_service = pokemon_service
        self.battle_state_service = battle_state_service
        self.damage_calc_service = damage_calc_service

    def get_pokemon_info(self, pokemon_name):
        """
        Returns information about a specific pokemon.
        """
        return self.pokemon_service.get_pokemon_info(pokemon_name)
    
    def calculate_damage(self, request): 
        """ 
        Calculates damage using the Pokemon Champions damage calculator. 
        """ 
        return self.damage_calc_service.calculate(request)
    
    def get_battle_state(self):
        """
        Returns the current state of the Pokemon battle.
        """

        return self.battle_state_service.get_battle_state()
    
    def add_opponent_pokemon(self, pokemon_names):
        """
        Adds the opponent's Pokemon to the current battle state.
        """
        return self.battle_state_service.add_opponent_pokemon(
            pokemon_names
        )

    def update_pokemon_state(
        self,
        pokemon_name,
        side,
        updates
    ):
        """
        Updates known information about a Pokemon.
        """
        self.battle_state_service.update_pokemon(
            pokemon_name=pokemon_name,
            side=side,
            **updates
        )

    def update_field(
        self,
        weather=None,
        terrain=None,
        my_side=None,
        opponent_side=None
    ):
        """
        Updates the current battle field conditions.
        """
        return self.battle_state_service.update_field(
            weather=weather,
            terrain=terrain,
            my_side=my_side,
            opponent_side=opponent_side
        )

    # def update_hp(
    #     self,
    #     pokemon_name,
    #     side,
    #     hp_percent
    # ):
    #     """
    #     Updates the current HP percentage of a Pokemon.
    #     """
    #     self.battle_state_service.update_hp(
    #         pokemon_name=pokemon_name,
    #         side=side,
    #         hp_percent=hp_percent
    #     )

    # def update_boosts(
    #     self,
    #     pokemon_name,
    #     side,
    #     boosts
    # ):
    #     """
    #     Updates the current stat boosts of a Pokemon.
    #     """
    #     self.battle_state_service.update_boosts(
    #         pokemon_name=pokemon_name,
    #         side=side,
    #         boosts=boosts
    #     )

    