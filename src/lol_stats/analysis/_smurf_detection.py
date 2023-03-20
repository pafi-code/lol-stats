"""Module to predict if a summoner is a smurf."""

from lol_stats import data

_MAX_SMURF_LEVEL = 60


def is_smurf(summoner: data.SummonerInGame) -> bool:
    """Check if a summoner is a smurf."""
    if summoner.level <= _MAX_SMURF_LEVEL:
        return True
    return False
