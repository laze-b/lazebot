from lazebot import op_req
from lazebot import game_data
from dataclasses import dataclass


@dataclass(frozen=True)
class PhaseNeed:
    primaryNeeds: dict[str: int]
    backupNeeds: dict[str: int]


def compute_op_needs(ally_code: str, num_backups: int, max_phase: int,
                     planets_to_exclude: list[str]) -> (str, dict[int, PhaseNeed]):
    all_op_reqs = op_req.fetch_counts_by_base_id_and_phase(max_phase, planets_to_exclude)
    (guild_name, players, all_guild_units) = game_data.fetch_players_and_guild_units(ally_code, set(all_op_reqs.keys()))

    phase_needs = __get_op_needs(all_op_reqs, num_backups)

    # now fill them with what the players have to get what's left
    for base_id, units in all_guild_units:
        for unit in units:
            min_phase_satisfied = unit.relic - 4
            if min_phase_satisfied >= 1:
                __fill_required_unit(all_op_reqs, base_id, min_phase_satisfied)

    return guild_name, phase_needs


def __get_op_needs(all_op_reqs, num_backups):
    phase_needs = {}
    for base_id, phase_counts in all_op_reqs:
        for phase, count in phase_counts:
            if phase not in phase_needs:
                phase_needs[phase] = PhaseNeed({}, {})
            phase_needs[phase].primaryNeeds[base_id] = count
            phase_needs[phase].backupNeeds[base_id] = num_backups
    return phase_needs


def __fill_required_unit(all_op_reqs, base_id, min_phase_satisfied):
    for phase, count in all_op_reqs[base_id]:
        if phase >= min_phase_satisfied:
            all_op_reqs[base_id][phase] = all_op_reqs[base_id][phase] - 1
            if all_op_reqs[base_id][phase] == 0:
                all_op_reqs[base_id].pop(phase, None)
                # todo finish