import requests
import json
import csv

__useApi = False
__cache = True


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


def fetch_op_reqs():
    with open("../lazebot/data/ops.txt") as f:
        op_reqs = {}
        reader = csv.DictReader(f, delimiter="\t")
        for op in reader:
            base_id = op["baseId"]
            name = op["character_name"]
            phase = op["phase"]
            relic_tier = min(9, int(phase) + 4)
            op_req = op_reqs.setdefault(base_id, OpReq(name))
            op_req.add_req(relic_tier)
        return op_reqs


class OpReq:
    def __init__(self, name, relic_tiers=None):
        if relic_tiers is None:
            relic_tiers = []
        self.name = name
        self.relic_tiers = relic_tiers

    def add_req(self, relic_tier):
        self.relic_tiers.append(relic_tier)

    def total_units(self, max_relic_tier):
        total_count = 0
        matching = [rt for rt in self.relic_tiers if rt <= max_relic_tier]
        for current_relic_tier in range(max_relic_tier, 4, -1):
            # add the current tier to the count
            current_count = matching.count(current_relic_tier)
            total_count += current_count
            # remove lower tiers to prevent duplicate counting
            for lower_tier in range(current_relic_tier - 1, 4, -1):
                for x in range(current_count):
                    if lower_tier in matching:
                        matching.remove(lower_tier)
            matching = [rt for rt in matching if rt < current_relic_tier]

        return total_count

    def max_matching(self, relic_tier):
        matching = [rt for rt in self.relic_tiers if rt <= relic_tier]
        if matching:
            return max(matching)
        else:
            return -1

    def __str__(self):
        return f'OpReq("{self.name}", {self.relic_tiers}'

    def __repr__(self):
        return f'OpReq("{self.name}", {self.relic_tiers}'


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
