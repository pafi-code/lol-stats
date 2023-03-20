"""Module to predict if a summoner is a smurf."""

from lol_stats import data

from . import _utils

_MAX_SMURF_LEVEL = 60


def portion_games_with_smurfs_in_game(games: data.Games) -> float:
    """
    Calculate the portion of games where smurfs are present.

    Parameters
    ----------
    games
        The games that should be analyzed.


    Returns
    -------
    float
        The portion.
    """
    counter = 0
    for game in games.games:
        if _utils.is_smurf_in_game(game):
            counter += 1
    return counter / len(games.games)


def is_smurf(summoner: data.SummonerInGame) -> bool:
    """Check if a summoner is a smurf."""
    if summoner.level <= _MAX_SMURF_LEVEL:
        return True
    return False
