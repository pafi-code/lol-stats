"""Data definition of a team."""

import pydantic

from . import _summoner


class Team(pydantic.BaseModel):
    """Definition of a team."""

    summoners: list[_summoner.SummonerInGame]

    @property
    def gold(self) -> int:
        return sum(summoner.game_stats.gold_earned for summoner in self.summoners)

    @property
    def kills(self) -> int:
        return sum(summoner.game_stats.kills for summoner in self.summoners)

    @property
    def deaths(self) -> int:
        return sum(summoner.game_stats.deaths for summoner in self.summoners)

    @property
    def win(self) -> bool:
        return all(summoner.won for summoner in self.summoners)

    @property
    def my_team(self) -> bool:
        return any(summoner.is_me for summoner in self.summoners)
