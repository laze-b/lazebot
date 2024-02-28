from lazebot import op_req
from lazebot import game_data
from lazebot.game_data import Unit
from dataclasses import dataclass


@dataclass
class OpNeed:
    primary: int
    backups: int
    have: int


@dataclass(frozen=True)
class PhaseNeed:
    units: dict[str: OpNeed]  # [base_id: OpNeed]


@dataclass(frozen=True)
class UnitNeed:
    ship: bool
    primary: list[str]
    backups: list[str]


def compute_op_unit_needs(ally_code: str, num_backups: int, max_phase: int,
                          planets_to_exclude: list[str]) -> (str, dict[str, UnitNeed]):
    all_op_reqs = op_req.fetch_counts_by_base_id_and_phase(max_phase, planets_to_exclude)
    (guild_name, _, all_guild_units) = game_data.fetch_players_and_guild_units(ally_code, set(all_op_reqs.keys()))
    phase_needs = __compute_phase_needs(all_op_reqs, all_guild_units, num_backups)
    unit_needs = __compute_unit_needs(phase_needs)
    return guild_name, unit_needs


def compute_op_phase_needs(ally_code: str, num_backups: int, max_phase: int,
                           planets_to_exclude: list[str]) -> (str, dict[int, PhaseNeed]):
    # {base_id: {phase: count}}
    all_op_reqs = op_req.fetch_counts_by_base_id_and_phase(max_phase, planets_to_exclude)
    (guild_name, _, all_guild_units) = game_data.fetch_players_and_guild_units(ally_code, set(all_op_reqs.keys()))
    phase_needs = __compute_phase_needs(all_op_reqs, all_guild_units, num_backups)
    return guild_name, phase_needs


def __compute_unit_needs(phase_needs: dict[int: PhaseNeed]) -> dict[str, UnitNeed]:
    unit_needs = {}
    for phase in sorted(phase_needs.keys(), reverse=True):
        for base_id, op_need in phase_needs[phase].units.items():
            if base_id not in unit_needs:
                unit_needs[base_id] = UnitNeed([], [])
            if op_need.primary < op_need.have:
                unit_needs[base_id].primary.append()

    return unit_needs


def __compute_phase_needs(all_op_reqs: dict[str: dict[int: int]], all_guild_units: dict[str: list[Unit]],
                          num_backups: int) -> dict[int: dict[str: OpNeed]]:
    phase_needs = __get_phase_needs(all_op_reqs, num_backups)
    return __fill_phase_needs(phase_needs, all_guild_units)


def __get_phase_needs(all_op_reqs: dict[str: dict[int: int]], num_backups: int) -> dict[int: PhaseNeed]:
    phase_needs = {}
    for base_id, phase_counts in all_op_reqs.items():
        for phase, count in phase_counts.items():
            if phase not in phase_needs:
                phase_needs[phase] = PhaseNeed({})
            op_need = OpNeed(count, num_backups, 0)
            phase_needs[phase].units[base_id] = op_need
    return phase_needs


def __fill_phase_needs(phase_needs: dict[int: dict[str: OpNeed]],
                       all_guild_units: dict[str: list[Unit]]) -> dict[int: dict[str: OpNeed]]:
    for base_id, units in all_guild_units.items():
        for unit in units:
            if unit.ship:
                max_phase_satisfied = 6 if unit.rarity == 7 else 0
            else:
                max_phase_satisfied = unit.relic - 4 if unit.relic < 9 else 6
            if max_phase_satisfied >= 1:
                __fill_required_unit(phase_needs, base_id, max_phase_satisfied)

    # remove all fully filled
    pruned_phased_needs = {}
    for phase, phase_need in phase_needs.items():
        for base_id, op_need in phase_need.units.items():
            if op_need.have < op_need.primary + op_need.backups:
                if phase not in pruned_phased_needs:
                    pruned_phased_needs[phase] = PhaseNeed({})
                pruned_phased_needs[phase].units[base_id] = op_need
    return pruned_phased_needs


def __fill_required_unit(phase_needs: dict[int: PhaseNeed], base_id: str, max_phase_satisfied: int):
    for phase, phase_need in phase_needs.items():
        if phase <= max_phase_satisfied:
            if base_id in phase_need.units:
                op_need = phase_need.units[base_id]
                op_need.have = op_need.have + 1
