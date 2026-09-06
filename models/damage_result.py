from dataclasses import dataclass, field
from typing import Optional

@dataclass
class StatsResponse:
    hp: int
    atk: int
    def_: int
    spa: int
    spd: int
    spe: int

    @classmethod
    def from_dict(cls, data: dict) -> "StatsResponse":
        return cls(
            hp=data["hp"],
            atk=data["atk"],
            def_=data["def"],
            spa=data["spa"],
            spd=data["spd"],
            spe=data["spe"],
        )
    
    def to_dict(self) -> dict:
        return {
            "hp": self.hp,
            "atk": self.atk,
            "def": self.def_,
            "spa": self.spa,
            "spd": self.spd,
            "spe": self.spe,
        }


@dataclass
class PokemonDamageResponse:
    name: str
    stats: StatsResponse

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "stats": self.stats.to_dict(),
        }

    @classmethod
    def from_dict(cls, data: dict) -> "PokemonDamageResponse":
        return cls(
            name=data["name"],
            stats=StatsResponse.from_dict(data["stats"]),
        )


@dataclass
class MoveResponse:
    name: str
    power: int
    type: str
    category: str

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "power": self.power,
            "type": self.type,
            "category": self.category,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "MoveResponse":
        return cls(
            name=data["name"],
            power=data["power"],
            type=data["type"],
            category=data["category"],
        )


@dataclass
class DamageResponse:
    rolls: list[int]
    min: int
    max: int
    minPercent: float
    maxPercent: float

    def to_dict(self) -> dict:
        return {
            "rolls": self.rolls,
            "min": self.min,
            "max": self.max,
            "minPercent": self.minPercent,
            "maxPercent": self.maxPercent,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "DamageResponse":
        return cls(
            rolls=data["rolls"],
            min=data["min"],
            max=data["max"],
            minPercent=data["minPercent"],
            maxPercent=data["maxPercent"],
        )


@dataclass
class KoResponse:
    oneHit: bool
    twoHit: bool

    def to_dict(self) -> dict:
        return {
            "oneHit": self.oneHit,
            "twoHit": self.twoHit,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "KoResponse":
        return cls(
            oneHit=data["oneHit"],
            twoHit=data["twoHit"],
        )


@dataclass
class DamageCalculationResponse:
    attacker: PokemonDamageResponse
    defender: PokemonDamageResponse
    move: MoveResponse
    damage: DamageResponse
    ko: KoResponse

    def to_dict(self) -> dict:
        return {
            "attacker": self.attacker.to_dict(),
            "defender": self.defender.to_dict(),
            "move": self.move.to_dict(),
            "damage": self.damage.to_dict(),
            "ko": self.ko.to_dict(),
        }

    @classmethod
    def from_dict(cls, data: dict) -> "DamageCalculationResponse":
        return cls(
            attacker=PokemonDamageResponse.from_dict(data["attacker"]),
            defender=PokemonDamageResponse.from_dict(data["defender"]),
            move=MoveResponse.from_dict(data["move"]),
            damage=DamageResponse.from_dict(data["damage"]),
            ko=KoResponse.from_dict(data["ko"]),
        )