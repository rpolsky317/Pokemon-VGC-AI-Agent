from agent.vgc_agent import VGCAgent
from agent.orchestrator_agent import OrchestratorAgent
from tools.tool_dispatcher import ToolDispatcher
from tools.battle_state_tools_dispatcher import BattleStateToolsDispatcher
from tools.pokemon_info_tools_dispatcher import PokemonInfoToolDispatcher
from tools.damage_calc_tool_dispatcher import DamageCalcToolDispatcher
from tools.orchestrator_tool_dispatcher import OrchestratorToolDispatcher

from services.pokemon_info_service import PokemonInfoService
from services.move_service import MoveService
from services.battle_state_service import BattleStateService
from services.damage_calc_service import DamageCalcService

from repositories.pokemon_repo import PokemonRepo
from repositories.move_repo import MoveRepo

from clients.pokeapi_client import PokeApiClient
from clients.damage_calc_client import DamageCalcClient

from models.battle_state import BattleState

from agent.battle_state_agent import BattleStateAgent
from agent.pokemon_info_agent import PokemonInfoAgent
from agent.damage_calc_agent import DamageCalcAgent


def create_agent(
    my_pokemon=None,
    opponent_pokemon=None
) -> VGCAgent:
    # --------------------------------------------------
    # Setup Pokemon information services
    # --------------------------------------------------

    pokemon_repo = PokemonRepo()
    move_repo = MoveRepo()

    pokeapi_client = PokeApiClient()

    move_service = MoveService(
        move_repo,
        pokeapi_client
    )

    pokemon_service = PokemonInfoService(
        pokemon_repo,
        pokeapi_client,
        move_service
    )

    # --------------------------------------------------
    # Setup initial battle state
    # --------------------------------------------------

    battle_state = BattleState(
        my_pokemon,
        opponent_pokemon
    )

    battle_state_service = BattleStateService(
        battle_state
    )

    # --------------------------------------------------
    # Setup damage calculator
    # --------------------------------------------------

    damage_calc_client = DamageCalcClient(
        base_url="http://localhost:3000"
    )

    damage_calc_service = DamageCalcService(
        damage_calc_client
    )

    

    # -----------------------------------------
    # Battle State Agent
    # -----------------------------------------

    battle_state_tool_dispatcher = BattleStateToolsDispatcher(
        battle_state_service=battle_state_service,
    )

    battle_state_agent = BattleStateAgent(
        battle_state_tool_dispatcher
    )

    # -----------------------------------------
    # Pokemon Information Agent
    # -----------------------------------------

    pokemon_info_tool_dispatcher = PokemonInfoToolDispatcher(
        pokemon_service=pokemon_service,
    )

    pokemon_info_agent = PokemonInfoAgent(
        pokemon_info_tool_dispatcher
    )

    # -----------------------------------------
    # Damage Calc Agent
    # -----------------------------------------

    damage_calc_tool_dispatcher = DamageCalcToolDispatcher(
        damage_calc_service=damage_calc_service,
    )

    damage_calc_agent = DamageCalcAgent(
        damage_calc_tool_dispatcher
    )

    # --------------------------------------------------
    # Setup tool dispatcher
    # --------------------------------------------------

    tool_dispatcher = OrchestratorToolDispatcher(
        battle_state_agent=battle_state_agent,
        pokemon_info_agent=pokemon_info_agent,
        damage_calc_agent=damage_calc_agent

    )

    # tool_dispatcher = ToolDispatcher(
    #     pokemon_service=pokemon_service,
    #     battle_state_service=battle_state_service,
    #     damage_calc_service=damage_calc_service,
    # )

    # --------------------------------------------------
    # Create agent
    # --------------------------------------------------

    # return VGCAgent(
    #     tool_dispatcher=tool_dispatcher,
    #     battle_state_agent=battle_state_agent
    # )

    return OrchestratorAgent(
            tool_dispatcher=tool_dispatcher
        )