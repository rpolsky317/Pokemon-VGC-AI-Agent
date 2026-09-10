from agent.base_agent import BaseAgent

class BattleStateAgent(BaseAgent):

    def __init__(
        self,
        tool_dispatcher
    ):

        instructions = """
            You are the Battle State Agent for a competitive Pokemon VGC battle assistant.

            Your responsibility is to maintain and retrieve the current BattleState.

            You handle:

            - Adding Pokemon to either team
            - Updating Pokemon battle information
            - Recording weather
            - Recording terrain
            - Recording field conditions
            - Recording side conditions
            - Recording stat boosts
            - Recording status conditions
            - Retrieving the current BattleState

            You MUST use the available battle state tools when the user provides
            new battle information.

            Do not merely acknowledge battle information.

            For example:

            User:
            "My opponent has Charizard, Raichu, and Pelipper."

            You should use the appropriate battle state tool to record those Pokemon.

            User:
            "My opponent set up Tailwind."

            You should update the BattleState.

            User:
            "What Pokemon does my opponent have?"

            You should retrieve the BattleState.

            You should NOT:

            - Calculate damage
            - Look up Pokemon base stats
            - Look up Pokemon abilities
            - Look up Pokemon moves
            - Make strategic recommendations unless they can be answered
            solely from the BattleState

            Your job is to accurately maintain the BattleState.
            """
        tools = self._build_tools()

        super().__init__(instructions, tools, tool_dispatcher)


    def _build_tools(self):

        return [


            # ---------------------------------------------------------
            # GET BATTLE STATE
            # ---------------------------------------------------------

            {
                "type": "function",
                "name": "get_battle_state",
                "description": (
                    "Get the authoritative current BattleState. "
                    "Use this tool whenever the user asks about their Pokemon, "
                    "their opponent's Pokemon, the teams, active Pokemon, HP, "
                    "known Pokemon information, or current field conditions. "
                    "\n\n"
                    "The returned state contains separate lists for my Pokemon "
                    "and my opponent's Pokemon. When the user refers to "
                    "\"my Pokemon\" or \"my opponent's Pokemon\", inspect the "
                    "appropriate list in this result. "
                    "\n\n"
                    "Do not assume that the conversation history contains the "
                    "complete or current battle state. Always use this tool for "
                    "questions about the current battle state."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": [],
                    "additionalProperties": False
                }
            },

            # ---------------------------------------------------------
            # UPDATE POKEMON BATTLE STATE
            # ---------------------------------------------------------

            {
                "type": "function",
                "name": "update_pokemon_battle_state",
                "description": (
                    "Update information known about a Pokemon in the current "
                    "battle. Use this when new information is learned about "
                    "an opponent or when the battle state changes."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {

                        "pokemon_name": {
                            "type": "string",
                            "description": (
                                "The Pokemon whose state should be updated."
                            )
                        },

                        "side": {
                            "type": "string",
                            "enum": [
                                "my",
                                "opponent"
                            ],
                            "description": (
                                "Which side of the battle the Pokemon is on."
                            )
                        },

                        "updates": {
                            "type": "object",
                            "description": (
                                "The Pokemon attributes to update."
                            ),
                            "additionalProperties": True
                        }
                    },

                    "required": [
                        "pokemon_name",
                        "side",
                        "updates"
                    ],

                    "additionalProperties": False
                }
            },

            # ---------------------------------------------------------
            # UPDATE BATTLE FIELD
            # ---------------------------------------------------------

            {
                "type": "function",
                "name": "update_battle_field",
                "description": (
                    "Update the current battle field state. Use this whenever "
                    "the user reports a change to weather, terrain, or a side "
                    "condition such as Reflect, Light Screen, Aurora Veil, "
                    "or Tailwind."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {

                        "weather": {
                            "type": [
                                "string",
                                "null"
                            ],
                            "description": (
                                "Current global weather. Use Sun, Rain, Sand, "
                                "Hail, or Snow. Use null when no weather is active."
                            )
                        },

                        "terrain": {
                            "type": [
                                "string",
                                "null"
                            ],
                            "description": (
                                "Active terrain. Only provide this if terrain is explicitly "
                                "active or known from BattleState. Do NOT assume Misty Terrain "
                                "or any other terrain when none is specified, use none."
                            )
                        },

                        "my_side": {
                            "type": "object",
                            "description": (
                                "Field conditions currently active on my side."
                            ),
                            "properties": {
                                "reflect": {
                                    "type": "boolean"
                                },
                                "light_screen": {
                                    "type": "boolean"
                                },
                                "aurora_veil": {
                                    "type": "boolean"
                                },
                                "tailwind": {
                                    "type": "boolean"
                                }
                            },
                            "additionalProperties": False
                        },

                        "opponent_side": {
                            "type": "object",
                            "description": (
                                "Field conditions currently active on the opponent's side."
                            ),
                            "properties": {
                                "reflect": {
                                    "type": "boolean"
                                },
                                "light_screen": {
                                    "type": "boolean"
                                },
                                "aurora_veil": {
                                    "type": "boolean"
                                },
                                "tailwind": {
                                    "type": "boolean"
                                }
                            },
                            "additionalProperties": False
                        }
                    },

                    "required": [],

                    "additionalProperties": False
                }
            },
            {
                "type": "function",
                "name": "add_opponent_pokemon",
                "description": (
                    "Add or update the opponent's Pokemon team in the current battle state. "
                    "Use this whenever the user provides the opponent's Pokemon team. "
                    "The user may provide up to 6 Pokemon. "
                    "Store the Pokemon names exactly as provided."
                ),
                "parameters": {
                    "type": "object",
                    "properties": {
                        "pokemon_names": {
                            "type": "array",
                            "description": (
                                "The Pokemon on the opponent's team. "
                                "Usually a list of 6 Pokemon names."
                            ),
                            "items": {
                                "type": "string"
                            }
                        }
                    },
                    "required": ["pokemon_names"],
                    "additionalProperties": False
                }
            },

        ]
    
    


    