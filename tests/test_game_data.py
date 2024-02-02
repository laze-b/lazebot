import pytest
from lazebot import game_data


def test_fetch():
    (guild_name, players, guild_units) = game_data.fetch_players_and_guild_units(
        "736645715", {"BOBAFETTSCION", "TIEINTERCEPTOR"})
    print(guild_name)
    print(players)
    print(guild_units)
    assert True


