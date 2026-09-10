from agent.base_agent import BaseAgent

class DamageCalcAgent(BaseAgent):

    def __init__(
        self,
        tool_dispatcher
    ):

        instructions = """
            You are the Damage Calculation Agent for a competitive Pokemon VGC battle assistant.

            Your responsibility is to answer questions about damage and KOs with exact calculations. 

            DAMAGE CALC ROUTINE

            1) You should always receive a copy of the current battle state and a calculation request. 
                - The battle state let's know relevant information like items, natures, and field conditions that may effect calculations.

            2) Call the calculate_damage tool based on the request. Use the information from the battle state and the request to synthesis the correct paramters for calculate_damage.
                - If both the battle state and the request provide different values for the same parameter, use the request's value.
                - If neither the battle state nor the request specify the weather or terrain set it to None, do not make one up.

            3) Whatever information is not provided just leave it blank or default in the parameters, do not invent a value. 

            3) Return the damage ranges and stats from the calculate_damage call to the user.

            For example:

            Request:
            "Will Aerodactyl KO a calm Charizard with Rock Slide?"

                Battle state: {'my_side': [{'name': 'Froslass-Mega', 'level': 50, 'nature': 'Modest', 'ability': None, 'item': None, 'evs': {'hp': 32, 'spa': 32}, 'ivs': {}, 'boosts': {}, 'hp_percent': 100}, {'name': 'Whimsicott', 'level': 50, 'nature': 'Modest', 'ability': None, 'item': None, 'evs': {'spd': 32, 'spa': 32}, 'ivs': {}, 'boosts': {}, 'hp_percent': 100}, {'name': 'Aerodactyl', 'level': 50, 'nature': Adamant, 'ability': None, 'item': None, 'evs': {}, 'ivs': {}, 'boosts': {}, 'hp_percent': 100}, {'name': 'Gholdengo', 'level': 50, 'nature': 'Modest', 'ability': None, 'item': 'Life Orb', 'evs': {'spd': 32, 'spa': 32}, 'ivs': {}, 'boosts': {}, 'hp_percent': 100}, {'name': 'Raichu', 'level': 50, 'nature': None, 'ability': None, 'item': None, 'evs': {}, 'ivs': {}, 'boosts': {}, 'hp_percent': 100}, {'name': 'Pelipper', 'level': 50, 'nature': None, 'ability': None, 'item': None, 'evs': {}, 'ivs': {}, 'boosts': {}, 'hp_percent': 100}], 'opponent_side': [{'name': 'Raichu', 'level': 50, 'nature': None, 'ability': None, 'item': None, 'evs': {}, 'ivs': {}, 'boosts': {}, 'hp_percent': 100}, {'name': 'Sneasler', 'level': 50, 'nature': None, 'ability': None, 'item': None, 'evs': {}, 'ivs': {}, 'boosts': {}, 'hp_percent': 100}, {'name': 'Pelipper', 'level': 50, 'nature': None, 'ability': None, 'item': None, 'evs': {}, 'ivs': {}, 'boosts': {}, 'hp_percent': 100}, {'name': 'Pikachu', 'level': 50, 'nature': None, 'ability': None, 'item': None, 'evs': {}, 'ivs': {}, 'boosts': {}, 'hp_percent': 100}, {'name': 'Blastoise', 'level': 50, 'nature': None, 'ability': None, 'item': None, 'evs': {}, 'ivs': {}, 'boosts': {}, 'hp_percent': 100}, {'name': 'Charizard', 'level': 50, 'nature': None, 'ability': None, 'item': None, 'evs': {}, 'ivs': {}, 'boosts': {}, 'hp_percent': 100}], 'field': {'game_type': 'Doubles', 'weather': None, 'terrain': None, 'my_side': {'reflect': False, 'light_screen': False, 'aurora_veil': False, 'tailwind': False}, 'opponent_side': {'reflect': False, 'light_screen': False, 'aurora_veil': False, 'tailwind': False}}}

            You should pass in Aerodactyl as the attacker with the items, nature, level, and evs from the battle state, and you should pass in Charizard as the defender with Calm nature and 0 evs and None item since those were not provided.

            Request:
            "Will Aerodactyl KO a calm Charizard with Rock Slide?"

                Battle state: {'my_side': [{'name': 'Froslass-Mega', 'level': 50, 'nature': 'Modest', 'ability': None, 'item': None, 'evs': {'hp': 32, 'spa': 32}, 'ivs': {}, 'boosts': {}, 'hp_percent': 100}, {'name': 'Whimsicott', 'level': 50, 'nature': 'Modest', 'ability': None, 'item': None, 'evs': {'spd': 32, 'spa': 32}, 'ivs': {}, 'boosts': {}, 'hp_percent': 100}, {'name': 'Aerodactyl', 'level': 50, 'nature': Adamant, 'ability': None, 'item': None, 'evs': {}, 'ivs': {}, 'boosts': {}, 'hp_percent': 100}, {'name': 'Gholdengo', 'level': 50, 'nature': 'Modest', 'ability': None, 'item': 'Life Orb', 'evs': {'spd': 32, 'spa': 32}, 'ivs': {}, 'boosts': {}, 'hp_percent': 100}, {'name': 'Raichu', 'level': 50, 'nature': None, 'ability': None, 'item': None, 'evs': {}, 'ivs': {}, 'boosts': {}, 'hp_percent': 100}, {'name': 'Pelipper', 'level': 50, 'nature': None, 'ability': None, 'item': None, 'evs': {}, 'ivs': {}, 'boosts': {}, 'hp_percent': 100}], 'opponent_side': [{'name': 'Raichu', 'level': 50, 'nature': None, 'ability': None, 'item': None, 'evs': {}, 'ivs': {}, 'boosts': {}, 'hp_percent': 100}, {'name': 'Sneasler', 'level': 50, 'nature': None, 'ability': None, 'item': None, 'evs': {}, 'ivs': {}, 'boosts': {}, 'hp_percent': 100}, {'name': 'Pelipper', 'level': 50, 'nature': None, 'ability': None, 'item': None, 'evs': {}, 'ivs': {}, 'boosts': {}, 'hp_percent': 100}, {'name': 'Pikachu', 'level': 50, 'nature': None, 'ability': None, 'item': None, 'evs': {}, 'ivs': {}, 'boosts': {}, 'hp_percent': 100}, {'name': 'Blastoise', 'level': 50, 'nature': None, 'ability': None, 'item': None, 'evs': {}, 'ivs': {}, 'boosts': {}, 'hp_percent': 100}, {'name': 'Charizard', 'level': 50, 'nature': None, 'ability': None, 'item': None, 'evs': {}, 'ivs': {}, 'boosts': {}, 'hp_percent': 100}], 'field': {'game_type': 'Doubles', 'weather': sun, 'terrain': None, 'my_side': {'reflect': False, 'light_screen': False, 'aurora_veil': False, 'tailwind': False}, 'opponent_side': {'reflect': False, 'light_screen': False, 'aurora_veil': False, 'tailwind': False}}}

            You should pass in Aerodactyl as the attacker with the items, nature, level, and evs from the battle state, and you should pass in Charizard as the defender with Calm nature and 0 evs and None item since those were not provided, and you should set the weather to sun as in the battle state.

            Do not re-run the calculate_damage method with different parameters, only run it once. leave unknowns as they are in the battle state even if they are null.

            Never replace null values with:
                - Sun
                - Rain
                - Sand
                - Hail
                - Snow
                - Misty Terrain
                - Electric Terrain
                - Grassy Terrain
                - Psychic Terrain

                unless those values are explicitly present in the authoritative
                BattleState or explicitly specified as a hypothetical condition in
                the user's damage calculation request.

            """
        tools = self._build_tools()

        super().__init__(instructions, tools, tool_dispatcher)


    def _build_tools(self):

        return [
            # ---------------------------------------------------------
            # CALCULATE DAMAGE
            # ---------------------------------------------------------
            {
                "type": "function",
                "name": "calculate_damage",
                "description": (
                    "AUTHORITATIVE Pokemon Champions damage calculator. "
                    "MUST be used for any question involving damage, KO chances, "
                    "damage ranges, damage percentages, type effectiveness, "
                    "resistances, or whether a move can KO a Pokemon. "
                    "Do not estimate damage using Pokemon stats or PokeAPI data. "
                    "Provide the attacker, defender, move, and any known battle "
                    "conditions such as weather, terrain, boosts, items, abilities, "
                    "or side effects."
                ),

                "parameters": {
                    "type": "object",
                    "properties": {

                        # -------------------------------------------------
                        # ATTACKER
                        # -------------------------------------------------

                        "attacker": {
                            "type": "object",
                            "properties": {
                                "species": {
                                    "type": "string",
                                    "description": (
                                        "Attacking Pokemon species."
                                    )
                                },
                                "nature": {
                                    "type": "string",
                                    "description": (
                                        "Pokemon nature. Defaults to Serious "
                                        "if omitted."
                                    )
                                },
                                "ability": {
                                    "type": "string"
                                },
                                "item": {
                                    "type": "string"
                                },
                                "statPoints": {
                                    "type": "object",
                                    "description": (
                                        "Pokemon Champions stat points. These are Champions stat "
                                        "points, not traditional Pokemon EVs. Any omitted stat "
                                        "defaults to 0."
                                    ),
                                    "properties": {
                                        "hp": {
                                            "type": "integer"
                                        },
                                        "atk": {
                                            "type": "integer"
                                        },
                                        "def": {
                                            "type": "integer"
                                        },
                                        "spa": {
                                            "type": "integer"
                                        },
                                        "spd": {
                                            "type": "integer"
                                        },
                                        "spe": {
                                            "type": "integer"
                                        }
                                    },
                                    "required": [],
                                    "additionalProperties": False
                                },
                                "boosts": {
                                    "type": "object",

                                    "properties": {
                                        "atk": {
                                            "type": "integer"
                                        },
                                        "def": {
                                            "type": "integer"
                                        },
                                        "spa": {
                                            "type": "integer"
                                        },
                                        "spd": {
                                            "type": "integer"
                                        },
                                        "spe": {
                                            "type": "integer"
                                        }
                                    },
                                    "required": [],
                                    "additionalProperties": False
                                },
                                "status": {
                                    "type": "string"
                                }
                            },
                            "required": [
                                "species"
                            ],
                            "additionalProperties": False
                        },
                        # -------------------------------------------------
                        # DEFENDER
                        # -------------------------------------------------

                        "defender": {
                            "type": "object",
                            "properties": {

                                "species": {
                                    "type": "string"
                                },
                                "nature": {
                                    "type": "string"
                                },
                                "ability": {
                                    "type": "string"
                                },
                                "item": {
                                    "type": "string"
                                },
                                "statPoints": {
                                    "type": "object",
                                    "properties": {
                                        "hp": {
                                            "type": "integer"
                                        },
                                        "atk": {
                                            "type": "integer"
                                        },
                                        "def": {
                                            "type": "integer"
                                        },
                                        "spa": {
                                            "type": "integer"
                                        },
                                        "spd": {
                                            "type": "integer"
                                        },
                                        "spe": {
                                            "type": "integer"
                                        }
                                    },
                                    "required": [],
                                    "additionalProperties": False
                                },
                                "boosts": {
                                    "type": "object",
                                    "properties": {
                                        "atk": {
                                            "type": "integer"
                                        },
                                        "def": {
                                            "type": "integer"
                                        },
                                        "spa": {
                                            "type": "integer"
                                        },
                                        "spd": {
                                            "type": "integer"
                                        },
                                        "spe": {
                                            "type": "integer"
                                        }
                                    },
                                    "required": [],
                                    "additionalProperties": False
                                },
                                "status": {
                                    "type": "string"
                                }
                            },
                            "required": [
                                "species"
                            ],
                            "additionalProperties": False
                        },
                        # -------------------------------------------------
                        # MOVE
                        # -------------------------------------------------
                        "move": {
                            "type": "object",
                            "properties": {
                                "name": {
                                    "type": "string",
                                    "description": (
                                        "Move being used by the attacker."
                                    )
                                }
                            },
                            "required": [
                                "name"
                            ],
                            "additionalProperties": False
                        },
                        # -------------------------------------------------
                        # FIELD
                        # -------------------------------------------------
                        "field": {
                            "type": "object",
                            "properties": {
                                "weather": {
                                    "type": "string",
                                    "enum": [
                                        "Sun",
                                        "Rain",
                                        "Sand",
                                        "Hail",
                                        "Snow"
                                    ]
                                },
                                "terrain": {
                                    "type": "string",
                                    "enum": [
                                        "Electric",
                                        "Grassy",
                                        "Psychic",
                                        "Misty"
                                    ]
                                },
                                "magicRoom": {
                                    "type": "boolean"
                                },
                                "wonderRoom": {
                                    "type": "boolean"
                                },
                                "attackerSide": {
                                    "type": "object",
                                    "properties": {
                                        "reflect": {
                                            "type": "boolean"
                                        },
                                        "lightScreen": {
                                            "type": "boolean"
                                        },
                                        "auroraVeil": {
                                            "type": "boolean"
                                        },
                                        "protected": {
                                            "type": "boolean"
                                        },
                                        "seeded": {
                                            "type": "boolean"
                                        },
                                        "charge": {
                                            "type": "boolean"
                                        },
                                        "helpingHand": {
                                            "type": "boolean"
                                        },
                                        "tailwind": {
                                            "type": "boolean"
                                        },
                                        "friendGuard": {
                                            "type": "boolean"
                                        },
                                        "battery": {
                                            "type": "boolean"
                                        },
                                        "powerSpot": {
                                            "type": "boolean"
                                        },
                                        "steelySpirit": {
                                            "type": "boolean"
                                        },
                                        "flowerGift": {
                                            "type": "boolean"
                                        }
                                    },
                                    "required": [],
                                    "additionalProperties": False
                                },
                                "defenderSide": {
                                    "type": "object",
                                    "properties": {
                                        "reflect": {
                                            "type": "boolean"
                                        },
                                        "lightScreen": {
                                            "type": "boolean"
                                        },
                                        "auroraVeil": {
                                            "type": "boolean"
                                        },
                                        "protected": {
                                            "type": "boolean"
                                        },
                                        "seeded": {
                                            "type": "boolean"
                                        },
                                        "charge": {
                                            "type": "boolean"
                                        },
                                        "helpingHand": {
                                            "type": "boolean"
                                        },
                                        "tailwind": {
                                            "type": "boolean"
                                        },
                                        "friendGuard": {
                                            "type": "boolean"
                                        },
                                        "battery": {
                                            "type": "boolean"
                                        },
                                        "powerSpot": {
                                            "type": "boolean"
                                        },
                                        "steelySpirit": {
                                            "type": "boolean"
                                        },
                                        "flowerGift": {
                                            "type": "boolean"
                                        }
                                    },
                                    "required": [],
                                    "additionalProperties": False
                                }
                            },
                            "required": [],
                            "additionalProperties": False
                        }
                    },
                    # THIS IS THE IMPORTANT PART:
                    # required belongs here, alongside properties.
                    "required": [
                        "attacker",
                        "defender",
                        "move"
                    ],

                    "additionalProperties": False
                }
            }
        ]
    