import pytest
from lazebot import guild_op_score
from lazebot.guild_op_score import Unit


@pytest.mark.parametrize('name,player_unit,guild_units,op_reqs,value', [
    ("doesn't meet req ship", Unit("A", 1, -1, 6, True), [], [5], 0.),
    ("not required ship", Unit("A", 1, -1, 7, True), [], [], 0.),
    ("ship meets, only in guild", Unit("A", 1, -1, 7, True), [], [5], 12787.5),
    ("ship meets, not enough in guild", Unit("A", 1, -1, 7, True), 4 * [Unit("A", 1, -1, 7, True)], 8 * [6], 12787.5),
    ("ship meets, no extra in guild", Unit("A", 1, -1, 7, True), 4 * [Unit("A", 1, -1, 7, True)], 5 * [6], 12787.5),
    ("ship meets, some extra in guild",
     Unit("A", 1, -1, 7, True), [Unit("A", 1, -1, rarity, True) for rarity in [3, 4, 5, 6, 7, 7]], [2], 2900.0),
    ("ship meets, lots of extra in guild", Unit("A", 1, -1, 7, True), 10 * [Unit("A", 1, -1, 7, True)], 5 * [6], 0.),
    ("doesn't meet req ground", Unit("A", 13, 4, 7, False), [], [5], 0.),
    ("not required ground", Unit("A", 13, 9, 7, False), [], [], 0.),
    ("ground meets, only in guild, r5", Unit("A", 13, 5, 7, False), [], [5], 42950.7),
    ("ground meets, only in guild, r5 overkill", Unit("A", 13, 9, 7, False), [], [5], 42950.7),
    ("ground meets, only in guild, r6", Unit("A", 13, 6, 7, False), [], [6], 48279.6),
    ("ground meets, only in guild, r7", Unit("A", 13, 7, 7, False), [], [7], 55490.4),
    ("ground meets, only in guild, r8", Unit("A", 13, 8, 7, False), [], [8], 74911.7),
    ("ground meets, only in guild, r9", Unit("A", 13, 9, 7, False), [], [9], 104739.4),
    ("ground meets, only in guild, two units", Unit("A", 13, 9, 7, False), [], [9, 9], 104739.4),
])
def test_compute_ship_score(name, player_unit, guild_units, op_reqs, value):
    result = guild_op_score.__compute_unit_score(player_unit, guild_units, op_reqs)
    assert result.unit == player_unit
    assert result.guildUnits == guild_units
    assert result.op_reqs == op_reqs
    assert result.score == pytest.approx(value, 0.1)
