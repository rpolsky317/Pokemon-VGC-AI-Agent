
class PokemonInfoToolDispatcher:

    """
    Provides a list of tools available to the AI agent.
    """

    def __init__(self, pokemon_service):
        self.pokemon_service = pokemon_service

    def dispatch(self, tool_name, arguments):
        """
        Execute a tool requested by the AI agent.
        """
        
        if tool_name == "get_pokemon_info":
            return self.get_pokemon_info(
                pokemon_name=arguments["pokemon_name"]
            )

        raise ValueError(
            f"Unknown tool: {tool_name}"
        )
    
    def get_pokemon_info(self, pokemon_name):
        """
        Returns information about a specific pokemon.
        """
        return self.pokemon_service.get_pokemon_info(pokemon_name)
    
    