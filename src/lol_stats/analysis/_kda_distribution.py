"""Calculate the kda distribution per level."""

import math
from collections import defaultdict
from statistics import StatisticsError, mean, stdev

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

from lol_stats import data

_LEVEL_KEY = "levels"
_MEAN_KEY = "means"
_STD_KEY = "stds"


def plot_kda_distribution(summoners: list[data.SummonerInGame]) -> plt.Axes:
    """
    Plot the kda over bins via mean and standard deviation.

    Parameters
    ----------
    summoners
        The list of summoners that should be evaluated.


    Returns
    -------
    plt.Axes
        The axes containing the plot.
    """
    sns.set()
    stats = _get_kda_distribution(summoners)
    levels = stats[_LEVEL_KEY]
    means = np.array(stats[_MEAN_KEY])
    stds = np.array(stats[_STD_KEY])
    fig, axes = plt.subplots()
    axes.plot(levels, means, color="b")
    axes.fill_between(levels, means - stds, means + stds, color="b", alpha=0.2)
    axes.set_xlabel("Level")
    axes.set_ylabel("Average KDA")
    fig.autofmt_xdate()
    return axes


def _get_kda_distribution(summoners: list[data.SummonerInGame]) -> dict:
    """Get a kda distribution given player levels."""
    bins: dict[tuple[int, int], list[float]] = defaultdict(list)
    for summoner in summoners:
        bins[_get_bin(summoner.level)].append(get_kda(summoner.game_stats))

    mean_dict = dict(
        sorted(
            {key: mean(value) for key, value in bins.items()}.items(),
            key=lambda item: item[0][0],
        ),
    )
    std_dict = dict(
        sorted(
            {key: _get_std(value) for key, value in bins.items()}.items(),
            key=lambda item: item[0][0],
        ),
    )
    return {
        _LEVEL_KEY: [str(key) for key in mean_dict],
        _MEAN_KEY: list(mean_dict.values()),
        _STD_KEY: list(std_dict.values()),
    }


def get_kda(stats: data.GameStats) -> float:
    """Calculate the kda of a summoner in a game."""
    if stats.deaths > 0:
        return (stats.kills + stats.assists) / stats.deaths
    return stats.kills + stats.assists


def _get_bin(level: int) -> tuple[int, int]:
    """Sort levels into a bins of size 30."""
    step_size = 30
    max_multiple = 12
    lower_bound = math.floor(level / step_size)
    upper_bound = math.ceil(level / step_size)
    if upper_bound == lower_bound:
        upper_bound += 1
    if lower_bound >= max_multiple:
        return (12 * 30, 100000)
    return step_size * lower_bound, step_size * upper_bound


def _get_std(scores: list[float]) -> float:
    """Calculate the standard deviation of a list."""
    try:
        return stdev(scores)
    except StatisticsError:
        return 0
