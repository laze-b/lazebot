import pytest
from lazebot import game_data

game_data.__cache = True
game_data.__useApi = False


def test_fetch():
    guild = game_data.fetch_guild("W6ig-DV0RoKkfTQOa1hTGw")
    print(guild)
    print(game_data.fetch_players(guild))
    assert True


