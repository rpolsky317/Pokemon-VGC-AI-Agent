from dataclasses import dataclass, field
from typing import Optional


@dataclass
class StatPoints:
    hp: int = 0
    atk: int = 0
    def_: int = 0
    spa: int = 0
    spd: int = 0
    spe: int = 0

    def to_dict(self) -> dict:
        return {
            "hp": self.hp,
            "atk": self.atk,
            "def": self.def_,
            "spa": self.spa,
            "spd": self.spd,
            "spe": self.spe,
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "StatPoints":
        return cls(
            hp=data.get("hp", 0),
            atk=data.get("atk", 0),
            def_=data.get("def", 0),
            spa=data.get("spa", 0),
            spd=data.get("spd", 0),
            spe=data.get("spe", 0),
        )


@dataclass
class StatBoosts:
    atk: int = 0
    def_: int = 0
    spa: int = 0
    spd: int = 0
    spe: int = 0

    def to_dict(self) -> dict:
        return {
            "atk": self.atk,
            "def": self.def_,
            "spa": self.spa,
            "spd": self.spd,
            "spe": self.spe,
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "StatBoosts":
        return cls(
            atk=data.get("atk", 0),
            def_=data.get("def", 0),
            spa=data.get("spa", 0),
            spd=data.get("spd", 0),
            spe=data.get("spe", 0),
        )


@dataclass
class PokemonInput:
    species: str
    ability: Optional[str] = None
    item: Optional[str] = None
    nature: Optional[str] = None
    statPoints: StatPoints = field(default_factory=StatPoints)
    boosts: StatBoosts = field(default_factory=StatBoosts)
    status: Optional[str] = None

    def to_dict(self) -> dict:
        result = {
            "species": self.species,
            "statPoints": self.statPoints.to_dict(),
            "boosts": self.boosts.to_dict(),
        }

        if self.ability is not None:
            result["ability"] = self.ability

        if self.item is not None:
            result["item"] = self.item

        if self.nature is not None:
            result["nature"] = self.nature

        if self.status is not None:
            result["status"] = self.status

        return result
    
    @classmethod
    def from_dict(cls, data: dict) -> "PokemonInput":
        return cls(
            species=data["species"],
            ability=data.get("ability"),
            item=data.get("item"),
            nature=data.get("nature"),
            statPoints=StatPoints.from_dict(
                data.get("statPoints", {})
            ),
            boosts=StatBoosts.from_dict(
                data.get("boosts", {})
            ),
            status=data.get("status"),
        )


@dataclass
class MoveInput:
    name: str

    def to_dict(self) -> dict:
        return {
            "name": self.name
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "MoveInput":
        return cls(
            name=data["name"]
        )


@dataclass
class SideFieldInput:
    reflect: bool = False
    lightScreen: bool = False
    auroraVeil: bool = False
    protected: bool = False
    seeded: bool = False
    charge: bool = False
    helpingHand: bool = False
    tailwind: bool = False
    friendGuard: bool = False
    battery: bool = False
    powerSpot: bool = False
    steelySpirit: bool = False
    flowerGift: bool = False

    def to_dict(self) -> dict:
        return {
            "reflect": self.reflect,
            "lightScreen": self.lightScreen,
            "auroraVeil": self.auroraVeil,
            "protected": self.protected,
            "seeded": self.seeded,
            "charge": self.charge,
            "helpingHand": self.helpingHand,
            "tailwind": self.tailwind,
            "friendGuard": self.friendGuard,
            "battery": self.battery,
            "powerSpot": self.powerSpot,
            "steelySpirit": self.steelySpirit,
            "flowerGift": self.flowerGift,
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "SideFieldInput":
        return cls(
            reflect=data.get("reflect", False),
            lightScreen=data.get("lightScreen", False),
            auroraVeil=data.get("auroraVeil", False),
            protected=data.get("protected", False),
            seeded=data.get("seeded", False),
            charge=data.get("charge", False),
            helpingHand=data.get("helpingHand", False),
            tailwind=data.get("tailwind", False),
            friendGuard=data.get("friendGuard", False),
            battery=data.get("battery", False),
            powerSpot=data.get("powerSpot", False),
            steelySpirit=data.get("steelySpirit", False),
            flowerGift=data.get("flowerGift", False),
        )


@dataclass
class FieldInput:
    weather: Optional[str] = None
    terrain: Optional[str] = None
    magicRoom: bool = False
    wonderRoom: bool = False
    attackerSide: SideFieldInput = field(
        default_factory=SideFieldInput
    )
    defenderSide: SideFieldInput = field(
        default_factory=SideFieldInput
    )

    def to_dict(self) -> dict:
        return {
            "weather": self.weather,
            "terrain": self.terrain,
            "magicRoom": self.magicRoom,
            "wonderRoom": self.wonderRoom,
            "attackerSide": self.attackerSide.to_dict(),
            "defenderSide": self.defenderSide.to_dict(),
        }
    
    @classmethod 
    def from_dict(cls, data: dict) -> FieldInput:
        return cls( 
            weather=data.get("weather"), 
            terrain=data.get("terrain"), 
            magicRoom=data.get("magicRoom", False), 
            wonderRoom=data.get("wonderRoom", False), 
            attackerSide=SideFieldInput.from_dict( data.get("attackerSide", {}) ), 
            defenderSide=SideFieldInput.from_dict( data.get("defenderSide", {}) )
        )


@dataclass
class DamageCalculationRequest:
    attacker: PokemonInput
    defender: PokemonInput
    move: MoveInput
    field: FieldInput = field(default_factory=FieldInput)

    def to_dict(self) -> dict:
        return {
            "attacker": self.attacker.to_dict(),
            "defender": self.defender.to_dict(),
            "move": self.move.to_dict(),
            "field": self.field.to_dict(),
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "DamageCalculationRequest":
        return cls(
            attacker=PokemonInput.from_dict(data["attacker"]),
            defender=PokemonInput.from_dict(data["defender"]),
            move=MoveInput.from_dict(data["move"]),
            field=FieldInput.from_dict(data.get("field", {})),
        )
    
    