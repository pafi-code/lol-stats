"""Module to get the summoner."""

import riotwatcher

from lol_stats import data

from . import _query, _regions

_PUUID_KEY = "puuid"
_NAME_KEY = "name"
_LEVEL_KEY = "summonerLevel"


def get_summoner_by_name(
    name: str,
    region: _regions.Region,
    watcher: riotwatcher.LolWatcher,
) -> data.Summoner:
    """
    Get a summoner by his name and region.

    Parameters
    ----------
    name
        The name of the summoner.
    region
        The region of the summoner.
    watcher
        The watcher that used to query riot api.


    Returns
    -------
    data.Summoner
        The information about the summoner.
    """
    summoner_dict = _query.query(watcher.summoner.by_name, args=[region.value, name])
    return data.Summoner(
        puuid=summoner_dict[_PUUID_KEY],
        name=summoner_dict[_NAME_KEY],
        level=summoner_dict[_LEVEL_KEY],
    )
