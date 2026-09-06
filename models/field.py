class Field:
    def __init__(
        self,
        game_type="Doubles",
        weather=None,
        terrain=None,
        my_side=None,
        opponent_side=None
    ):
        self.game_type = game_type
        self.weather = weather
        self.terrain = terrain

        self.my_side = my_side or SideState()
        self.opponent_side = opponent_side or SideState()

    def update_field(
        self,
        weather=None,
        terrain=None,
        my_side=None,
        opponent_side=None
    ):
        if weather is not None:
            self.weather = weather

        if terrain is not None:
            self.terrain = terrain

        if my_side is not None:
            for attribute, value in my_side.items():
                if not hasattr(self.my_side, attribute):
                    raise ValueError(
                        f"SideState has no attribute '{attribute}'."
                    )

                setattr(self.my_side, attribute, value)

        if opponent_side is not None:
            for attribute, value in opponent_side.items():
                if not hasattr(self.opponent_side, attribute):
                    raise ValueError(
                        f"SideState has no attribute '{attribute}'."
                    )

                setattr(self.opponent_side, attribute, value)


    def to_dict(self):
        return {
            "game_type": self.game_type,
            "weather": self.weather,
            "terrain": self.terrain,
            "my_side": self.my_side.to_dict(),
            "opponent_side": self.opponent_side.to_dict()
        }

class SideState:
    def __init__(
        self,
        reflect=False,
        light_screen=False,
        aurora_veil=False,
        tailwind=False
    ):
        self.reflect = reflect
        self.light_screen = light_screen
        self.aurora_veil = aurora_veil
        self.tailwind = tailwind

    def to_dict(self):
        return {
            "reflect": self.reflect,
            "light_screen": self.light_screen,
            "aurora_veil": self.aurora_veil,
            "tailwind": self.tailwind
        }