from get import *
from pprint import pprint
from PIL import Image, ImageDraw, ImageFont
import math
import matplotlib.pyplot as plt

BC_URL="http://bloodcat.com/osu/i/"

SKIN_DIC="skin/"

def generate_score_pic(score):
    bg=download_bg(score)
    base_img = Image.open(bg)
    base_img = base_img.resize((1600, 900))
    generate_info_panel(base_img, score)
    generate_rank_panel(base_img, score)
    generate_count(base_img, score)
    generate_combo(base_img, score)
    generate_rank(base_img, score)
    generate_mods(base_img, score)
    generate_pp(base_img, score)
    generate_diff(base_img, score)
    base_img.save(bg, 'png')
    plt.imshow(base_img)
    plt.show(base_img)
    return bg

def generate_info_panel(base_img, score):
    panel_img = Image.open(SKIN_DIC + "alpha.png")
    base_img.paste(panel_img, (0,0,panel_img.size[0],panel_img.size[1]),mask = panel_img.split()[3])
    draw = ImageDraw.Draw(base_img)
    draw.text((10, 14), score["name"], font=ImageFont.truetype(SKIN_DIC + "YuGothM.ttc", 40), fill="white")
    draw.text((10, 60), "Beatmap by "+score["creator"], font=ImageFont.truetype(SKIN_DIC + "YuGothB.ttc", 34), fill="white")
    draw.text((10, 102), "Played by "+score["user"]+" on "+score["date"] + ".", font=ImageFont.truetype(SKIN_DIC + "YuGothB.ttc", 34), fill="white")

def generate_rank_panel(base_img, score):
    panel_img = Image.open(SKIN_DIC + "ranking-panel.png")
    base_img.paste(panel_img, (0,160,panel_img.size[0],160+panel_img.size[1]),mask = panel_img.split()[3])
    layout_number_big(base_img, score['score'], 223, 193)

def generate_count(base_img, score):
    count300_img = Image.open(SKIN_DIC + "mania-hit300.png")
    base_img.paste(count300_img, (0,305,count300_img.size[0],305+count300_img.size[1]),mask = count300_img.split()[3])
    layout_number(base_img, score['300']+"x", 215, 313)
    count100_img = Image.open(SKIN_DIC + "mania-hit100.png")
    base_img.paste(count100_img, (0,425,count100_img.size[0],425+count100_img.size[1]),mask = count100_img.split()[3])
    layout_number(base_img, score['100'] + "x", 215, 433)
    count50_img = Image.open(SKIN_DIC + "mania-hit50.png")
    base_img.paste(count50_img, (0,540,count50_img.size[0],540+count50_img.size[1]),mask = count50_img.split()[3])
    layout_number(base_img, score['50'] + "x", 215, 548)
    count0_img = Image.open(SKIN_DIC + "mania-hit0.png")
    base_img.paste(count0_img, (310,305,310+count0_img.size[0],305+count0_img.size[1]),mask = count0_img.split()[3])
    layout_number(base_img, score['miss'] + "x", 525, 313)

def generate_combo(base_img, score):
    layout_number(base_img, score['cb'] + "/"+ score["mxcb"] +"x", 70, 673)
    layout_number(base_img, score['acc'] + "%", 426, 673)

def generate_rank(base_img, score):
    if score['rank']=="F":
        rank_img = Image.open(SKIN_DIC + "section-fail.png")
        base_img.paste(rank_img, (1200, 160, 1200 + rank_img.size[0], 160 + rank_img.size[1]), mask=rank_img.split()[3])
    else:
        rank_img = Image.open(SKIN_DIC + "ranking-" + score["rank"].lower() + ".png")
        base_img.paste(rank_img, (1200, 160, 1200 + rank_img.size[0], 160 + rank_img.size[1]), mask=rank_img.split()[3])

def generate_mods(base_img, score):
    if score['mod']!="None":
        x = 1490
        for mod in score['mod']:
            mod_img = Image.open(SKIN_DIC + "selection-mod-" + mod + ".png")
            base_img.paste(mod_img, (x, 500, x + mod_img.size[0], 500 + mod_img.size[1]), mask=mod_img.split()[3])
            x-=31

def generate_pp(base_img, score):
    draw = ImageDraw.Draw(base_img)
    draw.text((18, 740), "official pp: " + score["off_pp"] + " pp", font=ImageFont.truetype(SKIN_DIC + "YuGothM.ttc", 34), fill="black")
    draw.text((18, 780), "calculated pp: " + score["true_pp"] + " pp", font=ImageFont.truetype(SKIN_DIC + "YuGothM.ttc", 34), fill="black")
    draw.text((18, 820), "calculated fc pp: " + score["maxcb_pp"] + " pp", font=ImageFont.truetype(SKIN_DIC + "YuGothM.ttc", 34), fill="black")
    draw.text((18, 860), "calculated ss pp: " + score["ss_pp"] + " pp", font=ImageFont.truetype(SKIN_DIC + "YuGothM.ttc", 34), fill="black")
    if score["perfect"]=="1":
        per_img = Image.open(SKIN_DIC + "ranking-perfect.png")
        base_img.paste(per_img, (400, 708, 400 + per_img.size[0], 708 + per_img.size[1]), mask=per_img.split()[3])

def generate_diff(base_img, score):
    raw_mod, old_bpm, old_cs, old_ar, old_hp=score['raw_mod'], float(score['bpm']), float(score['CS']), float(score['AR']), float(score['HP'])
    new_bpm, new_cs, new_ar, new_hp=change_diff(raw_mod, old_bpm, old_cs, old_ar, old_hp)
    draw = ImageDraw.Draw(base_img)
    draw.text((1027, 14), "calculated star: " + score["calc_star"] + " star", font=ImageFont.truetype(SKIN_DIC + "YuGothB.ttc", 46), fill="white")
    if new_bpm>old_bpm:
        draw.text((1030, 74), "bpm: " + str(new_bpm) +" ↑", font=ImageFont.truetype(SKIN_DIC + "YuGothM.ttc", 22), fill="red")
    elif new_bpm<old_bpm:
        draw.text((1030, 74), "bpm: " + str(new_bpm) + " ↓", font=ImageFont.truetype(SKIN_DIC + "YuGothM.ttc", 22), fill="green")
    else:
        draw.text((1030, 74), "bpm: " + str(new_bpm), font=ImageFont.truetype(SKIN_DIC + "YuGothM.ttc", 22), fill="white")
    if new_cs>old_cs:
        draw.text((1210, 74), "CS: " + str(new_cs) +" ↑", font=ImageFont.truetype(SKIN_DIC + "YuGothM.ttc", 22), fill="red")
    elif new_cs<old_cs:
        draw.text((1210, 74), "CS: " + str(new_cs) + " ↓", font=ImageFont.truetype(SKIN_DIC + "YuGothM.ttc", 22), fill="green")
    else:
        draw.text((1210, 74), "CS: " + str(new_cs), font=ImageFont.truetype(SKIN_DIC + "YuGothM.ttc", 22), fill="white")
    if new_ar>old_ar:
        draw.text((1330, 74), "AR: " + str(new_ar) +" ↑", font=ImageFont.truetype(SKIN_DIC + "YuGothM.ttc", 22), fill="red")
    elif new_ar<old_ar:
        draw.text((1330, 74), "AR: " + str(new_ar) + " ↓", font=ImageFont.truetype(SKIN_DIC + "YuGothM.ttc", 22), fill="green")
    else:
        draw.text((1330, 74), "AR: " + str(new_ar), font=ImageFont.truetype(SKIN_DIC + "YuGothM.ttc", 22), fill="white")
    if new_hp>old_hp:
        draw.text((1450, 74), "HP: " + str(new_hp) +" ↑", font=ImageFont.truetype(SKIN_DIC + "YuGothM.ttc", 22), fill="red")
    elif new_hp<old_hp:
        draw.text((1450, 74), "HP: " + str(new_hp) + " ↓", font=ImageFont.truetype(SKIN_DIC + "YuGothM.ttc", 22), fill="green")
    else:
        draw.text((1450, 74), "HP: " + str(new_hp), font=ImageFont.truetype(SKIN_DIC + "YuGothM.ttc", 22), fill="white")

def layout_number_big(base_img, numstr, x, y):
    for ch in numstr:
        if ch.isdigit():
            num_img = Image.open(SKIN_DIC + "score-"+ch+".png")
            num_img=num_img.resize((int(num_img.size[0]*1.3), int(num_img.size[1]*1.3)), Image.ANTIALIAS)
            base_img.paste(num_img, (x, y, x + num_img.size[0], y + num_img.size[1]), mask=num_img.split()[3])
            x+=45

def layout_number(base_img, numstr, x, y):
    for ch in numstr:
        if ch.isdigit():
            num_img = Image.open(SKIN_DIC + "score-"+ch+".png")
            base_img.paste(num_img, (x, y, x + num_img.size[0], y + num_img.size[1]), mask=num_img.split()[3])
            x+=32
        elif ch=="x":
            x_img = Image.open(SKIN_DIC + "score-x.png")
            base_img.paste(x_img, (x, y, x + x_img.size[0], y + x_img.size[1]), mask=x_img.split()[3])
            x += 32
        elif ch=="/":
            x+=16
            v_img = Image.open(SKIN_DIC + "score-virgule.png")
            base_img.paste(v_img, (x, y, x + v_img.size[0], y + v_img.size[1]), mask=v_img.split()[3])
            x+=32
        elif ch==".":
            d_img = Image.open(SKIN_DIC + "score-dot.png")
            base_img.paste(d_img, (x, y, x + d_img.size[0], y + d_img.size[1]), mask=d_img.split()[3])
            x += 32
        elif ch=="%":
            p_img = Image.open(SKIN_DIC + "score-percent.png")
            base_img.paste(p_img, (x, y, x + p_img.size[0], y + p_img.size[1]), mask=p_img.split()[3])
            x += 32

def download_bg(score):
    osu_url=BC_URL+score['bid']
    file=score['bid']+".jpg"
    with open(file, "wb") as code:
        code.write(requests.get(osu_url).content)
    return file

def change_diff(mods, bpm, CS, AR, HP):
    speed = 1
    od_ar_hp_multiplier = 1
    cs_multiplier = 1
    if mods & 1 << 4 > 0:  # HR
        od_ar_hp_multiplier *= 1.4
        cs_multiplier *= 1.3
    if mods & 1 << 1 > 0:  # EZ
        od_ar_hp_multiplier *= 0.5
        cs_multiplier *= 0.5
    if mods & 1 << 6 > 0:  # DT
        speed *= 1.5
    if mods & 1 << 8 > 0:  # HT
        speed *= 0.75
    # 计算bpm
    new_bpm = bpm * speed
    # 计算AR
    new_ar = AR * od_ar_hp_multiplier
    if new_ar <= 5:
        arms = 1800 - 120 * new_ar
    else:
        arms = 1200 - 150 * (new_ar - 5)
    arms = min(1800, max(450, arms)) / speed
    if arms > 1200:
        new_ar = (1800 - arms) / 120
    else:
        new_ar = (1200 - arms) / 150 + 5
    # 计算CS
    new_cs = max(0, min(10, CS * cs_multiplier))
    # 计算HP
    new_hp = min(10, HP * od_ar_hp_multiplier)
    return new_bpm, math.floor(new_cs * 100) / 100, math.floor(new_ar * 100) / 100, math.floor(new_hp * 100) / 100

if __name__ == '__main__':
    score=get_pp_info(get_user_best("wasupandceacar", 3), "wasupandceacar")
    pprint(score)
    generate_score_pic(score)