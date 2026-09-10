from dataclasses import dataclass
from typing import Callable
import traceback
from models.pokemon_state import PokemonState
from evals.eval_framework import EvalAssertions, EvalContext
from evals.eval_models import EvalResult


class AgentEvalRunner:

    def __init__(self, agent_factory: Callable):
        self.agent_factory = agent_factory
        self.results = []

    def run_eval(
        self,
        name: str,
        prompt: str,
        evaluator: Callable
    ):
        print(f"Running: {name}")

        agent = self.agent_factory()

        try:
            response = agent.run(prompt)

            result = evaluator(
                agent,
                response
            )

        except Exception as e:

            result = EvalResult(
                name=name,
                passed=False,
                tool_assertions=[]
            )

            print()
            print("=" * 60)
            print("ERROR")
            print("=" * 60)

            print(f"Error type: {type(e).__name__}")
            print(f"Error message: {e}")

            print()
            print("TRACEBACK:")
            traceback.print_exc()

            print("=" * 60)
            print()

        self.results.append(result)

        result.print()

        print()

    def print_summary(self):

        passed = sum(
            1
            for result in self.results
            if result.passed
        )

        total = len(self.results)

        print("=" * 50)
        print("EVAL SUMMARY")
        print("=" * 50)

        for result in self.results:

            status = (
                "PASS"
                if result.passed
                else "FAIL"
            )

            print(
                f"{status:5} "
                f"{result.name}"
            )

        print()
        print(f"Score: {passed}/{total}")

        if total:

            percentage = (
                passed / total
            ) * 100

            print(
                f"Percentage: {percentage:.1f}%"
            )

        print("=" * 50)


# ============================================================
# Battle State Evals
# ============================================================

def eval_opponent_team_entry(agent, response):

    context = create_eval_context(
        agent,
        response
    )

    assertions = EvalAssertions(context)

    expected_pokemon = {
        "charizard",
        "raichu",
        "pelipper",
        "sneasler",
        "incineroar",
        "whimsicott"
    }

    assertions.tool_was_called(
        "battle_state_agent",
        agent_name="orchestrator"
    )

    
    assertions.tool_was_called(
        "add_opponent_pokemon",
        agent_name="battle_state"
    ).with_argument(
            ["pokemon_names"],
            list(expected_pokemon)
        )
    
    return assertions.evaluate("eval_opponent_team_entry")

def eval_field_weather(agent, response):

    context = create_eval_context(
        agent,
        response
    )

    assertions = EvalAssertions(context)

    # check the we designated to the battle agent.
    assertions.tool_was_called(
        "battle_state_agent",
        agent_name="orchestrator"
    )

    
    assertions \
        .tool_was_called(
            "update_battle_field",
            agent_name="battle_state"
        ) \
        .with_argument(
            ["weather"],
            "sun"
        ) \
    
    return assertions.evaluate("eval_field_weather")

def eval_pokemon_state_item(agent, response):

    context = create_eval_context(
        agent,
        response
    )

    assertions = EvalAssertions(context)

    # check the we designated to the battle agent.
    assertions.tool_was_called(
        "battle_state_agent",
        agent_name="orchestrator"
    )

    # Check that the battle state agent
    # updated the Pokemon.
    assertions \
        .tool_was_called(
            "update_pokemon_battle_state",
            agent_name="battle_state"
        ) \
        .with_argument(
            ["pokemon_name"],
            "Whimsicott"
        ) \
        .with_argument(
            ["side"],
            "my"
        ) \
        .with_argument(
            ["updates", "item"],
            "Light Clay"
        )
    
    return assertions.evaluate("eval_pokemon_state_item")


def eval_tailwind(agent, response):

    context = create_eval_context(
        agent,
        response
    )

    assertions = EvalAssertions(context)

    # Check that the orchestrator delegated
    # to the battle state agent.
    assertions.tool_was_called(
        "battle_state_agent",
        agent_name="orchestrator"
    )


    # Check that Tailwind was updated.
    assertions \
        .tool_was_called(
            "update_battle_field",
            agent_name="battle_state"
        ) \
        .with_argument(
            ["my_side", "tailwind"],
            True
        )


    return assertions.evaluate(
        "eval_tailwind"
    )

def eval_reflect(agent, response):

    context = create_eval_context(
        agent,
        response
    )

    assertions = EvalAssertions(context)

    # Check orchestrator delegation.
    assertions.tool_was_called(
        "battle_state_agent",
        agent_name="orchestrator"
    )


    # Check Reflect was updated.
    assertions \
        .tool_was_called(
            "update_battle_field",
            agent_name="battle_state"
        ) \
        .with_argument(
            ["opponent_side", "reflect"],
            True
        )


    return assertions.evaluate(
        "eval_reflect"
    )

def eval_field_weather(agent, response):

    context = create_eval_context(
        agent,
        response
    )

    assertions = EvalAssertions(context)

    # check the we designated to the battle agent.
    assertions.tool_was_called(
        "battle_state_agent",
        agent_name="orchestrator"
    )

    
    assertions \
        .tool_was_called(
            "update_battle_field",
            agent_name="battle_state"
        ) \
        .with_argument(
            ["weather"],
            "sun"
        ) \
    
    return assertions.evaluate("eval_field_weather")


# --------------------------------------------------
# Pokemon Info Evals
# --------------------------------------------------


def eval_pokemon_stats(agent, response):

    context = create_eval_context(
        agent,
        response
    )

    assertions = EvalAssertions(context)

    # check the we designated to the battle agent.
    assertions.tool_was_called(
        "pokemon_info_agent",
        agent_name="orchestrator"
    )

    
    assertions \
        .tool_was_called(
            "get_pokemon_info",
            agent_name="pokemon_info"
        ) \
        .with_argument(
            ["pokemon_name"],
            "Charizard"
        ) \
    
    return assertions.evaluate("eval_pokemon_stats")

def eval_pokemon_moves(agent, response):

    context = create_eval_context(
        agent,
        response
    )

    assertions = EvalAssertions(context)

    # check the we designated to the battle agent.
    assertions.tool_was_called(
        "pokemon_info_agent",
        agent_name="orchestrator"
    )
    
    assertions \
        .tool_was_called(
            "get_pokemon_info",
            agent_name="pokemon_info"
        ) \
        .with_argument(
            ["pokemon_name"],
            "Charizard"
        ) \
    
    return assertions.evaluate("eval_pokemon_moves")


def eval_fastest_opponent(agent, response):

    context = EvalContext(
        agent=agent,
        response=response
    )

    assertions = EvalAssertions(context)

    return (
        assertions
        .tool_was_called(
            "get_battle_state"
        )

        .tool_was_called(
            "get_pokemon_info"
        )
        .with_argument(
            ["pokemon_name"],
            "charizard"
        )

        .tool_was_called(
            "get_pokemon_info"
        )
        .with_argument(
            ["pokemon_name"],
            "raichu"
        )

        .tool_was_called(
            "get_pokemon_info"
        )
        .with_argument(
            ["pokemon_name"],
            "pelipper"
        )

        .tool_was_called(
            "get_pokemon_info"
        )
        .with_argument(
            ["pokemon_name"],
            "sneasler"
        )

        .tool_was_called(
            "get_pokemon_info"
        )
        .with_argument(
            ["pokemon_name"],
            "incineroar"
        )

        .tool_was_called(
            "get_pokemon_info"
        )
        .with_argument(
            ["pokemon_name"],
            "whimsicott"
        )

        .passed()
    )

# ============================================================
# Damage Calc Evals
# ============================================================

def eval_damage_calculation(agent, response):

    context = create_eval_context(
        agent,
        response
    )

    assertions = EvalAssertions(context)

    assertions \
        .tool_was_called(
            "battle_state_agent",
            agent_name="orchestrator"
        )

    assertions \
        .tool_was_called(
            "get_battle_state",
            agent_name="battle_state"
        )    

    assertions \
        .tool_was_called(
            "damage_calc_agent",
            agent_name="orchestrator"
        )

    assertions \
        .tool_was_called(
            "calculate_damage",
            agent_name="damage_calc"
        ) \
        .with_argument(
            ["attacker", "species"],
            "Incineroar"
        ) \
        .with_argument(
            ["attacker", "nature"],
            "Adamant"
        ) \
        .with_argument(
            ["attacker", "item"],
            "Life Orb"
        ) \
        .with_argument(
            ["move", "name"],
            "Flare Blitz"
        ) \
        .with_argument(
            ["field", "weather"],
            "Sun"
        ) 

    return assertions.evaluate("eval_damage_calculation")

# Tests that it can load information from battle state.
def eval_damage_calculation_with_battle_state(agent, response):

    context = create_eval_context(
        agent,
        response
    )

    assertions = EvalAssertions(context)

    assertions \
        .tool_was_called(
            "battle_state_agent",
            agent_name="orchestrator"
        )

    assertions \
        .tool_was_called(
            "get_battle_state",
            agent_name="battle_state"
        )    

    assertions \
        .tool_was_called(
            "damage_calc_agent",
            agent_name="orchestrator"
        )

    assertions \
        .tool_was_called(
            "calculate_damage",
            agent_name="damage_calc"
        ) \
        .with_argument(
            ["attacker", "species"],
            "Incineroar"
        ) \
        .with_argument(
            ["attacker", "nature"],
            "Adamant"
        ) \
        .with_argument(
            ["attacker", "item"],
            "Life Orb"
        ) \
        .with_argument(
            ["move", "name"],
            "Flare Blitz"
        ) \
        .with_argument(
            ["defender", "species"],
            "Whimsicott"
        ) \
        .with_argument(
            ["defender", "nature"],
            "Modest"
        ) \
        .with_argument(
            ["defender", "statPoints", "spd"],
            32
        ) \
        .with_argument(
            ["field", "weather"],
            "None"
        ) 
        

    return assertions.evaluate("eval_damage_calculation_with_battle_state")


# ============================================================
# AGENT FACTORY
# ============================================================

def create_agent():

    from agent.agent_factory import create_agent

    my_pokemon = [
        PokemonState(
            name="Froslass-Mega",
            nature="Modest",
            evs={
                "hp": 32,
                "spa": 32
            }
        ),
        PokemonState(
            name="Whimsicott",
            nature="Modest",
            evs={
                "spd": 32,
                "spa": 32
            }
        ),
        PokemonState(
            name="Aerodactyl"
        ),
        PokemonState(
            name="Gholdengo",
            nature="Modest",
            item="Life Orb",
            evs={
                "spd": 32,
                "spa": 32
            }
        ),
        PokemonState(
            name="Raichu"
        ),
        PokemonState(
            name="Pelipper"
        )
    ]

    opponent_pokemon = []

    return create_agent(
        my_pokemon,
        opponent_pokemon
    )

def create_eval_context(
    agent,
    response
):

    return EvalContext(
        agents={
            "orchestrator": agent,

            "battle_state":
                agent.tool_dispatcher.battle_state_agent,

            "damage_calc":
                agent.tool_dispatcher.damage_calc_agent,

            "pokemon_info":
                agent.tool_dispatcher.pokemon_info_agent
        },

        response=response
    )


# ============================================================
# RUN EVALS
# ============================================================

if __name__ == "__main__":

    runner = AgentEvalRunner(
        agent_factory=create_agent
    )

    # runner.run_eval(
    #     name="opponent_team_entry",
    #     prompt=(
    #         "My opponent has charizard, raichu, pelipper, "
    #         "sneasler, incineroar, and whimsicott. "
    #         "Please note this in the battle state."
    #     ),
    #     evaluator=eval_opponent_team_entry
    # )

    # runner.run_eval(
    #     name="eval_field_weather",
    #     prompt=(
    #         "My opponent has set up the sun."
    #     ),
    #     evaluator=eval_field_weather
    # )

    # runner.run_eval(
    #     name="eval_pokemon_state_item",
    #     prompt=(
    #         "My whimsicott is holding the light clay item."
    #     ),
    #     evaluator=eval_pokemon_state_item
    # )

    # runner.run_eval(
    #     name="tailwind",
    #     prompt=(
    #         "I set up Tailwind on my side. "
    #         "Please note this in the battle state."
    #     ),
    #     evaluator=eval_tailwind
    # )

    # runner.run_eval(
    #     name="reflect",
    #     prompt=(
    #         "The opponent has set up Reflect. "
    #         "Please note this in the battle state."
    #     ),
    #     evaluator=eval_reflect
    # )

    # runner.run_eval(
    #     name="pokemon stats",
    #     prompt=(
    #         "How fast is Charizard?"
    #     ),
    #     evaluator=eval_pokemon_stats
    # )

    # runner.run_eval(
    #     name="pokemon moves",
    #     prompt=(
    #         "What moves does Charizard have?"
    #     ),
    #     evaluator=eval_pokemon_moves
    # )

    # runner.run_eval(
    #     name="fastest_opponent",
    #     prompt=(
    #         "My opponent has charizard, raichu, pelipper, "
    #         "sneasler, incineroar, and whimsicott. "
    #         "Which one has the highest base Speed?"
    #     ),
    #     evaluator=eval_fastest_opponent
    # )

    # runner.run_eval(
    #     name="damage_calculation",
    #     prompt=(
    #         "Can Adamant 32-attack-point Incineroar holding a life orb KO "
    #         "a 0-stat-point Sneasler with Flare Blitz "
    #         "while the sun is up?"
    #     ),
    #     evaluator=eval_damage_calculation
    # )

    runner.run_eval(
        name="damage_calculation with battle state",
        prompt=(
            "Can Adamant 32-attack-point Incineroar holding a life orb KO "
            "my whimsicott with Flare Blitz?"
        ),
        evaluator=eval_damage_calculation_with_battle_state
    )

    # runner.run_eval(
    #     name="no_invented_terrain",
    #     prompt=(
    #         "Can Adamant 32-attack-point Incineroar KO "
    #         "a 0-stat-point Sneasler with Flare Blitz "
    #         "while the sun is up?"
    #     ),
    #     evaluator=eval_no_invented_terrain
    # )

    # runner.run_eval(
    #     name="initial_team_report",
    #     prompt=(
    #         "My opponent has charizard, raichu, pelipper, "
    #         "sneasler, incineroar, and whimsicott. "
    #         "Give me the initial team report."
    #     ),
    #     evaluator=eval_initial_team_report
    # )

    runner.print_summary()