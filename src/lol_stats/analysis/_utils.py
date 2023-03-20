"""Utilities to work with games."""

from lol_stats import data

from . import _smurf_detection


def get_my_team(game: data.Game) -> data.Team:
    """Get my team."""
    if game.blue_team.is_my_team:
        return game.blue_team
    return game.red_team


def get_enemy_team(game: data.Game) -> data.Team:
    """Get the enemy team."""
    if not game.blue_team.is_my_team:
        return game.blue_team
    return game.red_team


def is_smurf_in_team(team: data.Team) -> bool:
    """Check if a smurf is in the enemy team."""
    return any(_smurf_detection.is_smurf(summoner) for summoner in team.summoners)


def is_smurf_in_game(game: data.Game) -> bool:
    """Check if a smurf is in the game."""
    return is_smurf_in_team(game.blue_team) or is_smurf_in_team(game.red_team)
