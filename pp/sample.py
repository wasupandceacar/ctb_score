from osu_parser.beatmap import Beatmap
from osu.ctb.difficulty import Difficulty
from ppCalc import calculate_pp

beatmap = Beatmap("test.osu")

difficulty = Difficulty(beatmap, 0)
print("Calculation:")
print("Stars: {}, PP: {}, MaxCombo: {}\n".format(difficulty.star_rating, calculate_pp(difficulty, 1, beatmap.max_combo, 0), beatmap.max_combo))

"""
m = {"NOMOD": 0, "EASY": 2, "HIDDEN": 8, "HARDROCK": 16, "DOUBLETIME": 64, "HALFTIME": 256, "FLASHLIGHT": 1024}
for key in m.keys():
    difficulty = Difficulty(beatmap, m[key])
    print("Mods: {}".format(key))
    print("Stars: {}".format(difficulty.star_rating))
    print("PP: {}\n".format(calculate_pp(difficulty, 1, beatmap.max_combo, 0)))
"""
