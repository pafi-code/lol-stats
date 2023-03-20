"""Module to predict if a summoner is a smurf."""

from collections import defaultdict

from lol_stats import data

from . import _utils


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


def count_amount_of_smurf_per_game(games: data.Games) -> dict[int, int]:
    """
    Calculate the number of smurfs in a game.

    Parameters
    ----------
    games
        The games that should be analyzed.


    Returns
    -------
    dict[int, int]
        Mapping from amount of smurfs to number of games.
    """
    counts: dict[int, int] = defaultdict(lambda: 0)
    for game in games.games:
        counts[_utils.count_smurf_in_game(game)] += 1
    return dict(sorted(counts.items(), key=lambda item: item[0]))
