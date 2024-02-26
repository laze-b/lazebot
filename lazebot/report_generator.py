import os

from lazebot import guild_op_score
from lazebot.game_data import Unit
from lazebot.guild_op_score import PlayerScore

MAX_REPORT_LENGTH = 4090  # discord embed maximum
OPS_SCORE_TITLE = '''\
====  Ops Score Report (RoTE)  ====
Scores reflect how much a guild relies on a player for TB ops. Rare units and higher relics contribute the most.

Score = Estimated crystal cost of replacing ops units'''


def ops_needed_report(ally_code: str, num_backups: int = 1, max_phase: int = 6,
                      planets_to_exclude: list[str] = None) -> (str, str):
    return "", ""


def op_score_report(ally_code: str, compute_guild: bool, max_phase: int = 6, verbose: bool = True) -> (str, str):
    score_params = guild_op_score.__DEFAULT_SCORE_PARAMS
    if compute_guild:
        guild_name, player_scores = guild_op_score.compute_guild_score(ally_code, max_phase, score_params)
        report = __guild_op_score_report(guild_name, player_scores)
    else:
        player_score = guild_op_score.compute_player_score(ally_code, max_phase, score_params)
        player_score.unitScores.sort(reverse=True, key=lambda x: x.score())
        report = __player_op_score_report(player_score, verbose)

    if len(report) > MAX_REPORT_LENGTH:
        report = __truncate_report(report, MAX_REPORT_LENGTH)
    return OPS_SCORE_TITLE, f"```{report}```"


def __guild_op_score_report(guild_name: str, player_scores: list[PlayerScore]) -> str:
    guild_score = round(sum(x.score() for x in player_scores))
    player_scores.sort(reverse=True, key=lambda x: x.score())
    output = [f'Total score for {guild_name}: {guild_score:,}', '']
    for player_score in player_scores:
        output.append(f"{player_score.player.name} ({player_score.player.allyCode}): {round(player_score.score()):,}")
    return os.linesep.join(output)


def __player_op_score_report(player_score: PlayerScore, verbose: bool) -> str:
    output = [f'Total score for {player_score.player.name}: {round(player_score.score()):,}', '', 'Units:']
    for unit_score in player_score.unitScores:
        output.append(f'{unit_score.unit.name}: {round(unit_score.score()):,}')
        if verbose:
            relic_tier = '' if unit_score.unit.ship else f' @ R{str(min(unit_score.phase + 4, 9))}'
            backups = [f"{__unit_desc(component.guildUnit)}" for component in unit_score.components]
            output.append(f"  {unit_score.opReqCount} req in P{unit_score.phase}{relic_tier}")
            output.append(f"  backups = {', '.join(backups)}")
    return os.linesep.join(output)


def __unit_desc(unit: Unit, score: float = None):
    if unit.ship:
        desc = [f"{unit.rarity}*"]
    else:
        if unit.gear < 12:
            desc = [f"{unit.rarity}*, G{unit.gear}"]
        elif unit.gear == 12:
            desc = [f"G{unit.gear}"]
        else:
            desc = [f"R{unit.relic}"]
    if score is not None:
        desc.append(f" = {round(score):,}")
    return "".join(desc)


def __truncate_report(report: str, length: int):
    if len(report) > length:
        print(f"Truncating length = {len(report)}")
        report = report[:length - 32] + '\n---------- truncated ----------'
    return report
