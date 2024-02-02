import json

__BASE_PATHS = ["../lazebot/data/cached", "lazebot/data/cached"]


def fetch_player(ally_code: str):
    for p in __BASE_PATHS:
        try:
            with open(f"{p}/{ally_code}.json") as f:
                return json.load(f)
        except FileNotFoundError:
            pass
    return None


def add_player(ally_code: str, player):
    for p in __BASE_PATHS:
        try:
            with open(f"{p}/{ally_code}.json", "w") as f:
                f.write(json.dumps(player))
                return
        except FileNotFoundError:
            pass


def fetch_guild(guild_id: str):
    for p in __BASE_PATHS:
        try:
            with open(f"{p}/{guild_id}.json") as f:
                return json.load(f)
        except FileNotFoundError:
            pass
    return None


def add_guild(guild_id: str, guild):
    for p in __BASE_PATHS:
        try:
            with open(f"../lazebot/data/cached/{guild_id}.json", "w") as f:
                f.write(json.dumps(guild))
                return
        except FileNotFoundError:
            pass
