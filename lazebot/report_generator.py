from lazebot import guild_op_score
from lazebot.guild_op_score import ScoreParams
from lazebot.guild_op_score import PlayerScore
from lazebot.game_data import Unit
import os


MAX_REPORT_LENGTH = 2000  # discord maximum


async def op_score_report(ally_code: str, compute_guild: bool, max_phase: int = 6, verbose: bool = True) -> str:
    score_params = guild_op_score.__DEFAULT_SCORE_PARAMS
    if compute_guild:
        guild_name, player_scores = guild_op_score.compute_guild_score(ally_code, max_phase, score_params)
        report = __guild_op_score_report(guild_name, player_scores)
    else:
        player_score = guild_op_score.compute_player_score(ally_code, max_phase, score_params)
        player_score.unitScores.sort(reverse=True, key=lambda x: x.score())
        report = __player_op_score_report(player_score, verbose)

    if len(report) > MAX_REPORT_LENGTH - 6:
        report = __truncate_report(report, MAX_REPORT_LENGTH - 6)  # leave 6 for code block backticks
    return f"```{report}```"


def __guild_op_score_report(guild_name: str, player_scores: list[PlayerScore]) -> str:
    guild_score = round(sum(x.score() for x in player_scores))
    player_scores.sort(reverse=True, key=lambda x: x.score())
    output = [f'''\
---- Ops Score Report (RoTE) ----
Based on investment into rare 
units for the guild.

Score for {guild_name}: {guild_score:,}
''']
    for player_score in player_scores:
        output.append(f"{player_score.player.name} ({player_score.player.allyCode}): {round(player_score.score()):,}")
    return os.linesep.join(output)


def __player_op_score_report(player_score: PlayerScore, verbose: bool) -> str:
    output = [f'''\
---- Ops Score Report (RoTE) ----
Based on investment into rare 
units for the guild.

Score for {player_score.player.name}: {round(player_score.score()):,}
''']
    for unit_score in player_score.unitScores:
        output.append(f'{unit_score.unit.name}: {__unit_desc(unit_score.unit, unit_score.score())}')
        if verbose:
            relic_tier = '' if unit_score.unit.ship else f' at R{str(min(unit_score.phase + 4, 9))}'
            output.append(f'  {unit_score.opReqCount} required in phase {unit_score.phase}{relic_tier}')
            output.append('  Backups:')
            for component in unit_score.components:
                output.append(
                    f"      {component.guildUnit.owner}: {__unit_desc(component.guildUnit, round(component.score))}")
    return os.linesep.join(output)


def __unit_desc(unit: Unit, score: float):
    if unit.ship:
        desc = [f"{unit.rarity}*"]
    else:
        if unit.gear < 12:
            desc = [f"{unit.rarity}*, G{unit.gear}"]
        elif unit.gear == 12:
            desc = [f"G{unit.gear}"]
        else:
            desc = [f"R{unit.relic}"]
    desc.append(f" ({round(score):,})")
    return "".join(desc)


def __plural(count: int, word: str):
    return f'{count} {word}' if count == 1 else f'{count} {word}s'


def __truncate_report(report: str, length: int):
    if len(report) > length:
        report = report[:length-32] + '\n---------- truncated ----------'
    return report
