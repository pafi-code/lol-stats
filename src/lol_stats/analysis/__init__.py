"""Subpackage for game analysis."""

from ._kda_distribution import plot_kda_distribution
from ._win_rate import (
    get_general_win_rate,
    get_win_rate_against_smurfs,
    get_win_rate_with_smurfs,
    get_win_rate_without_smurfs_in_game,
)

__all__ = [
    "plot_kda_distribution",
    "get_general_win_rate",
    "get_win_rate_against_smurfs",
    "get_win_rate_with_smurfs",
    "get_win_rate_without_smurfs_in_game",
]
