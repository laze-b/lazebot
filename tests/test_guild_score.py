import pytest
import lazebot.game_data as gd
import lazebot.guild_op_score as gs


def test_guild_op():
    op_req = gd.OpReq("test", [5])
    guild_op = gs.GuildOp(op_req)
    assert not guild_op.guildUnits


def test_stuff():
    a = [1, 2, 3, 4, 5]
    assert a[0:-1] == [0]