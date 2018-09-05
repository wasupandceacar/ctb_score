from pp.osu_parser.beatmap import Beatmap
from pp.osu.ctb.difficulty import Difficulty
from pp.ppCalc import calculate_pp
import json
import requests
import os

KEY="cff10afa31a4a9cd85aa7bc433c20c862562ed51"

U_URL="https://osu.ppy.sh/api/get_user?k="+KEY

U_BEST_URL="https://osu.ppy.sh/api/get_user_best?k="+KEY

U_RECENT_URL="https://osu.ppy.sh/api/get_user_recent?k="+KEY

MAP_URL="https://osu.ppy.sh/api/get_beatmaps?k="+KEY

def check_user(user):
    response = requests.get(U_URL + "&u=" + user + "&m=2")
    scores = json.loads(response.text)
    if len(scores)==0:
        return False
    else:
        return True

def get_user_best(user, num):
    response = requests.get(U_BEST_URL+"&u="+user+"&m=2&limit=100")
    scores=json.loads(response.text)
    if num>len(scores):
        return None
    else:
        return json.loads(response.text)[num-1]

def get_user_recent(user):
    response = requests.get(U_RECENT_URL + "&u=" + user + "&m=2&limit=50")
    scores = json.loads(response.text)
    if len(scores)==0:
        return 0
    else:
        return json.loads(response.text)[0]

def get_user_pr(user):
    response = requests.get(U_RECENT_URL + "&u=" + user + "&m=2&limit=50")
    scores = json.loads(response.text)
    if len(scores)==0:
        return 0
    else:
        for score in scores:
            if score['rank']!="F":
                return score
        return 1

def get_pp_info(score, user):
    # 无此记录
    if score==None:
        return {"error": "noscore"}
    # 没有最近游戏记录
    if score==0:
        return {"error": "norecent"}
    # 没有最近上传的记录
    if score==1:
        return {"error": "nopr"}
    # 下载
    osu_url="https://osu.ppy.sh/osu/"+score['beatmap_id']
    file=score['beatmap_id']+".osu"
    with open(file, "wb") as code:
        code.write(requests.get(osu_url).content)
    # 分析
    beatmap = Beatmap(file)
    difficulty = Difficulty(beatmap, int(score['enabled_mods']))
    response = requests.get(MAP_URL + "&b=" + score["beatmap_id"] + "&m=2&a=1")
    map=json.loads(response.text)[0]
    response = requests.get(U_URL + "&u=" + user + "&m=2")
    user = json.loads(response.text)[0]
    # 删除
    if os.path.exists(file):
        os.remove(file)
    mod=int(score['enabled_mods'])
    mods=[]
    if mod==0:
        mods="None"
    else:
        if mod & 1 << 0 > 0:
            mods.append("NF")
        if mod & 1 << 1 > 0:
            mods.append("EZ")
        if mod & 1 << 3 > 0:
            mods.append("HD")
        if mod & 1 << 4 > 0:
            mods.append("HR")
        if mod & 1 << 14 > 0:
            mods.append("PF")
        elif mod & 1 << 5 > 0:
            mods.append("SD")
        if mod & 1 << 9 > 0:
            mods.append("NC")
        elif mod & 1 << 6 > 0:
            mods.append("DT")
        if mod & 1 << 8 > 0:
            mods.append("HT")
        if mod & 1 << 10 > 0:
            mods.append("FL")
        if mod & 1 << 12 > 0:
            mods.append("SO")
    return {
        "user": user["username"],
        "name":map["artist"]+" - "+map["title"]+" ["+map["version"]+"]",
        "date":score["date"],
        "rank":score["rank"],
        "cb":score["maxcombo"],
        "mxcb": map['max_combo'],
        "bpm":map["bpm"],
        "acc":str('%.2f'%round(get_acc(score)*100, 2)),
        "off_pp":score["pp"] if "pp" in score else '0',
        "mod":mods,
        "bid":score["beatmap_id"],
        "calc_star":str(round(difficulty.star_rating, 2)),
        "true_pp":str(round(calculate_pp(difficulty, get_acc(score), int(score['maxcombo']), int(score['countmiss'])), 4)),
        "maxcb_pp":str(round(calculate_pp(difficulty, get_acc(score), beatmap.max_combo, 0), 4)),
        "ss_pp": str(round(calculate_pp(difficulty, 1, beatmap.max_combo, 0), 4)),
        "300": score["count300"],
        "100": score["count100"],
        "50": score["count50"],
        "miss": score["countmiss"],
        "perfect": score["perfect"],
        "score": score["score"],
        "creator": map["creator"],
        "CS": map["diff_size"],
        "AR": map['diff_approach'],
        "HP": map['diff_drain'],
        "raw_mod":mod,
        "error": "none"
    }

def get_acc(score):
    return round((int(score["count300"])+int(score["count100"])+int(score["count50"]))/(int(score["count300"])+int(score["count100"])+int(score["count50"])+int(score["countkatu"])+int(score["countmiss"])), 4)