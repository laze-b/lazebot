import pytest
from lazebot import op_req


def test_op_req_data():
    assert op_req.__OP_REQ.shape == (1710, 8)


def test_fetch_base_ids():
    assert len(op_req.fetch_unique_base_ids()) == 274


def test_fetch_relic_tiers():
    assert op_req.fetch_req_count("BOBAFETTSCION", 1) == 5
    assert op_req.fetch_req_count("BOBAFETTSCION", 2) == 12
    assert op_req.fetch_req_count("BOBAFETTSCION", 3) == 10
    assert op_req.fetch_req_count("BOBAFETTSCION", 4) == 6
    assert op_req.fetch_req_count("BOBAFETTSCION", 5) == 9
    assert op_req.fetch_req_count("BOBAFETTSCION", 6) == 9
