"""Data definition of a summoner."""

import enum

import pydantic


class TeamType(enum.Enum):
    """Possible teams in lol."""

    BLUE = 100
    RED = 200


class Role(enum.Enum):
    """Definition of different roles in the game."""

    SUPPPORT = "UTILITY"
    BOTTOM = "BOTTOM"
    MID = "MIDDLE"
    TOP = "TOP"
    JUNGLE = "JUNGLE"
    INVALID = ""


class ChampionInfo(pydantic.BaseModel):
    """Information about the champion that a summoner was playing."""

    champion_id: int
    champion_experience: int


class GameStats(pydantic.BaseModel):
    """Information about the game that the summoner was inside."""

    kills: int
    deaths: int
    assists: int
    gold_earned: int
    minions: int
    role: Role

    class Config:
        """Configure pydantic to allow enums."""

        use_enum_values = True


class Summoner(pydantic.BaseModel):
    """Defintion of a summoner outside of a game."""

    puuid: str
    name: str
    level: int


class SummonerInGame(Summoner):
    """Definition of a summoner in a game."""

    champion_info: ChampionInfo
    game_stats: GameStats
    team: TeamType
    is_me: bool
    won: bool

    class Config:
        """Configure pydantic to allow enums."""

        use_enum_values = True
