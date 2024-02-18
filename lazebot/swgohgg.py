import requests
from lazebot.api_cache_file import ApiCacheFile
from lazebot.exceptions import *

API_CACHE = ApiCacheFile()  # default to file cache for local testing


def fetch_player(ally_code: str):
    player = API_CACHE.fetch_player(ally_code)
    if player is None:
        url = f"https://api.swgoh.gg/player/{ally_code}"
        print(f"Calling API: {url}")
        result = requests.get(url)
        if result.status_code == 404 or not result.json()["data"]:
            raise PlayerNotFoundException
        player = result.json()
        API_CACHE.add_player(ally_code, player)
    return player


def fetch_guild(guild_id: str):
    guild = API_CACHE.fetch_guild(guild_id)
    if guild is None:
        url = f"https://api.swgoh.gg/guild-profile/{guild_id}"
        print(f"Calling API: {url}")
        result = requests.get(url)
        if result.status_code == 404 or not result.json()["data"]:
            raise GuildNotFoundException
        guild = result.json()
        API_CACHE.add_guild(guild_id, guild)
    return guild
