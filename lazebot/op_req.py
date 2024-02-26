from importlib import resources
import pandas as pd
from pandas import DataFrame
from lazebot import data


def __fetch_op_reqs() -> DataFrame:
    """
    Fetch op requirements from the data file.

    :return: Data frame matching the data in the data file
    """

    file = resources.files(data).joinpath('op_req.txt')
    op_req = pd.read_csv(file, sep='\t')
    return op_req


__OP_REQ: DataFrame = __fetch_op_reqs()


def __fetch_unique_base_ids(max_phase: int, planets_to_exclude: list[str]) -> set[str]:
    """
    Fetch the unique set of baseId values used in operations.

    :return: set of baseIds
    """

    query = f'phase <= {max_phase}'
    if planets_to_exclude:
        query = query + f' and planet not in {planets_to_exclude}'
    return set(__OP_REQ.query(query)["baseId"])


def __fetch_req_count(base_id: str, phase: int, planets_to_exclude: list[str]) -> int:
    """
    Fetch operation requirement counts for a unit and phase.

    :param base_id - the unit identifier
    :param phase - the op phase
    :return: count of requirements for the given unit and phase
    """
    query = f'baseId == "{base_id}" and phase == {phase}'
    if planets_to_exclude:
        query = query + f' and planet not in {planets_to_exclude}'
    return len(__OP_REQ.query(query))


def fetch_counts_by_base_id_and_phase(
        max_phase: int = 6,
        planets_to_exclude: list[str] = None) -> dict[str, dict[int, int]]:
    base_ids = __fetch_unique_base_ids(max_phase, planets_to_exclude)
    all_op_reqs = {}
    for base_id in base_ids:
        all_op_reqs[base_id] = {}
        for phase in range(1, max_phase + 1):
            all_op_reqs[base_id][phase] = __fetch_req_count(base_id, phase, planets_to_exclude)
    return all_op_reqs
