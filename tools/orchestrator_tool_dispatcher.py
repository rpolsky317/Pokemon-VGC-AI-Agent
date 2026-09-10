

class OrchestratorToolDispatcher:
    """
    Provides a list of tools available to the AI agent.
    """

    def __init__(self, battle_state_agent, pokemon_info_agent, damage_calc_agent):
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

        raise ValueError(
            f"Unknown tool: {tool_name}"
        )