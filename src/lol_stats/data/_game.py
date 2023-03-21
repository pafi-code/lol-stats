"""Data definition of a game."""
import json
import pathlib

import pydantic
from typing_extensions import Self

from lol_stats import logging

from . import _summoner, _team

_LOGGER = logging.create_colored_logger(__name__)


class GameMetadata(pydantic.BaseModel):
    """Metadata of a game."""

    match_id: str
    game_duration: int
    game_creation: int
    game_version: str
    map_id: int


class Game(pydantic.BaseModel):
    """Definition of a game."""

    metadata: GameMetadata
    blue_team: _team.Team
    red_team: _team.Team


class Games(pydantic.BaseModel):
    """Collection of games."""

    games: list[Game]

    @property
    def all_summoners(self) -> list[_summoner.SummonerInGame]:
        summoners = []
        for game in self.games:
            summoners.extend(game.blue_team.summoners)
            summoners.extend(game.red_team.summoners)
        return summoners

    def save(self, path: pathlib.Path) -> None:
        """
        Save the downloaded games as json.

        Parameters
        ----------
        path
            The path where to save the data.
        """
        with path.open("w", encoding="utf-8") as stream:
            json.dump(self.dict(), stream, indent=2, ensure_ascii=False)
        _LOGGER.info(f"Saved data at {path}.")

    @classmethod
    def load(cls, path: pathlib.Path) -> Self:
        """
        Load the data from json.

        Parameters
        ----------
        path
            The path where the file is saved.


        Returns
        -------
        Games
            The games as data object.
        """
        with path.open("r", encoding="utf-8") as stream:
            return cls.parse_obj(json.load(stream))
