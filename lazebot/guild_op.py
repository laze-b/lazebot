class GuildOp:
    def __init__(self, op_req):
        self.opReq = op_req
        self.guildUnits = []

    def add_guild_unit(self, unit):
        self.guildUnits.append(unit)
        self.guildUnits.sort(reverse=True, key=GuildOp.sort_unit)

    @staticmethod
    def sort_unit(unit):
        if unit.gearLevel == 13:
            return unit.gearLevel + unit.relicTier
        else:
            return unit.gearLevel