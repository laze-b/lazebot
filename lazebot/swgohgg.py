import requests
from lazebot.api_cache_file import ApiCacheFile


API_CACHE = ApiCacheFile()  # default to file cache for local testing


def fetch_player(ally_code: str):
    player = API_CACHE.fetch_player(ally_code)
    if player is None:
        url = f"http://api.swgoh.gg/player/{ally_code}"
        print(f"Calling API: {url}")
        player = requests.get(url).json()
        API_CACHE.add_player(ally_code, player)
    return player


def fetch_guild(guild_id: str):
    guild = API_CACHE.fetch_guild(guild_id)
    if guild is None:
        url = f"http://api.swgoh.gg/guild-profile/{guild_id}"
        print(f"Calling API: {url}")
        guild = requests.get(url).json()
        API_CACHE.add_guild(guild_id, guild)
    return guild
