import pytest
import lazebot.game_data as gd

gd.__cache = True
gd.__useApi = False


def test_fetch():
    guild = gd.fetch_guild("W6ig-DV0RoKkfTQOa1hTGw")
    print(guild)
    print(gd.fetch_players(guild))
    print(gd.fetch_op_reqs())
    assert True


@pytest.mark.parametrize('name,relic_tiers,max_relic_tier,total_units', [
    ("01", [], 9, 0),
    ("02", [9], 8, 0),
    ("03", [5, 6, 7, 8, 9], 9, 1),
    ("04", [5, 6, 7, 8, 9], 8, 1),
    ("05", [5, 6, 7, 8, 9], 7, 1),
    ("06", [5, 6, 7, 8, 9], 6, 1),
    ("07", [5, 6, 7, 8, 9], 5, 1),
    ("08", [5, 6, 7, 8, 9, 5, 6, 7, 8, 9], 7, 2),
    ("09", [5, 5, 5, 6, 6, 7, 8, 9], 7, 3),
    ("10", [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 9, 9, 7, 7, 7, 7, 7, 7, 8, 8, 8, 8, 6, 6, 6, 6, 6, 6, 6, 6], 9, 10)
])
def test_op_req_total_units(name, relic_tiers, max_relic_tier, total_units):
    assert gd.OpReq(name, relic_tiers).total_units(max_relic_tier) == total_units


@pytest.mark.parametrize('name,relic_tiers,relic_tier,max_matching', [
    ("01", [], 9, -1),
    ("02", [], 5, -1),
    ("03", [5, 6, 7, 8, 9], 9, 9),
    ("04", [5, 6, 7, 8, 9], 8, 8),
    ("05", [5, 6, 7, 8, 9], 7, 7),
    ("06", [5, 6, 7, 8, 9], 6, 6),
    ("07", [5, 6, 7, 8, 9], 5, 5),
    ("08", [5, 5, 5, 9, 9], 7, 5)
])
def test_op_req_max_matching(name, relic_tiers, relic_tier, max_matching):
    assert gd.OpReq(name, relic_tiers).max_matching(relic_tier) == max_matching
