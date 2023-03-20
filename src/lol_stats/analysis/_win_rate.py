"""Module to calculate different kind of winrates."""

from lol_stats import data

from . import _smurf_detection


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
        if game.blue_team.is_my_team and game.blue_team.won:
            win_counter += 1
        if game.red_team.is_my_team and game.red_team.won:
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
        enemies = _get_enemy_team(game)
        my_team = _get_my_team(game)
        if not _is_smurf_in_enemy_team(enemies) and not _is_smurf_in_enemy_team(
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
        enemies = _get_enemy_team(game)
        if _is_smurf_in_enemy_team(enemies):
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
        my_team = _get_my_team(game)
        if _is_smurf_in_enemy_team(my_team):
            if my_team.won:
                wins += 1
            else:
                loss += 1
    return wins / (wins + loss)


def _get_my_team(game: data.Game) -> data.Team:
    """Get my team."""
    if game.blue_team.is_my_team:
        return game.blue_team
    return game.red_team


def _get_enemy_team(game: data.Game) -> data.Team:
    """Get the enemy team."""
    if not game.blue_team.is_my_team:
        return game.blue_team
    return game.red_team


def _is_smurf_in_enemy_team(team: data.Team) -> bool:
    """Check if a smurf is in the enemy team."""
    return any(_smurf_detection.is_smurf(summoner) for summoner in team.summoners)
