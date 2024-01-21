from lazebot import op_req
from lazebot import game_data


def compute_guild_score(guild_id):
    players_data = game_data.fetch_players(guild_id)
    op_req_relic_tiers = op_req.fetch_op_req_relic_tiers(op_req.fetch_op_reqs())
    guild_ops = {}

    for baseId, req_relic_tiers in op_req_relic_tiers:
        guild_ops[baseId] = GuildOp(req_relic_tiers)

    for player in players_data:
        for unit in player.units:
            if unit.baseId in guild_ops:
                guild_ops[unit.baseId].add_guild_unit(unit)

    player_scores = {}
    for player in players_data:
        player_score = PlayerScore()
        player_scores[player.allyCode] = player_score
        for unit in player.units:
            if unit.baseId in guild_ops:
                player_score.add_unit_score(guild_ops[unit.baseId], unit)


class PlayerScore:
    def __init__(self):
        self.unit_scores = []

    def add_unit_score(self, guild_op, unit):
        count_needed = guild_op.opReq.total_units()
        self.unit_scores.append(UnitScore(guild_op.opReq, unit, guild_op.guildUnits[count_needed:]))


class UnitScore:
    def __init__(self, op_req, unit, replacements):
        self.playerUnit = unit
        self.replacements = replacements[:5]
        self.score = 0
        decay = 0.2
        weight = 1.0
        for replacement in replacements:
            self.score += weight * self.compute_score(op_req, unit, replacement)
            weight = weight - decay

    def compute_score(self, unit, op_req, replacement):
        if unit.isShip:
            return self.compute_ship_score(unit, replacement)
        else:
            return self.compute_ground_score(op_req, unit, replacement)

    def compute_ship_score(self, unit, replacement):
        return unit.rarity - replacement.rarity

    def compute_ground_score(self, op_req, unit, replacement):
        score = 0
        return score


class GuildOp:
    def __init__(self, req_relic_tiers):
        self.guildUnits = []
        self.reqRelicTiers = req_relic_tiers

    def add_guild_unit(self, unit):
        self.guildUnits.append(unit)
        self.guildUnits.sort(reverse=True, key=GuildOp.sort_unit)

    @staticmethod
    def sort_unit(unit):
        if unit.gearLevel == 13:
            return unit.gearLevel + unit.relicTier
        else:
            return unit.gearLevel

# reqs: 7 7 5 5
# replacement: 3
# unit: 7, 6, 5
# score: 4, 2, 2
