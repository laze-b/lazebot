import pytest
from lazebot import guild_op_score
from lazebot.guild_op_score import Unit
from lazebot.guild_op_score import UnitScoreComponent as Usc


def ship(base_id, rarity, ally_code):
    return Unit(base_id, base_id, 1, -1, rarity, True, ally_code)


def ships(base_id, *args):
    return [ship(base_id, rarity, ally_code) for rarity, ally_code in args]


def ground(base_id, relic, rarity, ally_code):
    gear = 1
    if relic >= 0:
        gear = 13
    return Unit(base_id, base_id, gear, relic, rarity, False, ally_code)


def grounds(base_id, *args):
    return [ground(base_id, relic, rarity, ally_code) for relic, rarity, ally_code in args]


@pytest.mark.parametrize(
    'scenario, phase, op_req_count, player_unit, guild_units, expected_components, expected_score', [
        ("doesn't meet req ship", 1, 1,
         ship("A", 6, "123"),
         ships("A", (6, "123")),
         [],
         0.),
        ("not required ship", 1, 0,
         ship("A", 7, "123"),
         ships("A", (7, "123")),
         [],
         0.),
        ("ship meets, only in guild", 1, 1,
         ship("A", 7, "123"),
         ships("A", (7, "123")),
         [Usc(ship("A", 0, None), 6600.), Usc(ship("A", 0, None), 3300.), Usc(ship("A", 0, None), 1650.),
          Usc(ship("A", 0, None), 825.), Usc(ship("A", 0, None), 412.5)],
         12787.5),
        ("ship meets, not enough in guild", 1, 5,
         ship("A", 7, "123"),
         ships("A", (7, "123"), (7, "222"), (7, "333"), (7, "444")),
         [Usc(ship("A", 0, None), 6600.), Usc(ship("A", 0, None), 3300.), Usc(ship("A", 0, None), 1650.),
          Usc(ship("A", 0, None), 825.), Usc(ship("A", 0, None), 412.5)],
         12787.5),
        ("ship meets, no extra in guild", 2, 5,
         ship("A", 7, "123"),
         ships("A", (7, "123"), (7, "222"), (7, "333"), (7, "444"), (7, "555")),
         [Usc(ship("A", 0, None), 6600.), Usc(ship("A", 0, None), 3300.), Usc(ship("A", 0, None), 1650.),
          Usc(ship("A", 0, None), 825.), Usc(ship("A", 0, None), 412.5)],
         12787.5),
        ("ship meets, some extra in guild", 3, 1,
         ship("A", 7, "123"),
         ships("A", (3, "222"), (7, "333"), (5, "444"), (6, "555"), (4, "666"), (7, "123")),
         [Usc(ship("A", 7, "333"), 0.), Usc(ship("A", 6, "555"), 1000.), Usc(ship("A", 5, "444"), 925.),
          Usc(ship("A", 4, "666"), 625.), Usc(ship("A", 3, "222"), 350.)],
         2900.0),
        ("ship meets, lots of extra in guild", 6, 5,
         ship("A", 7, "123"),
         ships("A", (7, None), (7, None), (7, None), (7, None), (7, None), (7, None), (7, None), (7, None),
               (7, None), (7, "123")),
         [Usc(ship("A", 7, None), 0.), Usc(ship("A", 7, None), 0.), Usc(ship("A", 7, None), 0.),
          Usc(ship("A", 7, None), 0.), Usc(ship("A", 7, None), 0.)],
         0.),
    ])
def test_compute_ship_score(scenario, phase, op_req_count,
                            player_unit,
                            guild_units,
                            expected_components,
                            expected_score):
    result = guild_op_score.__compute_unit_score(player_unit, guild_units, op_req_count, phase,
                                                 guild_op_score.__DEFAULT_SCORE_PARAMS)
    assert result.unit == player_unit
    assert result.opReqCount == op_req_count
    assert result.phase == phase
    assert len(result.components) == len(expected_components)
    for r, e in zip(result.components, expected_components):
        assert r.guildUnit == e.guildUnit
        assert r.score == pytest.approx(e.score, abs=0.1)
    assert result.score() == pytest.approx(expected_score, abs=0.1)


@pytest.mark.parametrize(
    'scenario, phase, op_req_count, player_unit, guild_units, expected_components, expected_score', [
        ("doesn't meet req ground", 1, 1,
         ground("A", 4, 7, "123"),
         grounds("A", (4, 7, "123")),
         [],
         0.),
        ("not required ground", 1, 0,
         ground("A", 9, 7, "123"),
         grounds("A", (9, 7, "123")),
         [],
         0.),
        ("ground meets, only in guild, r5", 1, 1,
         ground("A", 5, 7, "123"),
         grounds("A", (5, 7, "123")),
         [Usc(ground("A", -1, 0, None), 22168.1), Usc(ground("A", -1, 0, None), 11084.0),
          Usc(ground("A", -1, 0, None), 5542.0), Usc(ground("A", -1, 0, None), 2771.0),
          Usc(ground("A", -1, 0, None), 1385.5)],
         42950.7),
        ("ground meets, only in guild, r5 overkill", 1, 1,
         ground("A", 9, 7, "123"),
         grounds("A", (9, 7, "123")),
         [Usc(ground("A", -1, 0, None), 22168.1), Usc(ground("A", -1, 0, None), 11084.0),
          Usc(ground("A", -1, 0, None), 5542.0), Usc(ground("A", -1, 0, None), 2771.0),
          Usc(ground("A", -1, 0, None), 1385.5)],
         42950.7),
        ("ground meets, only in guild, r6", 2, 1,
         ground("A", 6, 7, "123"),
         grounds("A", (6, 7, "123")),
         [Usc(ground("A", -1, 0, None), 24918.4), Usc(ground("A", -1, 0, None), 12459.2),
          Usc(ground("A", -1, 0, None), 6229.6), Usc(ground("A", -1, 0, None), 3114.8),
          Usc(ground("A", -1, 0, None), 1557.4)],
         48279.6),
        ("ground meets, only in guild, r7", 3, 1,
         ground("A", 7, 7, "123"),
         grounds("A", (7, 7, "123")),
         [Usc(ground("A", -1, 0, None), 28640.1), Usc(ground("A", -1, 0, None), 14320.1),
          Usc(ground("A", -1, 0, None), 7160.0), Usc(ground("A", -1, 0, None), 3580.0),
          Usc(ground("A", -1, 0, None), 1790.0)],
         55490.4),
        ("ground meets, only in guild, r8", 4, 1,
         ground("A", 8, 7, "123"),
         grounds("A", (8, 7, "123")),
         [Usc(ground("A", -1, 0, None), 38664.1), Usc(ground("A", -1, 0, None), 19332.1),
          Usc(ground("A", -1, 0, None), 9666.0),
          Usc(ground("A", -1, 0, None), 4833.0), Usc(ground("A", -1, 0, None), 2416.5)],
         74911.7),
        ("ground meets, only in guild, r9", 6, 1,
         ground("A", 9, 7, "123"),
         grounds("A", (9, 7, "123")),
         [Usc(ground("A", -1, 0, None), 54059.1), Usc(ground("A", -1, 0, None), 27029.5),
          Usc(ground("A", -1, 0, None), 13514.8), Usc(ground("A", -1, 0, None), 6757.4),
          Usc(ground("A", -1, 0, None), 3378.7)],
         104739.4),
        ("ground meets, not enough in guild", 1, 5,
         ground("A", 5, 7, "123"),
         grounds("A", (5, 7, None), (5, 7, None), (5, 7, "123"), (5, 7, None)),
         [Usc(ground("A", -1, 0, None), 22168.1), Usc(ground("A", -1, 0, None), 11084.0),
          Usc(ground("A", -1, 0, None), 5542.0), Usc(ground("A", -1, 0, None), 2771.0),
          Usc(ground("A", -1, 0, None), 1385.5)],
         42950.7),
        ("ground meets, no extra in guild", 1, 5,
         ground("A", 5, 7, "123"),
         grounds("A", (5, 7, None), (5, 7, "123"), (5, 7, None), (5, 7, None), (5, 7, None)),
         [Usc(ground("A", -1, 0, None), 22168.1), Usc(ground("A", -1, 0, None), 11084.0),
          Usc(ground("A", -1, 0, None), 5542.0), Usc(ground("A", -1, 0, None), 2771.0),
          Usc(ground("A", -1, 0, None), 1385.5)],
         42950.7),
        ("ground meets, some extra in guild", 3, 1,
         ground("A", 7, 7, "123"),
         grounds("A", (3, 3, None), (7, 7, None), (5, 7, None), (6, 7, None), (4, 7, None), (7, 7, "123")),
         [Usc(ground("A", 7, 7, None), 0.), Usc(ground("A", 6, 7, None), 1860.8), Usc(ground("A", 5, 7, None), 1618.0),
          Usc(ground("A", 4, 7, None), 992.1), Usc(ground("A", 3, 3, None), 919.4)],
         5390.4),
        ("ground meets, lots of extra in guild", 6, 5,
         ground("A", 7, 7, "123"),
         grounds("A", (7, 7, None), (7, 7, None), (7, 7, None), (7, 7, "123"), (7, 7, None), (7, 7, None), (7, 7, None),
                 (7, 7, None), (7, 7, None), (7, 7, None)),
         [],
         0.),
    ])
def test_compute_ground_score(scenario, phase, op_req_count,
                              player_unit,
                              guild_units,
                              expected_components,
                              expected_score):
    result = guild_op_score.__compute_unit_score(player_unit, guild_units, op_req_count, phase,
                                                 guild_op_score.__DEFAULT_SCORE_PARAMS)
    assert result.unit == player_unit
    assert result.opReqCount == op_req_count
    assert result.phase == phase
    assert len(result.components) == len(expected_components)
    for r, e in zip(result.components, expected_components):
        assert r.guildUnit == e.guildUnit
        assert r.score == pytest.approx(e.score, abs=0.1)
    assert result.score() == pytest.approx(expected_score, abs=0.1)


@pytest.mark.parametrize('scenario, player_unit, guild_units, unit_op_reqs, expected_score', [
    ("no phase scores",
     ground("A", 4, 7, "123"),
     grounds("A", (4, 7, "123")),
     {},
     None),
    ("pick max",
     ground("A", 5, 7, "123"),
     grounds("A", (5, 7, "123")),
     {1: 1},
     42950.7),
])
def test_compute_max_phase_score(scenario, player_unit, guild_units, unit_op_reqs, expected_score):
    result = guild_op_score.__compute_max_phase_unit_score(player_unit, guild_units, unit_op_reqs,
                                                           guild_op_score.__DEFAULT_SCORE_PARAMS)
    if expected_score is None:
        assert result is None
    else:
        assert result.score() == pytest.approx(expected_score, abs=0.1)
