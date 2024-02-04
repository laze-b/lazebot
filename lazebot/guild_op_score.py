from lazebot import op_req
from lazebot import game_data
from lazebot.game_data import Unit
from lazebot.game_data import Player
from lazebot import item_value
from dataclasses import dataclass

"""
INPUTS:
ally_code
compute_guild - True to compute for the guild, False for just the player

SCORING:
- scoring is based on unit replacement cost, based on ops needs and the guild's overall units
- since phases run one at a time, only count the phase where the player's unit satisfies the requirement
and has the highest replacement cost
- for simplicity, assume the goal is to eventually max all phases and don't account for specific guild plans or preloads

OUTLINE:
Collect all operations requirement baseIds
for each unique req baseId
    Collect all matching guild units
for each player (either one, or all in guild based on inputs)
    for each unique req baseId
        get the player unit
        get all guild units
        for each phase satisfied by the player unit
            compute the replacement cost of the player unit by each guild unit
            sort the guild units in ascending order by replacement cost
            get the count of op reqs in that phase 
            use the first x units to satisfy the number of operations requirements needed
            compute a phase score by summing the replacement cost of reserve units
        use the max phase score and add to player score
    output total score for player
output guild report
"""


@dataclass(frozen=True)
class UnitScoreComponent:
    guildUnit: Unit
    score: float


@dataclass(frozen=True)
class UnitScore:
    unit: Unit
    opReqCount: int
    phase: int
    components: list[UnitScoreComponent]

    def score(self) -> float:
        return sum(c.score for c in self.components)


@dataclass(frozen=True)
class PlayerScore:
    player: Player
    unitScores: list[UnitScore]

    def score(self):
        return sum(u.score() for u in self.unitScores)


@dataclass(frozen=True)
class ScoreParams:
    num_units_to_compare: int
    initial_weight: float
    decay: float


# these were chosen so the sum of all the weights is close to 1
__DEFAULT_SCORE_PARAMS = ScoreParams(5, .52, .5)


def compute_player_score(ally_code: str, max_phase: int, score_params=__DEFAULT_SCORE_PARAMS) -> PlayerScore:
    base_ids = op_req.fetch_unique_base_ids()
    all_op_reqs = {}
    for base_id in base_ids:
        all_op_reqs[base_id] = {}
        for phase in range(1, max_phase + 1):
            all_op_reqs[base_id][phase] = op_req.fetch_req_count(base_id, phase)

    (guild_name, players, all_guild_units) = game_data.fetch_players_and_guild_units(ally_code, base_ids)

    player = players[ally_code]
    return __compute_player_score(player, all_guild_units, all_op_reqs, score_params)


def compute_guild_score(ally_code: str, max_phase: int,
                        score_params=__DEFAULT_SCORE_PARAMS) -> (str, list[PlayerScore]):
    base_ids = op_req.fetch_unique_base_ids()
    all_op_reqs = {}
    for base_id in base_ids:
        all_op_reqs[base_id] = {}
        for phase in range(1, max_phase + 1):
            all_op_reqs[base_id][phase] = op_req.fetch_req_count(base_id, phase)

    (guild_name, players, all_guild_units) = game_data.fetch_players_and_guild_units(ally_code, base_ids)

    player_scores = []
    for player in players.values():
        player_scores.append(__compute_player_score(player, all_guild_units, all_op_reqs, score_params))
    return guild_name, player_scores


def __compute_player_score(player: Player, all_guild_units: dict[str, list[Unit]],
                           all_op_reqs: dict[str, dict[int, int]], score_params: ScoreParams) -> PlayerScore:
    unit_scores = []
    for unit in player.units:
        guild_units = all_guild_units[unit.baseId]
        unit_op_reqs = all_op_reqs[unit.baseId]
        max_phase_score = __compute_max_phase_unit_score(unit, guild_units, unit_op_reqs, score_params)
        if max_phase_score:
            unit_scores.append(max_phase_score)
    return PlayerScore(player, unit_scores)


def __compute_max_phase_unit_score(player_unit: Unit, guild_units: list[Unit],
                                   unit_op_reqs: dict[int, int], score_params: ScoreParams) -> UnitScore | None:
    max_phase_score = None
    for phase, op_req_count in unit_op_reqs.items():
        phase_score = __compute_unit_score(player_unit, guild_units, op_req_count, phase, score_params)
        if phase_score.score() > 0.0 and (not max_phase_score or phase_score.score() > max_phase_score.score()):
            max_phase_score = phase_score
    return max_phase_score


def __compute_unit_score(player_unit: Unit, guild_units: list[Unit], op_req_count: int, phase: int,
                         score_params: ScoreParams) -> UnitScore:
    if player_unit.ship:
        return __compute_ship_score(player_unit, guild_units, op_req_count, phase, score_params)
    else:
        return __compute_ground_score(player_unit, guild_units, op_req_count, phase, score_params)


def __compute_ship_score(player_unit: Unit, guild_units: list[Unit], op_req_count: int, phase: int,
                         score_params: ScoreParams) -> UnitScore:
    """
    Compute the guild op score for a ship unit.

    :param player_unit: The player's unit
    :param guild_units: List of all other units in the guild (should include player_unit)
    :param op_req_count: Ops requirement count for the unit
    :param phase: The ops phase we are evaluating
    :return: the computed score
    """

    components = []
    # we only get credit if it's actually required, and we meet the requirement
    if op_req_count > 0 and player_unit.rarity == 7:
        compare_units = guild_units.copy()
        # pad the compare_units if there aren't enough in the guild
        while len(compare_units) < (score_params.num_units_to_compare + op_req_count):
            compare_units.append(Unit(player_unit.baseId, player_unit.name, 1, -1, 0, True))

        # sort and prune so we only score what's needed
        compare_units.sort(reverse=True, key=lambda u: 100 if u.allyCode == player_unit.allyCode else u.rarity)
        compare_units = compare_units[op_req_count:score_params.num_units_to_compare + op_req_count]

        # get the replacement costs
        replacement_costs = []
        for guild_unit in compare_units:
            replacement_cost = item_value.compute_shard_value(player_unit.rarity, guild_unit.rarity)
            replacement_costs.append(replacement_cost)
        guild_replacement_costs = list(zip(compare_units, replacement_costs))

        # calculate score based on the parameters
        components = __compute_weighted_score(guild_replacement_costs, score_params)

    return UnitScore(player_unit, op_req_count, phase, components)


def __compute_ground_score(player_unit: Unit, guild_units: list[Unit], op_req_count: int, phase: int,
                           score_params: ScoreParams) -> UnitScore:
    """
    Compute the guild op score for a ground unit.

    :param player_unit: The player's unit
    :param guild_units: List of all other units in the guild (should include player_unit)
    :param op_req_count: Ops requirement count for the unit
    :param phase: The ops phase we are evaluating
    :return: the computed score
    """

    components = []
    # we only get credit if it's actually required, and we meet the requirement
    relic_tier = min(phase + 4, 9)
    if op_req_count > 0 and player_unit.relic >= relic_tier:
        compare_units = guild_units.copy()
        # pad the compare_units if there aren't enough in the guild
        while len(compare_units) < (score_params.num_units_to_compare + op_req_count):
            compare_units.append(Unit(player_unit.baseId, player_unit.name, 1, -1, 0, False))

        # sort and prune so we only score what's needed
        def sorter(u: Unit):
            if u.allyCode == player_unit.allyCode:
                return 1000  # always first
            elif u.gear == 13:
                return u.relic + 100  # 2nd group
            else:
                return u.rarity * 10 + u.gear  # 3rd group with rarity being more important

        compare_units.sort(reverse=True, key=sorter)
        compare_units = compare_units[op_req_count:score_params.num_units_to_compare + op_req_count]

        # get the replacement costs and sort them
        replacement_costs = []
        for guild_unit in compare_units:
            replacement_cost = __ground_value_difference(relic_tier, guild_unit.relic, guild_unit.rarity)
            replacement_costs.append(replacement_cost)
        guild_replacement_costs = list(zip(compare_units, replacement_costs))

        # calculate score based on the parameters
        components = __compute_weighted_score(guild_replacement_costs, score_params)

    return UnitScore(player_unit, op_req_count, phase, components)


def __compute_weighted_score(guild_replacement_costs: list[(Unit, float)],
                             score_params: ScoreParams) -> list[UnitScoreComponent]:
    components = []
    weight = score_params.initial_weight
    for (guild_unit, replacement_cost) in guild_replacement_costs:
        score = weight * replacement_cost
        components.append(UnitScoreComponent(guild_unit, score))
        weight = weight * score_params.decay
    return components


def __ground_value_difference(my_relic: int, compare_to_relic: int, compare_to_rarity):
    value = 0.
    if my_relic > compare_to_relic:
        value += item_value.compute_gear_value(my_relic, compare_to_relic)
        if compare_to_rarity < 7:
            value += item_value.compute_shard_value(7, compare_to_rarity)
    return value
