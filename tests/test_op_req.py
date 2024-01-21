import pytest
from lazebot import op_req


def test_fetch_op_reqs():
    result = op_req.fetch_op_reqs()
    assert result.shape == (1710, 9)


def test_fetch_op_req_relic_tiers():
    result = op_req.fetch_op_req_relic_tiers(op_req.fetch_op_reqs())
    assert len(result) == 274
    sample = result["BOBAFETTSCION"]
    assert sorted(sample) == sorted([
        5, 5, 5, 5, 5, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 8, 8, 8, 8, 8, 8,
        9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9])


@pytest.mark.parametrize('name,relic_tier_reqs,unit_relic_tier,satisfied_count', [
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
def test_reqs_satisfied(name, relic_tier_reqs, unit_relic_tier, satisfied_count):
    assert op_req.reqs_satisfied(relic_tier_reqs, unit_relic_tier) == satisfied_count


@pytest.mark.parametrize('name,relic_tier_reqs,unit_relic_tier,max_req_satisfied', [
    ("01", [], 9, -1),
    ("02", [], 5, -1),
    ("03", [5, 6, 7, 8, 9], 9, 9),
    ("04", [5, 6, 7, 8, 9], 8, 8),
    ("05", [5, 6, 7, 8, 9], 7, 7),
    ("06", [5, 6, 7, 8, 9], 6, 6),
    ("07", [5, 6, 7, 8, 9], 5, 5),
    ("08", [5, 5, 5, 9, 9], 7, 5)
])
def test_max_req_satisfied(name, relic_tier_reqs, unit_relic_tier, max_req_satisfied):
    assert op_req.max_req_satisfied(relic_tier_reqs, unit_relic_tier) == max_req_satisfied
