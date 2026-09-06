from agent.vgc_agent import VGCAgent
from tools.tool_dispatcher import ToolDispatcher

from services.pokemon_info_service import PokemonInfoService
from services.move_service import MoveService
from services.battle_state_service import BattleStateService
from services.damage_calc_service import DamageCalcService

from repositories.pokemon_repo import PokemonRepo
from repositories.move_repo import MoveRepo

from clients.pokeapi_client import PokeApiClient
from clients.damage_calc_client import DamageCalcClient

from models.battle_state import BattleState
from models.pokemon_state import PokemonState


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

    # --------------------------------------------------
    # Setup tool dispatcher
    # --------------------------------------------------

    tool_dispatcher = ToolDispatcher(
        pokemon_service=pokemon_service,
        battle_state_service=battle_state_service,
        damage_calc_service=damage_calc_service
    )

    # --------------------------------------------------
    # Create agent
    # --------------------------------------------------

    return VGCAgent(
        tool_dispatcher
    )