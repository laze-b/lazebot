import pytest
from lazebot import item_value


@pytest.mark.parametrize('name,my_relic_tier,baseline_relic_tier,value', [
    ("same1", 9, 9, 0),
    ("same2", 5, 5, 0),
    ("same3", -1, -1, 0),
    ("r0", 0, -1, 11079),
    ("r1", 1, 0, 125),
    ("r2", 2, 1, 718),
    ("r3", 3, 2, 1006),
    ("r4", 4, 3, 1174),
    ("r5", 5, 4, 1465),
    ("r6", 6, 5, 2750),
    ("r7", 7, 6, 3722),
    ("r8", 8, 7, 10024),
    ("r9", 9, 8, 15395),
    ("all", 9, -1, 47459),
    ("some", 6, 3, 5388)
])
def test_compute_gear_value(name, my_relic_tier, baseline_relic_tier, value):
    assert item_value.compute_gear_value(my_relic_tier, baseline_relic_tier) == pytest.approx(value, 0.1)


@pytest.mark.parametrize('name,my_rarity,baseline_rarity,value', [
    ("same1", 7, 7, 0),
    ("same2", 5, 5, 0),
    ("same3", 0, 0, 0),
    ("1 star", 1, 0, 200),
    ("2 star", 2, 1, 300),
    ("3 star", 3, 2, 500),
    ("4 star", 4, 3, 600),
    ("5 star", 5, 4, 1300),
    ("6 star", 6, 5, 1700),
    ("7 star", 7, 6, 2000),
    ("all", 7, 0, 6600),
    ("some", 6, 3, 3600)
])
def test_compute_gear_value(name, my_rarity, baseline_rarity, value):
    assert item_value.compute_shard_value(my_rarity, baseline_rarity) == pytest.approx(value, 0.1)
