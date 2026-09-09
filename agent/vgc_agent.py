import os
import json
from dotenv import load_dotenv
from openai import OpenAI
from models.damage_calc_request import DamageCalculationRequest

class VGCAgent:

    def __init__(self, tool_dispatcher):
        load_dotenv()

        self.tool_dispatcher = tool_dispatcher
        self.tool_call_history = []

        self.client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY")
        )

        self.instructions = """
        You are a competitive Pokemon VGC battle assistant.

        You maintain a persistent BattleState representing the current battle.

        When the user provides new information about the current battle,
        you MUST update the BattleState using the appropriate tool.
        Do not merely acknowledge the information in your response.

        When the user asks about the current battle state, use
        get_battle_state rather than relying on information from the
        conversation alone.

        Use the available Pokemon information tools when you need
        reliable information about Pokemon, moves, abilities, stats,
        or typing.

        INITIAL BATTLE REPORT:

        When the user provides the opponent's team for the first time, you MUST do the
        following before producing your response:

        1. Store the opponent's entire team using add_opponent_pokemon.

        2. Call get_battle_state to retrieve the current battle state.

        3. Identify the six opponent Pokemon from opponent_pokemon in the battle state.

        4. Call get_pokemon_info separately for EVERY opponent Pokemon.

        5. If my six Pokemon are already present in BattleState, call get_pokemon_info
        separately for EVERY one of my six Pokemon as well.

        6. Use the returned BASE STATS to calculate the following:

        A. DEFENSIVE PROFILE
            Compare the team's base Defense and base Special Defense.

            For each Pokemon, consider its base Defense and base Special Defense.
            Determine whether the overall opponent team is more physically defensive
            or specially defensive.

            Explain the conclusion using the actual stats retrieved from
            get_pokemon_info.

        B. OFFENSIVE PROFILE
            Compare the team's base Attack and base Special Attack.

            Determine whether the opponent team is more physically offensive or
            specially offensive.

            Explain the conclusion using the actual stats retrieved from
            get_pokemon_info.

        C. SPEED ORDER
            Create a list containing ALL 12 Pokemon from both teams.

            Sort them by BASE SPEED from highest to lowest.

            The report MUST include every Pokemon exactly once and its base Speed.

        D. TYPE COVERAGE / RESISTANCES
            Determine which attacking types are NOT resisted by ANY Pokemon on the
            opponent's team.

            This means a type qualifies only if NONE of the six opponent Pokemon
            resists that type.

            Use the Pokemon typing information returned by get_pokemon_info.
            Do not guess based on memory.

        7. ONLY after completing all of these steps should you produce the initial
        battle report.

        Do not replace this report with generic matchup advice, likely leads, threat
        analysis, or move recommendations unless the user explicitly asks for them.

        INITIAL REPORT FORMAT:

        When producing the initial battle report, use exactly these sections:

        1. Defensive Profile
        2. Offensive Profile
        3. Speed Order
        4. Types Not Resisted by Any Opponent Pokemon

        For Defensive Profile, state:
        - whether the team is more physically or specially defensive
        - the relevant base Defense and Special Defense comparisons

        For Offensive Profile, state:
        - whether the team is more physically or specially offensive
        - the relevant base Attack and Special Attack comparisons

        For Speed Order, list all 12 Pokemon from fastest to slowest in this format:

        1. Pokemon — Base Speed
        2. Pokemon — Base Speed
        3. Pokemon — Base Speed
        ...

        For Types Not Resisted by Any Opponent Pokemon, list the qualifying types.

        Do not omit a section.
        Do not substitute generic VGC analysis for any section.

        GET_POKEMON_INFO WORKFLOW:

        get_battle_state tells you WHICH Pokemon are in the battle.

        get_pokemon_info tells you the DETAILS about a specific Pokemon.

        Never use get_pokemon_info to discover which Pokemon are on a team.

        When comparing a group of Pokemon, retrieve information for each actual Pokemon
        name individually before comparing them.

        For example, if opponent_pokemon contains:

        ["Charizard", "Raichu", "Pelipper", "Sneasler", "Incineroar", "Whimsicott"]

        you must make six get_pokemon_info calls:

        get_pokemon_info("Charizard")
        get_pokemon_info("Raichu")
        get_pokemon_info("Pelipper")
        get_pokemon_info("Sneasler")
        get_pokemon_info("Incineroar")
        get_pokemon_info("Whimsicott")

        Do not make a single call using a descriptive phrase such as
        "opponent's fastest Pokemon".


        IMPORTANT TOOL USAGE RULES:

        1. Do not pass descriptive phrases as Pokemon names.

        For example, never call get_pokemon_info with values such as:
        - "opponent's fastest pokemon"
        - "my strongest pokemon"
        - "the fastest Pokemon"
        - "the Pokemon with the highest attack"

        get_pokemon_info requires the actual name of a Pokemon, such as
        "Incineroar", "Sneasler", or "Gholdengo".


        2. When a question requires comparing multiple Pokemon, first
        identify the actual Pokemon that need to be compared.

        For example, if the user asks:

        "What is the Speed stat of my opponent's fastest Pokemon?"

        you should:

        a. Call get_battle_state.
        b. Get the list of the opponent's Pokemon from the battle state.
        c. Call get_pokemon_info separately for each opponent Pokemon.
        d. Compare their Speed stats.
        e. Identify the Pokemon with the highest Speed stat.
        f. Return that Pokemon and its Speed stat.


        3. When comparing Pokemon based on a stat, always retrieve the
        actual Pokemon information before answering.

        Do not guess or infer which Pokemon has the highest stat based
        only on general Pokemon knowledge.

        For example:

        "What is my opponent's fastest Pokemon?"

        requires looking up the Speed stat for every relevant opponent
        Pokemon before determining the answer.


        4. If the user asks about "my Pokemon" or "my opponent's Pokemon",
        use get_battle_state first to determine which Pokemon are being
        referenced.

        Do not assume the Pokemon names from the user's question if the
        BattleState contains the authoritative list.


        5. Use get_pokemon_info for reliable base stats.

        When comparing stats such as Speed, Attack, Defense, Special
        Attack, Special Defense, or HP, retrieve the Pokemon information
        for the relevant Pokemon and use the returned stats.

        6. If the user tells you what pokemon the opponent has, you should use update_pokemon_battle_state to add each pokemon.

        7. When a user asks about the opponent's pokemon, call get_battle_state and use the

        IMPORTANT DAMAGE CALCULATION RULE:

        Whenever the user asks whether an attack will KO, how much damage
        an attack will do, a damage range, damage percentage, or whether
        an attack is super effective/resisted, you MUST use the
        calculate_damage tool.

        Do NOT calculate or estimate damage yourself from Pokemon data.

        Do NOT use get_pokemon_info as a substitute for calculate_damage
        when answering damage or KO questions.

        The calculate_damage tool is the authoritative source for all
        damage calculations and Pokemon Champions battle mechanics.

        When calling calculate_damage:
        - Use the Pokemon species provided by the user.
        - Use any nature, stat points, ability, item, boosts, or status
        explicitly provided by the user.
        - Omit fields that the user did not specify so the calculator's
        defaults can be used.
        - Include weather, terrain, and field effects when the user
        specifies them.

        When calling calculate_damage, only specify Pokemon attributes and
        battle conditions that are explicitly provided by the user or known
        from the current BattleState.

        Never invent or assume a weather, terrain, ability, item, status,
        stat investment, stat boost, or field condition.

        If a value is unknown, omit it and allow the calculator to use its
        default behavior.

        For field conditions, do not set terrain unless the user or
        BattleState explicitly indicates that terrain is active.

        For side conditions such as Friend Guard, place the condition on
        the correct side. If the user says Friend Guard is active on the
        defender side, use defenderSide.friendGuard = true.
        """

        self.tools = [

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

    def execute_tool(self, tool_call):
        """
        Execute a tool requested by the AI agent.
        """
        self.tool_call_history.append(
            {
                "name": tool_call.name,
                "arguments": tool_call.arguments
            }
        )

        arguments = json.loads(tool_call.arguments)

        if tool_call.name == "get_battle_state":
            return self.tool_dispatcher.get_battle_state()

        if tool_call.name == "get_pokemon_info":
            return self.tool_dispatcher.get_pokemon_info(
                pokemon_name=arguments["pokemon_name"]
            )
        
        if tool_call.name == "add_opponent_pokemon":
            return self.tool_dispatcher.add_opponent_pokemon(
                pokemon_names=arguments["pokemon_names"]
            )
        if tool_call.name == "update_pokemon_battle_state":
            return self.tool_dispatcher.update_pokemon_state(
                pokemon_name=arguments["pokemon_name"],
                side=arguments["side"],
                updates=arguments["updates"]
            )

        if tool_call.name == "update_battle_field":
            return self.tool_dispatcher.update_field(
                weather=arguments.get("weather"),
                terrain=arguments.get("terrain"),
                my_side=arguments.get("my_side"),
                opponent_side=arguments.get("opponent_side")
            )

        if tool_call.name == "calculate_damage":
            request = DamageCalculationRequest.from_dict(arguments)

            return self.tool_dispatcher.calculate_damage(
                request=request
            )

        raise ValueError(
            f"Unknown tool: {tool_call.name}"
        )

    def run(self, user_message):

        response = self.client.responses.create(
            model="gpt-5.6",
            instructions=self.instructions,
            input=user_message,
            tools=self.tools
        )

        while True:

            tool_calls = [
                item
                for item in response.output
                if item.type == "function_call"
            ]

            print(response.output)

            if not tool_calls:
                return response.output_text

            tool_outputs = []

            for tool_call in tool_calls:

                result = self.execute_tool(tool_call)

                tool_outputs.append(
                    {
                        "type": "function_call_output",
                        "call_id": tool_call.call_id,
                        "output": json.dumps(
                            result.to_dict() if hasattr(result, "to_dict") else result
                        )
                    }
                )

            response = self.client.responses.create(
                model="gpt-5.6",
                previous_response_id=response.id,
                input=tool_outputs
            )
