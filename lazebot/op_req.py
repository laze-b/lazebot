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


def fetch_unique_base_ids() -> set[str]:
    """
    Fetch the unique set of baseId values used in operations.

    :return: set of baseIds
    """

    return set(__OP_REQ["baseId"])


def fetch_req_count(base_id: str, phase: int) -> int:
    """
    Fetch operation requirement counts for a unit and phase.

    :param base_id - the unit identifier
    :param phase - the op phase
    :return: count of requirements for the given unit and phase
    """

    return len(__OP_REQ[(__OP_REQ["baseId"] == base_id) & (__OP_REQ["phase"] == phase)])
