from models.battle_state import BattleState

class UpdateBattleStateTests:

    def init(self):
        self.battle_state = BattleState(
            my_pokemon=[
                "Rillaboom",
                "Whimsicott",
                "Gholdengo",
                "Palafin",
                "Raichu",
                "Pelipper"
            ],
            opponent_pokemon=[
                "Sneasler",
                "Incineroar",
                "Gholdengo",
                "Amoonguss",
                "Dragonite",
                "Urshifu"
            ])

    def UpdateItem(self):
    
        self.battle_state.update_pokemon(
            "Gholdengo",
            "opponent",
            item="Life Orb"
        )

    def UpdateAbility(self):      
        self.battle_state.update_pokemon(
            "Sneasler",
            "opponent",
            ability="Unburden"
        )

    def UpdateBoosts(self):      
        self.battle_state.update_boosts(
            "Sneasler",
            "opponent",
            {"atk": 1}
        )

    def UpdateField(self):      
        self.battle_state.update_field(
                weather="Rain",
                terrain="Grassy"
        )
