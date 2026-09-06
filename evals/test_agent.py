from dataclasses import dataclass
from typing import Callable

from models.pokemon_state import PokemonState
from evals.eval_framework import EvalAssertions, EvalContext


@dataclass
class EvalResult:
    name: str
    passed: bool
    reason: str
    subtest_results: list[str]


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

            print(f"  EXCEPTION - {e}")

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
# EVALS
# ============================================================

def eval_opponent_team_entry(agent, response):

    context = EvalContext(
        agent=agent,
        response=response
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

    
    assertions \
        .tool_was_called("add_opponent_pokemon") \
        .with_argument(
            ["pokemon_names"],
            list(expected_pokemon)
        )
    
    return assertions.evaluate("eval_opponent_team_entry")


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


def eval_damage_calculation(agent, response):

    context = EvalContext(
        agent=agent,
        response=response
    )

    assertions = EvalAssertions(context)

    assertions \
        .tool_was_called("calculate_damage") \
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
        )

    assertions \
        .tool_was_called("get_battle_state")

    return assertions.evaluate("eval_damage_calculation")


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


# ============================================================
# RUN EVALS
# ============================================================

if __name__ == "__main__":

    runner = AgentEvalRunner(
        agent_factory=create_agent
    )

    runner.run_eval(
        name="opponent_team_entry",
        prompt=(
            "My opponent has charizard, raichu, pelipper, "
            "sneasler, incineroar, and whimsicott. "
            "Please note this in the battle state."
        ),
        evaluator=eval_opponent_team_entry
    )

    # runner.run_eval(
    #     name="fastest_opponent",
    #     prompt=(
    #         "My opponent has charizard, raichu, pelipper, "
    #         "sneasler, incineroar, and whimsicott. "
    #         "Which one has the highest base Speed?"
    #     ),
    #     evaluator=eval_fastest_opponent
    # )

    runner.run_eval(
        name="damage_calculation",
        prompt=(
            "Can Adamant 32-attack-point Incineroar holding a life orb KO "
            "a 0-stat-point Sneasler with Flare Blitz "
            "while the sun is up?"
        ),
        evaluator=eval_damage_calculation
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