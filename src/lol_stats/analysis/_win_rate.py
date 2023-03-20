"""Module to calculate different kind of winrates."""

from lol_stats import data

from . import _utils


def get_general_win_rate(games: data.Games) -> float:
    """
    Calculate your over all win rate.

    Parameters
    ----------
    games
        The games that should be used to calculate the score.

    Returns
    -------
    float
        The general win rate.
    """
    win_counter = 0
    for game in games.games:
        if _utils.get_my_team(game).won:
            win_counter += 1
    return win_counter / len(games.games)


def get_win_rate_without_smurfs_in_game(games: data.Games) -> float:
    """
    Calculate your winrate when no smurfs are in the game.

    Parameters
    ----------
    games
        The games that should be analyzed.


    Returns
    -------
    float
        Your winrate if no smurfs are in the game.
    """
    wins = 0
    loss = 0
    for game in games.games:
        enemies = _utils.get_enemy_team(game)
        my_team = _utils.get_my_team(game)
        if not _utils.is_smurf_in_team(enemies) and not _utils.is_smurf_in_team(
            my_team,
        ):
            if my_team.won:
                wins += 1
            else:
                loss += 1
    return wins / (wins + loss)


def get_win_rate_against_smurfs(games: data.Games) -> float:
    """
    Calculate the winrate if a smurf is in the enemy team.

    Parameters
    ----------
    games
        The games that should be used for calculation.


    Returns
    -------
    float
        The win rate if smurfs are in the enemy team.
    """
    wins = 0
    loss = 0
    for game in games.games:
        enemies = _utils.get_enemy_team(game)
        if _utils.is_smurf_in_team(enemies):
            if enemies.won:
                loss += 1
            else:
                wins += 1
    return wins / (wins + loss)


def get_win_rate_with_smurfs(games: data.Games) -> float:
    """
    Calculate the winrate if a smurf is in my team.

    Parameters
    ----------
    games
        The games that should be used for calculation.


    Returns
    -------
    float
        The win rate if smurfs are in my team.
    """
    wins = 0
    loss = 0
    for game in games.games:
        my_team = _utils.get_my_team(game)
        if _utils.is_smurf_in_team(my_team):
            if my_team.won:
                wins += 1
            else:
                loss += 1
    return wins / (wins + loss)
