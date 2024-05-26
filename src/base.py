from enum import Enum, EnumType
from typing import Dict, Optional


class Provider(Enum):
	betway = "https://betway.com/en/sports"


class BetwaySports(Enum):
	ice_hockey = "ice-hockey"
	soccer = "soccer"
	basketball = "basketball"
	baseball = "baseball"


class BetwayBasketball(Enum):
	nba = "usa/nba"
	ncaa = "usa/ncaab"
	bbl = "germany/bbl"


ENUM_MAPPING: Dict[EnumType, Enum] = {
	Provider: 0,
	BetwayBasketball: BetwaySports.basketball,
	BetwaySports: Provider.betway,
}


def generate_url(value) -> str:
	v = ENUM_MAPPING.get(value)
	if v is None:
		raise ValueError(f"{value.name} not in the mapping")
	if v == 0:
		return value.value

	return "/".join(generate_url(v), value.value)
