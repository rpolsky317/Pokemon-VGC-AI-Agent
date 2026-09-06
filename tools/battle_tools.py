

class battle_tools:

    def get_battle_state():
        """
        Returns the current state of the Pokemon battle.
        """

        return {
            "my_active_pokemon": [
                {
                    "pokemon": "Rillaboom",
                    "hp_percent": 100
                },
                {
                    "pokemon": "Whimsicott",
                    "hp_percent": 100
                }
            ],
            "opponent_active_pokemon": [
                {
                    "pokemon": "Gholdengo",
                    "hp_percent": 100
                },
                {
                    "pokemon": "Whimsicott",
                    "hp_percent": 100
                }
            ]
        }