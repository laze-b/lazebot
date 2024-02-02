from dataclasses import dataclass
from lazebot import swgohgg


@dataclass(frozen=True)
class Unit:
    baseId: str
    name: str
    gear: int  # range 0 - 13
    relic: int  # range -1 - 7
    rarity: int  # range 0 - 7
    ship: bool
    allyCode: str = None  # player ID that owns the unit
    owner: str = None  # player name that owns the unit


@dataclass(frozen=True)
class Player:
    allyCode: str
    name: str
    units: list[Unit]


def fetch_players_and_guild_units(
        ally_code: str, base_ids: set[str]) -> (str, dict[str, Player], dict[str, list[Unit]]):
    guild_id = __fetch_guild_id(ally_code)
    guild_name, players = __fetch_players(guild_id, base_ids)
    guild_units = __generate_guild_units(players)

    return guild_name, players, guild_units


def __fetch_guild_id(ally_code):
    player_data = swgohgg.fetch_player(ally_code)
    guild_id = player_data["data"]["guild_id"]
    return guild_id


def __fetch_players(guild_id, base_ids):
    players = {}
    guild_data = swgohgg.fetch_guild(guild_id)
    guild_name = guild_data["data"]["name"]
    for members_data in guild_data["data"]["members"]:
        next_ally_code = str(members_data["ally_code"])
        if next_ally_code is not None:
            next_player_data = swgohgg.fetch_player(next_ally_code)
            players[next_ally_code] = __create_player(next_ally_code, next_player_data, base_ids)
    return guild_name, players


def __generate_guild_units(players):
    guild_units = {}
    for player in players.values():
        for unit in player.units:
            guild_units.setdefault(unit.baseId, [])
            guild_units[unit.baseId] += [unit]
    return guild_units


def __create_player(ally_code: str, player_data: dict, base_ids: set[str]):
    player_name = player_data["data"]["name"]
    units = []
    for u in player_data["units"]:
        data = u["data"]
        if data["base_id"] in base_ids:
            unit = Unit(data["base_id"], data["name"], data["gear_level"], data["relic_tier"] - 2, data["rarity"],
                        data["combat_type"] == 2, ally_code, player_name)
            units.append(unit)
    return Player(str(ally_code), player_name, units)
