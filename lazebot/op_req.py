import pandas as pd


def fetch_op_reqs():
    df = pd.read_csv("data/op_req.txt")
    # for op in reader:
    #     base_id = op["baseId"]
    #     name = op["character_name"]
    #     phase = op["phase"]
    #     relic_tier = min(9, int(phase) + 4)
    #     op_req = op_reqs.setdefault(base_id, OpReq(name))
    #     op_req.add_req(relic_tier)
    print(df)
    return df


op_reqs = fetch_op_reqs()


class OpReq:
    def __init__(self, name, relic_tiers=None):
        if relic_tiers is None:
            relic_tiers = []
        self.name = name
        self.relic_tiers = relic_tiers

    def add_req(self, relic_tier):
        self.relic_tiers.append(relic_tier)

    def total_units(self, max_relic_tier):
        total_count = 0
        matching = [rt for rt in self.relic_tiers if rt <= max_relic_tier]
        for current_relic_tier in range(max_relic_tier, 4, -1):
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

    def max_matching(self, relic_tier):
        matching = [rt for rt in self.relic_tiers if rt <= relic_tier]
        if matching:
            return max(matching)
        else:
            return -1

    def __str__(self):
        return f'OpReq("{self.name}", {self.relic_tiers}'

    def __repr__(self):
        return f'OpReq("{self.name}", {self.relic_tiers}'
