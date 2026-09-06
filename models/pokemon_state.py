class PokemonState:
    
    def __init__(
        self,
        name,
        level=50,
        nature=None,
        ability=None,
        item=None,
        evs=None,
        ivs=None,
        boosts=None,
        hp_percent=100
    ):
        self.name = name
        self.level = level
        self.nature = nature
        self.ability = ability
        self.item = item
        self.evs = evs or {}
        self.ivs = ivs or {}
        self.boosts = boosts or {}
        self.hp_percent = hp_percent

    def to_dict(self):
        return {
            "name": self.name,
            "level": self.level,
            "nature": self.nature,
            "ability": self.ability,
            "item": self.item,
            "evs": self.evs,
            "ivs": self.ivs,
            "boosts": self.boosts,
            "hp_percent": self.hp_percent
        }