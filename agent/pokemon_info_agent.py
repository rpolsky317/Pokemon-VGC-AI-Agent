from agent.base_agent import BaseAgent

class PokemonInfoAgent(BaseAgent):

    def __init__(
        self,
        tool_dispatcher
    ):

        instructions = """
            You are the Pokemon Information Agent for a competitive Pokemon VGC battle assistant.

            Your responsibility is to lookup and provide information about a pokemon's movepool, base stats, typing, and abilities.


            You MUST use the get_pokemon_info tool to answer any question directed to you.

            For example:

            User:
            "What abilities can Charizard get?"

            You should call get_pokemon_info for Charizard and display the listed abilities.

            User:
            "What are the speed stats of Raichu, Rillaboom, Charizard, and Alakazam?"

            You should call get_pokemon_info 4 times, once for each pokemon listed.

            User:
            "What priority moves can Palafin get?"

            You should call get_pokemon_info for Palafin and filter the movepool for moves with a special priorty.

            You should NOT:

            - Calculate damage
            - Make strategic recommendations.
            - Assume relative speed or attack without using get_pokemon_info.
            - Assume any stat boosts are active, only use the base stats from get_pokemon_info.

            """
        tools = self._build_tools()

        super().__init__(instructions, tools, tool_dispatcher)


    def _build_tools(self):

        return [
            # ---------------------------------------------------------
            # GET POKEMON INFO
            # ---------------------------------------------------------

            {
                "type": "function",
                "name": "get_pokemon_info",
                "description": (
                    "Get information about a specific Pokemon such as its "
                    "base stats, typing, movepool, and possible abilities."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "pokemon_name": {
                            "type": "string",
                            "description": (
                                "The name of the Pokemon to retrieve information about."
                            )
                        }
                    },
                    "required": [
                        "pokemon_name"
                    ],
                    "additionalProperties": False
                }
            }
        ]
    