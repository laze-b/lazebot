"""
This module calculates the value of various items in the game.

Functions:
    compute_gear_value - compute the value of gear levels
    compute_shard_value - compute the value of rarity (star) levels
"""


def compute_gear_value(my_relic_tier: int, baseline_relic_tier: int) -> float:
    """
    Compute the value of a relic tier above a baseline.

    :param my_relic_tier: The relic tier we are valuing between [-1-9], -1 means non-relic (G12 or less)
    :param baseline_relic_tier: The baseline relic tier between [-1-9], -1 means non-relic (G12 or less).
        We only value the tiers above this.
    :return: estimated crystal value
    """
    value = 0.
    if my_relic_tier > baseline_relic_tier:
        for r in range(baseline_relic_tier + 1, my_relic_tier + 1):
            value += __relic_values[r]
    return value


def compute_shard_value(my_rarity: int, baseline_rarity: int) -> float:
    """
    Compute the value of a rarity (stars) above baseline.

    :param my_rarity: The rarity we are valuing between [0-7]. 0 means not unlocked yet.
    :param baseline_rarity: The baseline rarity between [0-7]. 0 means not unlocked yet.
        We only value the stars above this.
    :return: estimated crystal value
    """
    value = 0.
    if my_rarity > baseline_rarity:
        for r in range(baseline_rarity, my_rarity):
            value += __shard_values[r]
    return value


__value_salvagewhite = 100 / ((120 / 16) * 1.37)  # 9.732 (farming cost)
__value_salvagegreen = 100 / ((120 / 16) * .93)  # 14.337 (farming cost)
__value_salvageblue = 100 / ((120 / 16) * .66)  # 20.202 (farming cost)
__value_carbonite = 500 / 160  # 3.125 (relic pack)
__value_bronzium = 500 / 41.75  # 11.976 (relic pack)
# cheap for OG guild tokens, value opportunity cost of not buying bronzium (150/45 chromium == 15/45 bronzium
__value_chromium = __value_bronzium * (15 / 45) / (150 / 45)  # 1.198
__value_aurodium = 0.  # essentially free with mk1 guild tokens
__value_electrium = 500 / 8.1  # 61.728 (relic pack)
__value_zinbiddle = 500 / 6.4  # 78.125 (relic pack)
__value_aero = __value_electrium * 200 / 100  # 123.457 (value against electrium using mk3 comp)
__value_impulse = __value_electrium * 265 / 100  # 163.580 (value against electrium using mk3 comp)
__value_gyrda = 1250 / 5  # 250 (crystal cost)
__value_kyro = 50 / (12 * .2)  # 20.833 (farming cost)
# difficult to value - fluid with mk2 guild and fleet so value against gyrda ¯\_(ツ)_/¯
__value_g12_rs_armatek = __value_gyrda / 13  # 19.231
# these are less valuable than armatek, so adjust using mk2 guild
__value_g12_rs_czerka = __value_g12_rs_armatek * 855 / 1005  # 16.361
# these can exchange for impulse/electrium, so average those out
__value_g12_ls_armatek = (__value_electrium * 15 / 80 + __value_impulse * 12 / 110) / 2  # 14.710
# 24% of these can exchange for electrium, 24% are fluid with fleet so use weighted value
__value_g12_purple = .24 * __value_electrium * 15 / 80 + .76 * __value_g12_rs_armatek  # 17.393

__value_r0 = 90 * __value_g12_ls_armatek + 150 * __value_g12_rs_armatek + \
             80 * __value_g12_rs_czerka + 200 * __value_g12_purple + 100 * __value_kyro

__value_r1 = 40 * __value_carbonite

__value_r2 = 30 * __value_carbonite + 40 * __value_bronzium + 15 * __value_salvagewhite

__value_r3 = 30 * __value_carbonite + 40 * __value_bronzium + 20 * __value_chromium + \
             20 * __value_salvagewhite + 15 * __value_salvagegreen

__value_r4 = 30 * __value_carbonite + 40 * __value_bronzium + 40 * __value_chromium + \
             20 * __value_salvagewhite + 25 * __value_salvagegreen

__value_r5 = 30 * __value_carbonite + 40 * __value_bronzium + 30 * __value_chromium + \
             20 * __value_aurodium + \
             20 * __value_salvagewhite + 25 * __value_salvagegreen + 15 * __value_salvageblue

__value_r6 = 20 * __value_carbonite + 30 * __value_bronzium + 30 * __value_chromium + \
             20 * __value_aurodium + 20 * __value_electrium + \
             20 * __value_salvagewhite + 25 * __value_salvagegreen + 25 * __value_salvageblue

__value_r7 = 20 * __value_carbonite + 30 * __value_bronzium + 20 * __value_chromium + \
             20 * __value_aurodium + 20 * __value_electrium + 10 * __value_zinbiddle + \
             20 * __value_salvagewhite + 25 * __value_salvagegreen + 35 * __value_salvageblue

__value_r8 = 20 * __value_chromium + 20 * __value_aurodium + 20 * __value_electrium + \
             20 * __value_zinbiddle + 20 * __value_aero + 20 * __value_impulse + \
             20 * __value_salvagewhite + 25 * __value_salvagegreen + 45 * __value_salvageblue

__value_r9 = 20 * __value_chromium + 20 * __value_aurodium + 20 * __value_electrium + \
             20 * __value_zinbiddle + 20 * __value_aero + 20 * __value_impulse + 20 * __value_gyrda + \
             30 * __value_salvagewhite + 30 * __value_salvagegreen + 55 * __value_salvageblue

__relic_values = [
    __value_r0,  # 11,079
    __value_r1,  # 125
    __value_r2,  # 718
    __value_r3,  # 1,006
    __value_r4,  # 1,174
    __value_r5,  # 1,465
    __value_r6,  # 2,750
    __value_r7,  # 3,722
    __value_r8,  # 10,024
    __value_r9  # 15,395
]

__shard_value = 50 / (120 / 16 / 3)  # 20 (farming cost)

__shard_values = [
    __shard_value * 10,  # 200
    __shard_value * 15,  # 300
    __shard_value * 25,  # 500
    __shard_value * 30,  # 600
    __shard_value * 65,  # 1300
    __shard_value * 85,  # 1700
    __shard_value * 100  # 2000
]
