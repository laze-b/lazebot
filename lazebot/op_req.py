from importlib import resources

import pandas as pd

from lazebot import data


def fetch_op_reqs():
    """
    Fetch op requirements from the data file.

    :return: (DataFrame) Data frame matching the data in the data file
    """

    file = resources.files(data).joinpath('op_req.txt')
    op_req = pd.read_csv(file, sep='\t')
    # relic tiers start at 5 in phase 0, max is 9
    op_req["relic_tier"] = (op_req["phase"] + 4).clip(0, 9)
    return op_req


def fetch_op_req_relic_tiers(op_req):
    """
    Fetch operation requirement tiers.

    :param op_req: (DataFrame) A pandas DataFrame, must contain columns "baseId" and "relic_tier" representing
        individual operation requirements
    :return: (Dictionary) key = baseId, value = list of relic tiers representing each ops requirement
    """

    # map to group tiers by baseId
    grouped = op_req[["baseId", "relic_tier"]].groupby("baseId").agg(
        func=lambda x: list(x)
    )
    return grouped["relic_tier"].to_dict()


def reqs_satisfied(relic_tier_reqs, unit_relic_tier):
    """
    Calculate the number of op requirements satisfied by a given unit relic tier. This will account for
    the fact that the unit may be used in multiple phases by avoiding double counting across relic tiers.
    For example, if the reqs are [5, 6] and the unit is 6, this would only count as satisfying 1 req since
    a single unit could be applied multiple times.

    :param relic_tier_reqs: (list of int) list of all op relic tier requirements
    :param unit_relic_tier: (int) relic tier of the unit
    :return: (int) count of relic tier requirements satisfied by the unit
    """
    total_count = 0
    matching = [rt for rt in relic_tier_reqs if rt <= unit_relic_tier]
    for current_relic_tier in range(unit_relic_tier, 4, -1):
        # add the current tier to the count
        current_count = matching.count(current_relic_tier)
        total_count += current_count
        # remove lower tiers to prevent duplicate counting
        for lower_tier in range(current_relic_tier - 1, 4, -1):
            for x in range(current_count):
                if lower_tier in matching:
                    matching.remove(lower_tier)
        matching = [rt for rt in matching if rt < current_relic_tier]

    return total_count


def max_req_satisfied(relic_tier_reqs, unit_relic_tier):
    """
    Get the max relic tier req that is satisfied by the unit

    :param relic_tier_reqs: (list of int) list of reqs
    :param unit_relic_tier: (int) unit relic tier

    :return: max relic tier req satisfied, or -1 if none are satisfied
    """
    matching = [rt for rt in relic_tier_reqs if rt <= unit_relic_tier]
    if matching:
        return max(matching)
    else:
        return -1
