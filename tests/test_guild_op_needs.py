import pytest
from lazebot import guild_op_needs
from lazebot.guild_op_needs import PhaseNeed
from lazebot.guild_op_needs import OpNeed
from lazebot.game_data import Unit


def test_get_op_needs():
    # {base_id: {phase: count}}
    all_op_reqs = {
        "BOBAFETTSCION": {
            1: 10,
            2: 4,
            3: 2,
            4: 2,
            5: 1,
            6: 1,
        },
        "TIEINTERCEPTOR": {
            3: 1,
            4: 3,
            5: 5,
        },
    }

    initial_phase_needs = {
        1: PhaseNeed({
            "BOBAFETTSCION": OpNeed(10, 2, 0),
        }),
        2: PhaseNeed({
            "BOBAFETTSCION": OpNeed(4, 2, 0),
        }),
        3: PhaseNeed({
            "BOBAFETTSCION": OpNeed(2, 2, 0),
            "TIEINTERCEPTOR": OpNeed(1, 2, 0),
        }),
        4: PhaseNeed({
            "BOBAFETTSCION": OpNeed(2, 2, 0),
            "TIEINTERCEPTOR": OpNeed(3, 2, 0),
        }),
        5: PhaseNeed({
            "BOBAFETTSCION": OpNeed(1, 2, 0),
            "TIEINTERCEPTOR": OpNeed(5, 2, 0),
        }),
        6: PhaseNeed({
            "BOBAFETTSCION": OpNeed(1, 2, 0),
        }),
    }

    # {base_id: list[Unit]
    all_guild_units = {
        "BOBAFETTSCION": [
            Unit("BOBAFETTSCION", "DBB", 13, 9, 7, False),
            Unit("BOBAFETTSCION", "DBB", 13, 7, 7, False),
            Unit("BOBAFETTSCION", "DBB", 13, 7, 7, False),
            Unit("BOBAFETTSCION", "DBB", 13, 6, 7, False),
            Unit("BOBAFETTSCION", "DBB", 13, 6, 7, False),
            Unit("BOBAFETTSCION", "DBB", 13, 6, 7, False),
            Unit("BOBAFETTSCION", "DBB", 13, 6, 7, False),
            Unit("BOBAFETTSCION", "DBB", 13, 5, 7, False),
            Unit("BOBAFETTSCION", "DBB", 12, -1, 7, False),
        ],
        "TIEINTERCEPTOR": [
            Unit("TIEINTERCEPTOR", "TI-INT", -1, -1, 7, True),
            Unit("TIEINTERCEPTOR", "TI-INT", -1, -1, 7, True),
            Unit("TIEINTERCEPTOR", "TI-INT", -1, -1, 7, True),
            Unit("TIEINTERCEPTOR", "TI-INT", -1, -1, 7, True),
            Unit("TIEINTERCEPTOR", "TI-INT", -1, -1, 6, True),
        ]
    }

    filled_phase_needs = {
        1: PhaseNeed({
            "BOBAFETTSCION": OpNeed(10, 2, 8),
        }),
        3: PhaseNeed({
            "BOBAFETTSCION": OpNeed(2, 2, 3),
        }),
        4: PhaseNeed({
            "BOBAFETTSCION": OpNeed(2, 2, 1),
            "TIEINTERCEPTOR": OpNeed(3, 2, 4),
        }),
        5: PhaseNeed({
            "BOBAFETTSCION": OpNeed(1, 2, 1),
            "TIEINTERCEPTOR": OpNeed(5, 2, 4),
        }),
        6: PhaseNeed({
            "BOBAFETTSCION": OpNeed(1, 2, 1),
        }),
    }

    result = guild_op_needs.__get_phase_needs(all_op_reqs, 2)
    assert result == initial_phase_needs

    result = guild_op_needs.__fill_phase_needs(result, all_guild_units)
    assert result == filled_phase_needs
