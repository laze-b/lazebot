from lazebot import op_req
from lazebot import game_data
from lazebot import item_value
from dataclasses import dataclass


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

@dataclass(frozen=True)
class __ScoreParams:
    num_units_to_compare: int
    initial_weight: float
    decay: float


__score_params = __ScoreParams(5, 1, .5)


@dataclass(frozen=True)
class Unit:
    baseId: str
    gear: int  # range 0 - 13
    relic: int  # range -1 - 7
    rarity: int  # range 0-7
    ship: bool


@dataclass(frozen=True)
class UnitScore:
    unit: Unit
    guildUnits: list[Unit]
    op_reqs: list[int]
    score: float


def __compute_unit_score(player_unit: Unit, guild_units: list[Unit], op_reqs: list[int]) -> UnitScore:
    if player_unit.ship:
        return __compute_ship_score(player_unit, guild_units, len(op_reqs))
    else:
        return __compute_ground_score(player_unit, guild_units, op_reqs)


def __compute_ship_score(player_unit: Unit, guild_units: list[Unit], op_req_count: int) -> UnitScore:
    """
    Compute the guild op score for a ship unit.

    :param player_unit: The player's unit
    :param guild_units: List of all units in the guild (inclusive of the player)
    :param op_req_count: Number of units required across all ops zones
    :return: the computed score
    """

    score = 0.
    # we only get credit if it's actually required, and we meet the requirement
    if player_unit.rarity == 7 and op_req_count > 0:
        compare_units = sorted(guild_units, key=lambda x: x.rarity, reverse=True)
        # pad the compare_units if there aren't enough in the guild
        while len(compare_units) < (__score_params.num_units_to_compare + op_req_count):
            compare_units.append(Unit("dummy", 0, -1, 0, True))

        weight = __score_params.initial_weight
        for guild_unit in compare_units[op_req_count:__score_params.num_units_to_compare + op_req_count]:
            score += weight * item_value.compute_shard_value(7, guild_unit.rarity)
            weight = weight * __score_params.decay

    return UnitScore(player_unit, guild_units, op_req_count * [7], score)


def __compute_ground_score(player_unit: Unit, guild_units: list[Unit], op_reqs: list[int]) -> UnitScore:
    """
    Compute the guild op score for a ground unit.

    :param player_unit: The player's unit
    :param guild_units: List of all units in the guild (inclusive of the player)
    :param op_reqs: List of all relic tier requirements for the unit, each represents a distinct instance of an
        operation requirement
    :return: the computed score
    """

    score = 0.
    num_required = len(op_reqs)
    # we only get credit if it's actually required, and we meet the requirement
    if num_required > 0 and player_unit.relic >= min(op_reqs):
        compare_units = sorted(guild_units, key=lambda x: x.gear + x.relic, reverse=True)
        # pad the compare_units if there aren't enough in the guild
        while len(compare_units) < (__score_params.num_units_to_compare + num_required):
            compare_units.append(Unit("dummy", 0, -1, 0, True))

        weight = __score_params.initial_weight
        for guild_unit in compare_units[num_required:__score_params.num_units_to_compare + num_required]:
            score += weight * __ground_value_difference(
                player_unit.relic, guild_unit.relic, guild_unit.rarity)
            weight = weight * __score_params.decay

    return UnitScore(player_unit, guild_units, op_reqs, score)


def __ground_value_difference(my_relic: int, compare_to_relic: int, compare_to_rarity):
    value = 0.
    if my_relic > compare_to_relic:
        value += item_value.compute_gear_value(my_relic, compare_to_relic)
        if compare_to_rarity < 7:
            value += item_value.compute_shard_value(7, compare_to_rarity)
    return value
