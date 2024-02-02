import requests
from lazebot import api_cache


def fetch_player(ally_code: str):
    player = api_cache.fetch_player(ally_code)
    if player is None:
        url = f"http://api.swgoh.gg/player/{ally_code}"
        print(f"Calling API: {url}")
        player = requests.get(url).json()
        api_cache.add_player(ally_code, player)
    return player


def fetch_guild(guild_id: str):
    guild = api_cache.fetch_guild(guild_id)
    if guild is None:
        url = f"http://api.swgoh.gg/guild-profile/{guild_id}"
        print(f"Calling API: {url}")
        guild = requests.get(url).json()
        api_cache.add_guild(guild_id, guild)
    return guild
