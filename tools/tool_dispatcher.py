from models.damage_calc_request import DamageCalculationRequest

class ToolDispatcher:
    """
    Provides a list of tools available to the AI agent.
    """

    def __init__(self, pokemon_service, battle_state_service, damage_calc_service, battle_state_agent, pokemon_info_agent, damage_calc_agent):
        self.pokemon_service = pokemon_service
        self.battle_state_service = battle_state_service
        self.damage_calc_service = damage_calc_service
        self.battle_state_agent = battle_state_agent
        self.pokemon_info_agent = pokemon_info_agent
        self.damage_calc_agent = damage_calc_agent

    def dispatch(self, tool_name, arguments):
        """
        Execute a tool requested by the AI agent.
        """

        if tool_name  == "battle_state_agent":
            print("Delegating task to battle state agent\n")
            return self.battle_state_agent.run(
                arguments["request"]
            )
        
        if tool_name  == "pokemon_info_agent":
            print("Delegating task to pokemon info agent\n")
            return self.pokemon_info_agent.run(
                arguments["request"]
            )
        
        if tool_name  == "damage_calc_agent":
            print("Delegating task to damage calc agent\n")
            return self.damage_calc_agent.run(
                arguments["request"]
            )

        if tool_name == "get_pokemon_info":
            return self.get_pokemon_info(
                pokemon_name=arguments["pokemon_name"]
            )
        
        if tool_name == "add_opponent_pokemon":
            return self.add_opponent_pokemon(
                pokemon_names=arguments["pokemon_names"]
            )
        if tool_name == "update_pokemon_battle_state":
            return self.update_pokemon_state(
                pokemon_name=arguments["pokemon_name"],
                side=arguments["side"],
                updates=arguments["updates"]
            )

        if tool_name == "update_battle_field":
            return self.update_field(
                weather=arguments.get("weather"),
                terrain=arguments.get("terrain"),
                my_side=arguments.get("my_side"),
                opponent_side=arguments.get("opponent_side")
            )

        if tool_name == "calculate_damage":
            request = DamageCalculationRequest.from_dict(arguments)

            return self.calculate_damage(
                request=request
            )

        raise ValueError(
            f"Unknown tool: {tool_name}"
        )

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

    