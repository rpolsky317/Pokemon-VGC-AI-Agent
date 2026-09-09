
class BattleStateToolsDispatcher:

    """
    Provides a list of tools available to the AI agent.
    """

    def __init__(self, battle_state_service):
        self.battle_state_service = battle_state_service

    def dispatch(self, tool_name, arguements):
        """
        Execute a tool requested by the AI agent.
        """
        
        if tool_name == "get_battle_state":
            return self.get_battle_state()
        
        if tool_name == "add_opponent_pokemon":
            return self.add_opponent_pokemon(
                pokemon_names=arguements["pokemon_names"]
            )
        if tool_name== "update_pokemon_battle_state":
            return self.update_pokemon_state(
                pokemon_name=arguements["pokemon_name"],
                side=arguements["side"],
                updates=arguements["updates"]
            )
        
        if tool_name == "update_battle_field":
            return self.update_field(
                weather=arguements.get("weather"),
                terrain=arguements.get("terrain"),
                my_side=arguements.get("my_side"),
                opponent_side=arguements.get("opponent_side")
            )

        raise ValueError(
            f"Unknown tool: {tool_name}"
        )
    
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

    