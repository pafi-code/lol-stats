"""Module to download data from the league of legends API."""

from ._get_games_of_summoner import get_games_by_summoner_puuid
from ._get_summoner import get_summoner_by_name
from ._regions import Region

__all__ = ["get_summoner_by_name", "get_games_by_summoner_puuid", "Region"]
