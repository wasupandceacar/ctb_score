import math

def calculate_pp(diff, accuracy, combo, miss):
    """
    Calculate pp for gameplay

    diff        -- Difficulty object
    accuracy    -- Accuracy of the play             (Float 0-1)
    combo       -- MaxCombo achived during the play (Int)
    miss        -- Amount of misses during the play (Int)
    return      -- Total pp for gameplay
    """
    pp = pow((5 * max(1, diff.star_rating / 0.0049) - 4), 2) / 100000
    length_bonus = 0.95 + 0.4 * min(1, combo / 3000)
    if combo > 3000:
        length_bonus += math.log10(combo / 3000) * 0.5

    pp *= length_bonus
    pp *= pow(0.97, miss)
    pp *= min(pow(combo, 0.8) / pow(diff.beatmap.max_combo, 0.8), 1)

    AR=change_AR(diff.beatmap.difficulty["ApproachRate"], diff)
    approachRateFactor=1
    if AR > 9:
        approachRateFactor += 0.1 * (AR - 9)
    elif AR < 8:
        approachRateFactor += 0.025 * (8 - AR)

    pp*=approachRateFactor

    if diff.mods & 1 << 3 > 0:    #HD
        pp *= 1.05 + 0.075 * (10 - min(10, AR))

    if diff.mods & 1 << 10 > 0:    #FL
        pp *= 1.35 * length_bonus

    pp *= pow(accuracy, 5.5)

    if diff.mods & 1 << 0 > 0:    #NF
        pp *= 0.9

    if diff.mods & 1 << 12 > 0:    #SO
        pp *= 0.95

    return pp

def change_AR(AR, diff):
    speed = 1
    if diff.mods & 1 << 6 > 0:  # DT
        speed *= 1.5
    if diff.mods & 1 << 8 > 0:  # HT
        speed *= 0.75
    new_ar = AR
    if new_ar <= 5:
        arms = 1800 - 120 * new_ar
    else:
        arms = 1200 - 150 * (new_ar - 5)
    arms = min(1800, max(450, arms)) / speed
    if arms > 1200:
        new_ar = (1800 - arms) / 120
    else:
        new_ar = (1200 - arms) / 150 + 5
    return math.floor(new_ar * 100) / 100
