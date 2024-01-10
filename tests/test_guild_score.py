import pytest
import lazebot.guild_score as gs


def test_guild_op():
    op_req = gs.gd.OpReq("test", [5])
    guild_op = gs.GuildOp(op_req)
    assert guild_op.guildUnits is None
