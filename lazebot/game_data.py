import requests
import json

__cache = True
__useApi = False


def fetch_guild(guild_id):
    if __useApi:
        url = f"http://api.swgoh.gg/guild-profile/{guild_id}"
        print(f"Calling API: {url}")
        guild = requests.get(url).json()
        if __cache:
            with open(f"../lazebot/data/cached/{guild_id}.json", "w") as f:
                f.write(json.dumps(guild))
    else:
        with open(f"../lazebot/data/cached/{guild_id}.json") as f:
            guild = json.load(f)
    return guild


def get_ally_codes(guild):
    ally_codes = []
    for member in guild["data"]["members"]:
        if member["ally_code"] is not None:
            ally_codes.append(member["ally_code"])
    return ally_codes


def fetch_players(guild):
    ally_codes = get_ally_codes(guild)
    players = []
    for allyCode in ally_codes:
        if __useApi:
            url = f"http://api.swgoh.gg/player/{allyCode}"
            print(f"Calling API: {url}")
            player = requests.get(url).json()
            if __cache:
                with open(f"../lazebot/data/cached/{allyCode}.json", "w") as f:
                    f.write(json.dumps(player))
        else:
            with open(f"../lazebot/data/cached/{allyCode}.json") as f:
                player = json.load(f)
        units = []
        for u in player["units"]:
            data = u["data"]
            unit = Unit(data["base_id"], data["gear_level"], data["relic_tier"], data["rarity"], data["combat_type"])
            units.append(unit)
        players.append(Player(allyCode, player["data"]["name"], units))
    return players


class Player:
    def __init__(self, ally_code, name, units):
        self.allyCode = ally_code
        self.name = name
        self.units = units

    def __str__(self):
        return f"Player(\"{self.allyCode}\", \"{self.name}\", \"{self.units}\")"

    def __repr__(self):
        return f"Player(\"{self.allyCode}\", \"{self.name}\", \"{self.units}\")"


class Unit:
    def __init__(self, base_id, gear_level, relic_tier, rarity, combat_type):
        self.baseId = base_id
        self.gearLevel = int(gear_level)
        self.relicTier = int(relic_tier) - 2
        self.rarity = int(rarity)
        self.isShip = combat_type == "2"

    def __str__(self):
        return f"Unit(\"{self.baseId}\", {self.gearLevel}, {self.relicTier}, {self.rarity}, {self.isShip})"

    def __repr__(self):
        return f"Unit(\"{self.baseId}\", {self.gearLevel}, {self.relicTier}, {self.rarity}, {self.isShip})"
