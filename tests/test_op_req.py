import pytest
from lazebot import op_req


def test_op_req_data():
    assert op_req.__OP_REQ.shape == (1710, 8)


def test_fetch_base_ids():
    assert len(op_req.__fetch_unique_base_ids(6, [])) == 274
    assert len(op_req.__fetch_unique_base_ids(6, ["Scarif", "Hoth"])) == 270
    assert len(op_req.__fetch_unique_base_ids(5, [])) == 265
    assert len(op_req.__fetch_unique_base_ids(5, ["Vandor"])) == 262
    assert len(op_req.__fetch_unique_base_ids(1, [])) == 113
    assert len(op_req.__fetch_unique_base_ids(1, ["Mustafar"])) == 80


def test_fetch_relic_tiers():
    assert op_req.__fetch_req_count("BOBAFETTSCION", 1, []) == 5
    assert op_req.__fetch_req_count("BOBAFETTSCION", 2, []) == 12
    assert op_req.__fetch_req_count("BOBAFETTSCION", 3, []) == 10
    assert op_req.__fetch_req_count("BOBAFETTSCION", 4, []) == 6
    assert op_req.__fetch_req_count("BOBAFETTSCION", 5, []) == 9
    assert op_req.__fetch_req_count("BOBAFETTSCION", 5, ["Malachor"]) == 2
    assert op_req.__fetch_req_count("BOBAFETTSCION", 6, []) == 9


def test_fetch_counts_by_base_id_and_phase():
    result = op_req.fetch_counts_by_base_id_and_phase()
    assert len(result.keys()) == 274
    assert result["BOBAFETTSCION"] == {1: 5, 2: 12, 3: 10, 4: 6, 5: 9, 6: 9}
    assert result["JEDIKNIGHTGUARDIAN"] == {3: 3}

    result = op_req.fetch_counts_by_base_id_and_phase(max_phase=3)
    assert len(result.keys()) == 226
    assert result["BOBAFETTSCION"] == {1: 5, 2: 12, 3: 10}

    result = op_req.fetch_counts_by_base_id_and_phase(
        max_phase=4, planets_to_exclude=["Haven-class Medical Station", "Lothal"])
    assert len(result.keys()) == 237
    assert result["BOBAFETTSCION"] == {1: 5, 2: 12, 3: 10, 4: 2}
