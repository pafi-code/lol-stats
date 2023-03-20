"""Utilities to work with games."""

from lol_stats import data

_MAX_SMURF_LEVEL = 60


def is_smurf(summoner: data.SummonerInGame) -> bool:
    """Check if a summoner is a smurf."""
    if summoner.level <= _MAX_SMURF_LEVEL:
        return True
    return False


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
    return any(is_smurf(summoner) for summoner in team.summoners)


def is_smurf_in_game(game: data.Game) -> bool:
    """Check if a smurf is in the game."""
    return is_smurf_in_team(game.blue_team) or is_smurf_in_team(game.red_team)


def count_smurf_in_team(team: data.Team) -> int:
    """Count the number of smurfs in a team."""
    count = 0
    for summoner in team.summoners:
        if is_smurf(summoner):
            count += 1
    return count


def count_smurf_in_game(game: data.Game) -> int:
    """Count the number of smurfs in the game."""
    return count_smurf_in_team(game.blue_team) + count_smurf_in_team(game.red_team)
