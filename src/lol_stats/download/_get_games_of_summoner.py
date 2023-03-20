"""Module to get games of a summoner."""

import riotwatcher
import tqdm

from lol_stats import data, logging

from . import _query, _regions

_AMOUNT_ARG = "count"
_QUEUE_TYPE_ARG = "type"
_TEN_MINUTES = 600

_LOGGER = logging.create_colored_logger(__name__)


def get_games_by_summoner_puuid(
    puuid: str,
    region: _regions.Region,
    amount: int,
    watcher: riotwatcher.RiotWatcher,
) -> data.Games:
    game_ids = _query.query(
        watcher.match.matchlist_by_puuid,
        args=[region.value, puuid],
        kwargs={
            _AMOUNT_ARG: amount,
            _QUEUE_TYPE_ARG: "RANKED_SOLO_5x5",
        },
    )
    games = []
    for game_id in tqdm.tqdm(game_ids):
        game_as_json = _query.query(
            watcher.match.by_id,
            args=[region.value, game_id],
        )
        game = _convert_game_to_data(game_as_json, puuid)
        if game.metadata.game_duration <= _TEN_MINUTES:
            _LOGGER.info(
                msg=f"Ignoring game id {game.metadata.match_id}. Game was aborted.",
            )
        else:
        games.append(_convert_game_to_data(game_as_json, puuid))
    return data.Games(games=games)


_METADATA_KEY = "metadata"
_MATCH_ID_KEY = "matchId"
_INFO_KEY = "info"
_GAME_DURATION_KEY = "gameDuration"
_GAME_CREATION_KEY = "gameCreation"
_GAME_VERSION_KEY = "gameVersion"
_MAP_ID_KEY = "mapId"
_PARTICIPANTS_KEY = "participants"


def _convert_game_to_data(game_as_json: dict, my_puuid: str) -> data.Game:
    metadata_as_json = game_as_json[_METADATA_KEY]
    game_info_as_json = game_as_json[_INFO_KEY]
    metadata = data.GameMetadata(
        match_id=metadata_as_json[_MATCH_ID_KEY],
        game_duration=game_info_as_json[_GAME_DURATION_KEY],
        game_creation=game_info_as_json[_GAME_CREATION_KEY],
        game_version=game_info_as_json[_GAME_VERSION_KEY],
        map_id=game_info_as_json[_MAP_ID_KEY],
    )
    blue_team, red_team = _convert_participants_to_teams(
        game_info_as_json[_PARTICIPANTS_KEY],
        my_puuid,
    )

    return data.Game(metadata=metadata, red_team=red_team, blue_team=blue_team)


def _convert_participants_to_teams(
    participants_as_json: dict,
    my_puuid: str,
) -> tuple[data.Team, data.Team]:
    blue_team = []
    red_team = []
    for participant in participants_as_json:
        summoner = _convert_participants_to_summoner_in_game(participant, my_puuid)
        if summoner.team == data.TeamType.BLUE.value:
            blue_team.append(summoner)
        else:
            red_team.append(summoner)
    return data.Team(summoners=blue_team), data.Team(summoners=red_team)


_ASSIST_KEY = "assists"
_KILLS_KEY = "kills"
_DEATH_KEY = "deaths"
_CHAMPION_ID_KEY = "championId"
_CHAMPION_EXP_KEY = "champExperience"
_GOLD_EARNED_KEY = "goldEarned"
_MINIONS_KEY = "totalMinionsKilled"
_ROLE_KEY = "teamPosition"
_PUUID_KEY = "puuid"
_NAME_KEY = "summonerName"
_LEVEL_KEY = "summonerLevel"
_WIN_KEY = "win"
_TEAM_ID_KEY = "teamId"


def _convert_participants_to_summoner_in_game(
    participant_as_json: dict,
    my_puuid: str,
) -> data.SummonerInGame:
    champion_info = data.ChampionInfo(
        champion_id=participant_as_json[_CHAMPION_ID_KEY],
        champion_experience=participant_as_json[_CHAMPION_EXP_KEY],
    )
    game_stats = data.GameStats(
        kills=participant_as_json[_KILLS_KEY],
        deaths=participant_as_json[_DEATH_KEY],
        assists=participant_as_json[_ASSIST_KEY],
        gold_earned=participant_as_json[_GOLD_EARNED_KEY],
        minions=participant_as_json[_MINIONS_KEY],
        role=data.Role(participant_as_json[_ROLE_KEY]),
    )
    return data.SummonerInGame(
        puuid=participant_as_json[_PUUID_KEY],
        name=participant_as_json[_NAME_KEY],
        level=participant_as_json[_LEVEL_KEY],
        is_me=participant_as_json[_PUUID_KEY] == my_puuid,
        won=participant_as_json[_WIN_KEY],
        team=data.TeamType(participant_as_json[_TEAM_ID_KEY]),
        champion_info=champion_info,
        game_stats=game_stats,
    )
