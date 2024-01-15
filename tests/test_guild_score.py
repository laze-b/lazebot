import pytest
import lazebot.game_data as gd
import lazebot.guild_score as gs


def test_guild_op():
    op_req = gd.OpReq("test", [5])
    guild_op = gs.GuildOp(op_req)
    assert not guild_op.guildUnits