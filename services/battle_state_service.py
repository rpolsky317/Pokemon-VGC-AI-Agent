class BattleStateService:

    def __init__(self, battle_state):
        self.battle_state = battle_state

    def get_battle_state(self):
        return self.battle_state.to_dict()
    
    def add_opponent_pokemon(self, pokemon_names):
        self.battle_state.add_opponent_pokemon(pokemon_names)

    def update_pokemon(
        self,
        pokemon_name,
        side,
        **updates
    ):
        self.battle_state.update_pokemon(
            pokemon_name=pokemon_name,
            side=side,
            **updates
        )

    def update_hp(
        self,
        pokemon_name,
        side,
        hp_percent
    ):
        self.battle_state.update_hp(
            pokemon_name=pokemon_name,
            side=side,
            hp_percent=hp_percent
        )

    def update_boosts(
        self,
        pokemon_name,
        side,
        boosts
    ):
        self.battle_state.update_boosts(
            pokemon_name=pokemon_name,
            side=side,
            boosts=boosts
        )

    def update_field(
        self,
        weather=None,
        terrain=None,
        my_side=None,
        opponent_side=None
    ):
        self.battle_state.field.update_field(
            weather=weather,
            terrain=terrain,
            my_side=my_side,
            opponent_side=opponent_side
        )

        #return self.battle_state.field.to_dict()