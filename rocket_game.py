import pygame
import sys
import math
import random
import json
import os

# ----------------------------------------------------
# 1. INISIALISASI & AUDIOSYNTH
# ----------------------------------------------------
pygame.init()
try:
    pygame.mixer.init(22050, -8, 1, 512)
    HAS_SOUND = True
except:
    HAS_SOUND = False

WIDTH, HEIGHT = 1100, 750
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🚀 SPACEX ORBIT MASTER - 10 LEVELS GOD MODE (WARFARE ED.)")
clock = pygame.time.Clock()

def generate_tone(freq_start, freq_end, duration, vol=0.3):
    if not HAS_SOUND: return None
    sample_rate = 22050
    n_samples = int(sample_rate * duration)
    buf = bytearray()
    for i in range(n_samples):
        t = i / sample_rate
        freq = freq_start + (freq_end - freq_start) * (i / n_samples)
        val = int(128 + 127 * vol * math.sin(2 * math.pi * freq * t))
        buf.append(max(0, min(255, val)))
    try:
        return pygame.mixer.Sound(buffer=bytes(buf))
    except:
        return None

# Sound Effects
snd_launch  = generate_tone(150, 480, 0.5, 0.4)
snd_rcs     = generate_tone(320, 290, 0.08, 0.2)
snd_win     = generate_tone(523, 1046, 0.6, 0.4)
snd_fail    = generate_tone(220, 70, 0.6, 0.5)
snd_pickup  = generate_tone(800, 1200, 0.2, 0.3)
snd_correct = generate_tone(400, 800, 0.3, 0.4)
snd_powerup = generate_tone(600, 1500, 0.4, 0.5)
snd_laser   = generate_tone(900, 300, 0.1, 0.3)
snd_exp     = generate_tone(160, 40, 0.3, 0.5)

# ----------------------------------------------------
# 2. SAVE / LOAD HIGH SCORE
# ----------------------------------------------------
SAVE_FILE = "space_high_scores.json"

def load_high_score():
    if os.path.exists(SAVE_FILE):
        try:
            with open(SAVE_FILE, "r") as f:
                return json.load(f).get("high_score", 0)
        except: return 0
    return 0

def save_high_score(new_score):
    old_high = load_high_score()
    if new_score > old_high:
        try:
            with open(SAVE_FILE, "w") as f:
                json.dump({"high_score": new_score}, f)
            return new_score
        except: pass
    return old_high

high_score = load_high_score()

# ----------------------------------------------------
# 3. WARNA & FONT
# ----------------------------------------------------
COLOR_BG       = (5, 8, 20)
WHITE          = (255, 255, 255)
EARTH_BLUE     = (28, 110, 220)
EARTH_GREEN    = (35, 160, 85)
EARTH_BROWN    = (130, 95, 45)
MOON_GRAY      = (180, 185, 195)
YELLOW         = (255, 220, 50)
RED            = (255, 65, 65)
CYAN           = (0, 240, 255)
ORANGE         = (255, 130, 0)
GREEN          = (40, 240, 110)
GRAY           = (120, 125, 140)
PURPLE         = (180, 70, 255)
SOLAR_BLUE     = (20, 90, 200)

font_title = pygame.font.SysFont("impact", 30)
font_sub   = pygame.font.SysFont("arial", 18, bold=True)
font_ui    = pygame.font.SysFont("arial", 14, bold=True)
font_huge  = pygame.font.SysFont("impact", 46)

# ----------------------------------------------------
# 4. DATA ROKET, KUIS, & ACHIEVEMENTS
# ----------------------------------------------------
ROCKET_SPECS = {
    "FALCON 9":    {"fuel": 100.0, "shield": 100.0, "rcs_mult": 1.0, "color": WHITE, "desc": "Sangat Seimbang & Andal"},
    "STARSHIP":    {"fuel": 150.0, "shield": 150.0, "rcs_mult": 0.8, "color": (200, 210, 225), "desc": "Tangki Jumbo & Armor Tebal"},
    "CREW DRAGON": {"fuel": 80.0,  "shield": 80.0,  "rcs_mult": 1.4, "color": CYAN, "desc": "Sangat Lincah & Responsif"}
}
selected_rocket = "FALCON 9"

QUIZ_LIST = [
    {"q": "Gaya apa yang menarik roket ke pusat planet?", "opt": ["A. Gravitasi", "B. Gesekan", "C. Magnet"], "ans": 0},
    {"q": "Siapa pendiri perusahaan antariksa SpaceX?", "opt": ["A. Jeff Bezos", "B. Elon Musk", "C. Bill Gates"], "ans": 1},
    {"q": "Apa nama Stasiun Luar Angkasa Internasional?", "opt": ["A. NASA", "B. ESA", "C. ISS"], "ans": 2},
    {"q": "Di mana letak ruang hampa udara berada?", "opt": ["A. Laut Dalam", "B. Luar Angkasa", "C. Inti Bumi"], "ans": 1}
]
current_quiz = random.choice(QUIZ_LIST)
quiz_bonus = False

achievements = {
    "quiz_master": False,
    "no_damage": True,
    "blackhole_survivor": False
}

# ----------------------------------------------------
# 5. ENVIRONMENT & 10 LEVELS DATA
# ----------------------------------------------------
stars = [{"x": random.randint(0, WIDTH), "y": random.randint(0, HEIGHT), "size": random.choice([1,1,2,2,3]), "color": random.choice([WHITE, CYAN, (255,240,200)]), "twinkle": random.uniform(0, 6.28)} for _ in range(220)]

EARTH_POS = (WIDTH // 2, HEIGHT // 2)
EARTH_RADIUS = 75
GM_EARTH = 360000.0
GM_MOON = 35000.0

LEVELS = {
    1:  {"name": "LEO Docking Basics",       "dist": 170, "speed": 0.002, "debris": 2, "has_moon": False, "has_blackhole": False, "has_boss": False},
    2:  {"name": "Orbit Alignment",          "dist": 190, "speed": 0.003, "debris": 3, "has_moon": False, "has_blackhole": False, "has_boss": False},
    3:  {"name": "Asteroid Field Raid",      "dist": 210, "speed": 0.004, "debris": 5, "has_moon": False, "has_blackhole": False, "has_boss": False},
    4:  {"name": "Medium Orbit Navigation",  "dist": 240, "speed": 0.004, "debris": 6, "has_moon": False, "has_blackhole": False, "has_boss": False},
    5:  {"name": "High Orbit Challenge",     "dist": 270, "speed": 0.005, "debris": 8, "has_moon": False, "has_blackhole": False, "has_boss": False},
    6:  {"name": "Lunar Gravity Slingshot",  "dist": 300, "speed": 0.004, "debris": 6, "has_moon": True,  "has_blackhole": False, "has_boss": False},
    7:  {"name": "Lunar Debris Field",       "dist": 320, "speed": 0.006, "debris": 8, "has_moon": True,  "has_blackhole": False, "has_boss": False},
    8:  {"name": "Black Hole Anomaly",       "dist": 340, "speed": 0.006, "debris": 7, "has_moon": False, "has_blackhole": True,  "has_boss": False},
    9:  {"name": "Event Horizon Crossing",   "dist": 360, "speed": 0.008, "debris": 9, "has_moon": False, "has_blackhole": True,  "has_boss": False},
    10: {"name": "GOD MODE: ALIEN DREADNOUGHT", "dist": 380, "speed": 0.009, "debris": 6, "has_moon": True, "has_blackhole": True, "has_boss": True}
}

level = 1
max_level = 10
game_state = "MENU" # MENU, HANGAR, QUIZ, AIMING, FLYING, CLEAR, GAME_OVER, FINAL_VICTORY

total_score = 0
fuel = 100.0
shield = 100.0
mission_time = 0.0
screen_shake = 0
slowmo_timer = 0.0
weapon_type = "SINGLE"
triple_timer = 0.0

launch_angle = -90.0
launch_power = 40.0

rocket_pos = [0.0, 0.0]
rocket_vel = [0.0, 0.0]
trail = []
particles = []
bullets = []
enemy_bullets = []

station_angle = 0.0
station_dist = 170.0
moon_angle = 0.0
moon_dist = 310.0
blackhole_pos = (230, 170)

boss = {"hp": 300, "max_hp": 300, "angle": 0.0, "dist": 330.0, "shoot_timer": 0.0}
debris_list = []
collectible_list = []
powerup_list = []

def load_level(lvl):
    global station_dist, station_angle, debris_list, collectible_list, powerup_list, launch_power, launch_angle, fuel, shield, mission_time, moon_angle, quiz_bonus, weapon_type, bullets, enemy_bullets, boss
    data = LEVELS[lvl]
    station_dist = data["dist"]
    station_angle = random.uniform(0, math.pi * 2)
    moon_angle = random.uniform(0, math.pi * 2)
    launch_angle = -90.0
    launch_power = 38.0 + (lvl * 1.8)
    
    spec = ROCKET_SPECS[selected_rocket]
    fuel = spec["fuel"] * (1.20 if quiz_bonus else 1.0)
    shield = spec["shield"]
    mission_time = 0.0
    weapon_type = "SINGLE"
    
    trail.clear(); bullets.clear(); enemy_bullets.clear()

    # Generate Debris
    debris_list.clear()
    for _ in range(data["debris"]):
        debris_list.append({
            "angle": random.uniform(0, math.pi * 2),
            "dist": random.uniform(120, station_dist + 20),
            "speed": random.uniform(0.003, 0.009) * random.choice([-1, 1]),
            "size": random.randint(8, 14),
            "hp": 2
        })

    # Science Data
    collectible_list.clear()
    for _ in range(2):
        collectible_list.append({
            "angle": random.uniform(0, math.pi * 2),
            "dist": random.uniform(130, station_dist),
            "collected": False
        })

    # Power-Ups
    powerup_list.clear()
    types = ["FUEL", "SHIELD", "SLOWMO", "TRIPLE"]
    for t in types:
        powerup_list.append({
            "type": t,
            "angle": random.uniform(0, math.pi * 2),
            "dist": random.uniform(140, station_dist + 10),
            "collected": False
        })

    if data["has_boss"]:
        boss["hp"] = 300; boss["max_hp"] = 300; boss["angle"] = station_angle + math.pi / 2; boss["shoot_timer"] = 0

def fire_laser():
    global fuel
    if fuel < 1.5: return
    fuel -= 1.0
    if snd_laser: snd_laser.play()

    spd = math.hypot(rocket_vel[0], rocket_vel[1])
    if spd < 1: vx, vy = 0, -15
    else: vx, vy = (rocket_vel[0] / spd) * 16, (rocket_vel[1] / spd) * 16

    bullets.append({"x": rocket_pos[0], "y": rocket_pos[1], "vx": vx, "vy": vy, "life": 45})

    if weapon_type == "TRIPLE":
        ang = math.atan2(vy, vx)
        bullets.append({"x": rocket_pos[0], "y": rocket_pos[1], "vx": math.cos(ang+0.25)*16, "vy": math.sin(ang+0.25)*16, "life": 45})
        bullets.append({"x": rocket_pos[0], "y": rocket_pos[1], "vx": math.cos(ang-0.25)*16, "vy": math.sin(ang-0.25)*16, "life": 45})

# ----------------------------------------------------
# 6. DRAWING HELPERS
# ----------------------------------------------------
def add_explosion(x, y, color, count=20):
    for _ in range(count):
        ang = random.uniform(0, math.pi * 2)
        spd = random.uniform(1, 5)
        particles.append({"x": x, "y": y, "vx": math.cos(ang)*spd, "vy": math.sin(ang)*spd, "life": 25, "color": color})

def update_particles(surface):
    for p in particles[:]:
        p["x"] += p["vx"]; p["y"] += p["vy"]; p["life"] -= 1
        if p["life"] <= 0: particles.remove(p)
        else: pygame.draw.circle(surface, p["color"], (int(p["x"]), int(p["y"])), max(1, p["life"]//6))

def draw_earth(surface, rot_cloud):
    cx, cy = EARTH_POS
    for r, alpha in [(EARTH_RADIUS + 16, 25), (EARTH_RADIUS + 10, 50), (EARTH_RADIUS + 4, 90)]:
        s = pygame.Surface((r*2, r*2), pygame.SRCALPHA)
        pygame.draw.circle(s, (100, 180, 255, alpha), (r, r), r)
        surface.blit(s, (cx - r, cy - r))

    pygame.draw.circle(surface, EARTH_BLUE, EARTH_POS, EARTH_RADIUS)

    surf_e = pygame.Surface((EARTH_RADIUS*2, EARTH_RADIUS*2), pygame.SRCALPHA)
    pygame.draw.circle(surf_e, (255, 255, 255, 255), (EARTH_RADIUS, EARTH_RADIUS), EARTH_RADIUS)

    cont = pygame.Surface((EARTH_RADIUS*2, EARTH_RADIUS*2), pygame.SRCALPHA)
    pygame.draw.ellipse(cont, EARTH_GREEN, (25, 20, 65, 45))
    pygame.draw.ellipse(cont, EARTH_BROWN, (40, 30, 35, 25))
    pygame.draw.ellipse(cont, EARTH_GREEN, (70, 75, 55, 50))
    
    clouds = pygame.Surface((EARTH_RADIUS*2, EARTH_RADIUS*2), pygame.SRCALPHA)
    pygame.draw.arc(clouds, (255, 255, 255, 180), (10, 10, 130, 130), rot_cloud, rot_cloud + 1.4, 8)

    cont.blit(surf_e, (0,0), special_flags=pygame.BLEND_RGBA_MIN)
    clouds.blit(surf_e, (0,0), special_flags=pygame.BLEND_RGBA_MIN)

    surface.blit(cont, (cx - EARTH_RADIUS, cy - EARTH_RADIUS))
    surface.blit(clouds, (cx - EARTH_RADIUS, cy - EARTH_RADIUS))

def draw_moon(surface, mx, my):
    pygame.draw.circle(surface, MOON_GRAY, (int(mx), int(my)), 22)
    pygame.draw.circle(surface, (140, 145, 155), (int(mx - 5), int(my - 4)), 5)
    pygame.draw.circle(surface, (140, 145, 155), (int(mx + 6), int(my + 5)), 4)

def draw_blackhole(surface, bx, by, timer):
    for r, col in [(45, PURPLE), (30, ORANGE), (18, WHITE)]:
        s = pygame.Surface((r*2, r*2), pygame.SRCALPHA)
        pygame.draw.circle(s, (*col, 120), (r, r), int(r + math.sin(timer*5)*3))
        surface.blit(s, (bx - r, by - r))
    pygame.draw.circle(surface, (0, 0, 0), (bx, by), 12)
    txt = font_ui.render("⚠️ BLACK HOLE", True, PURPLE)
    surface.blit(txt, (bx - txt.get_width()//2, by - 30))

def draw_boss(surface, bx, by, boss_data):
    pts = [(bx, by - 28), (bx + 32, by + 16), (bx + 15, by + 25), (bx, by + 16), (bx - 15, by + 25), (bx - 32, by + 16)]
    pygame.draw.polygon(surface, PURPLE, pts)
    pygame.draw.polygon(surface, RED, pts, 2)
    pygame.draw.circle(surface, YELLOW, (int(bx), int(by)), 7)

    bw, bh = 100, 7
    pygame.draw.rect(surface, GRAY, (bx - bw//2, by - 38, bw, bh))
    pygame.draw.rect(surface, RED, (bx - bw//2, by - 38, int(bw * max(0, boss_data["hp"]) / boss_data["max_hp"]), bh))
    pygame.draw.rect(surface, WHITE, (bx - bw//2, by - 38, bw, bh), 1)

def draw_space_station(surface, x, y, pulse_t):
    spos = (int(x), int(y))
    pygame.draw.rect(surface, GRAY, (x - 36, y - 4, 72, 8))
    pygame.draw.rect(surface, SOLAR_BLUE, (x - 42, y - 11, 26, 22))
    pygame.draw.rect(surface, SOLAR_BLUE, (x + 16, y - 11, 26, 22))
    for i in range(1, 4):
        pygame.draw.line(surface, CYAN, (x - 42 + i*6, y - 11), (x - 42 + i*6, y + 10), 1)
        pygame.draw.line(surface, CYAN, (x + 16 + i*6, y - 11), (x + 16 + i*6, y + 10), 1)
    
    pygame.draw.circle(surface, WHITE, spos, 10)
    pygame.draw.circle(surface, GRAY, spos, 6)

    target_r = int(36 + math.sin(pulse_t * 6) * 4)
    pygame.draw.circle(surface, GREEN, spos, target_r, 3)
    
    txt = font_ui.render("🎯 TARGET DOCKING", True, GREEN)
    surface.blit(txt, (x - txt.get_width()//2, y - 35))

def draw_docking_cam(surface, st_x, st_y, rx, ry):
    pip_w, pip_h = 170, 170
    pip_x, pip_y = WIDTH - pip_w - 20, HEIGHT - pip_h - 20
    pip_surf = pygame.Surface((pip_w, pip_h))
    pip_surf.fill((10, 15, 28))

    scale = 1.8
    center_x, center_y = pip_w // 2, pip_h // 2

    pygame.draw.circle(pip_surf, GREEN, (center_x, center_y), int(35 * scale), 2)
    pygame.draw.circle(pip_surf, WHITE, (center_x, center_y), int(8 * scale))

    rel_x = center_x + int((rx - st_x) * scale)
    rel_y = center_y + int((ry - st_y) * scale)
    pygame.draw.circle(pip_surf, RED, (rel_x, rel_y), 5)
    pygame.draw.line(pip_surf, YELLOW, (center_x, center_y), (rel_x, rel_y), 1)

    surface.blit(pip_surf, (pip_x, pip_y))
    pygame.draw.rect(surface, GREEN, (pip_x, pip_y, pip_w, pip_h), 2)
    txt = font_ui.render("📹 DOCKING CAM", True, GREEN)
    surface.blit(txt, (pip_x + 10, pip_y + 10))

# ----------------------------------------------------
# 7. MAIN GAME LOOP
# ----------------------------------------------------
running = True
pulse_timer = 0.0
cloud_rot = 0.0

while running:
    dt = clock.tick(60) / 1000.0
    pulse_timer += dt
    cloud_rot += dt * 0.1
    if slowmo_timer > 0: slowmo_timer -= dt
    if triple_timer > 0:
        triple_timer -= dt
        if triple_timer <= 0: weapon_type = "SINGLE"

    if game_state == "FLYING": mission_time += dt

    # Handling Screen Shake
    render_offset = [0, 0]
    if screen_shake > 0:
        screen_shake -= 1
        render_offset = [random.randint(-4, 4), random.randint(-4, 4)]

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if game_state == "MENU":
                if event.key == pygame.K_SPACE: game_state = "HANGAR"

            elif game_state == "HANGAR":
                r_keys = list(ROCKET_SPECS.keys())
                idx = r_keys.index(selected_rocket)
                if event.key == pygame.K_RIGHT: selected_rocket = r_keys[(idx + 1) % len(r_keys)]
                elif event.key == pygame.K_LEFT: selected_rocket = r_keys[(idx - 1) % len(r_keys)]
                elif event.key == pygame.K_SPACE:
                    current_quiz = random.choice(QUIZ_LIST)
                    game_state = "QUIZ"

            elif game_state == "QUIZ":
                if event.key in [pygame.K_1, pygame.K_a]: ans = 0
                elif event.key in [pygame.K_2, pygame.K_b]: ans = 1
                elif event.key in [pygame.K_3, pygame.K_c]: ans = 2
                else: ans = -1

                if ans != -1:
                    if ans == current_quiz["ans"]:
                        quiz_bonus = True
                        achievements["quiz_master"] = True
                        if snd_correct: snd_correct.play()
                    else:
                        quiz_bonus = False
                        if snd_fail: snd_fail.play()
                    level = 1
                    total_score = 0
                    load_level(1)
                    game_state = "AIMING"

            elif game_state == "AIMING":
                if event.key == pygame.K_SPACE:
                    game_state = "FLYING"
                    if snd_launch: snd_launch.play()
                    rad = math.radians(launch_angle)
                    start_r = EARTH_RADIUS + 10
                    rocket_pos = [EARTH_POS[0] + math.cos(rad) * start_r, EARTH_POS[1] + math.sin(rad) * start_r]
                    rocket_vel = [math.cos(rad) * launch_power, math.sin(rad) * launch_power]

            elif game_state == "FLYING":
                if event.key in [pygame.K_f, pygame.K_SPACE]:
                    fire_laser()

            elif game_state == "CLEAR":
                if event.key == pygame.K_SPACE:
                    if level < max_level:
                        level += 1
                        load_level(level)
                        game_state = "AIMING"
                    else:
                        high_score = save_high_score(total_score)
                        game_state = "FINAL_VICTORY"

            elif game_state in ["GAME_OVER", "FINAL_VICTORY"]:
                if event.key == pygame.K_r: game_state = "MENU"

    keys = pygame.key.get_pressed()
    if game_state == "AIMING":
        if keys[pygame.K_LEFT]:  launch_angle -= 1.3
        if keys[pygame.K_RIGHT]: launch_angle += 1.3
        if keys[pygame.K_UP]:    launch_power = min(75.0, launch_power + 0.4)
        if keys[pygame.K_DOWN]:  launch_power = max(18.0, launch_power - 0.4)

    # Kontrol RCS Thruster & Nitro
    is_thruster_active = False
    spec = ROCKET_SPECS[selected_rocket]
    if game_state == "FLYING" and fuel > 0:
        rcs_f = 32.0 * spec["rcs_mult"]
        if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
            rcs_f = 75.0 * spec["rcs_mult"]
            fuel -= 12 * dt; is_thruster_active = True

        if keys[pygame.K_w] or keys[pygame.K_UP]:    rocket_vel[1] -= rcs_f * dt; fuel -= 4 * dt; is_thruster_active = True
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:  rocket_vel[1] += rcs_f * dt; fuel -= 4 * dt; is_thruster_active = True
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:  rocket_vel[0] -= rcs_f * dt; fuel -= 4 * dt; is_thruster_active = True
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]: rocket_vel[0] += rcs_f * dt; fuel -= 4 * dt; is_thruster_active = True
        
        if is_thruster_active and int(pulse_timer*25)%5 == 0:
            if snd_rcs: snd_rcs.play()

    # Logika Fisika Game
    lvl_data = LEVELS[level]
    speed_mult = 0.3 if slowmo_timer > 0 else 1.0
    station_angle += lvl_data["speed"] * speed_mult
    st_x = EARTH_POS[0] + math.cos(station_angle) * station_dist
    st_y = EARTH_POS[1] + math.sin(station_angle) * station_dist

    if lvl_data["has_moon"]:
        moon_angle += 0.002 * speed_mult
        m_x = EARTH_POS[0] + math.cos(moon_angle) * moon_dist
        m_y = EARTH_POS[1] + math.sin(moon_angle) * moon_dist

    if lvl_data["has_boss"] and boss["hp"] > 0:
        boss["angle"] += 0.005 * speed_mult
        bx = EARTH_POS[0] + math.cos(boss["angle"]) * boss["dist"]
        by = EARTH_POS[1] + math.sin(boss["angle"]) * boss["dist"]

        if game_state == "FLYING":
            boss["shoot_timer"] += dt
            if boss["shoot_timer"] > 1.2:
                boss["shoot_timer"] = 0
                ang = math.atan2(rocket_pos[1] - by, rocket_pos[0] - bx)
                enemy_bullets.append({"x": bx, "y": by, "vx": math.cos(ang)*8.0, "vy": math.sin(ang)*8.0})

    for deb in debris_list: deb["angle"] += deb["speed"] * speed_mult

    if game_state == "FLYING":
        # Peluru Player
        for b in bullets[:]:
            b["x"] += b["vx"]; b["y"] += b["vy"]; b["life"] -= 1
            if b["life"] <= 0: bullets.remove(b)

        # Peluru Musuh
        for eb in enemy_bullets[:]:
            eb["x"] += eb["vx"]; eb["y"] += eb["vy"]
            if math.hypot(eb["x"] - rocket_pos[0], eb["y"] - rocket_pos[1]) < 12:
                shield -= 20; screen_shake = 8
                add_explosion(rocket_pos[0], rocket_pos[1], RED, 12)
                enemy_bullets.remove(eb)

        # Gravitasi Bumi
        dx = EARTH_POS[0] - rocket_pos[0]
        dy = EARTH_POS[1] - rocket_pos[1]
        r = math.sqrt(dx*dx + dy*dy)

        if r <= EARTH_RADIUS or r > 950:
            add_explosion(rocket_pos[0], rocket_pos[1], RED, 30)
            high_score = save_high_score(total_score)
            game_state = "GAME_OVER"
            if snd_fail: snd_fail.play()

        else:
            acc_e = GM_EARTH / (r * r)
            rocket_vel[0] += acc_e * (dx / r) * dt
            rocket_vel[1] += acc_e * (dy / r) * dt

            # Gravitasi Bulan
            if lvl_data["has_moon"]:
                mdx, mdy = m_x - rocket_pos[0], m_y - rocket_pos[1]
                mr = math.sqrt(mdx*mdx + mdy*mdy)
                if mr < 22:
                    add_explosion(rocket_pos[0], rocket_pos[1], GRAY, 20)
                    game_state = "GAME_OVER"
                elif mr < 160:
                    acc_m = GM_MOON / (mr * mr)
                    rocket_vel[0] += acc_m * (mdx / mr) * dt
                    rocket_vel[1] += acc_m * (mdy / mr) * dt

            # Gravitasi Black Hole
            if lvl_data["has_blackhole"]:
                blx, bly = blackhole_pos
                bdx, bdy = blx - rocket_pos[0], bly - rocket_pos[1]
                br = math.sqrt(bdx*bdx + bdy*bdy)
                if br < 18:
                    add_explosion(rocket_pos[0], rocket_pos[1], PURPLE, 40)
                    game_state = "GAME_OVER"
                    if snd_fail: snd_fail.play()
                elif br < 200:
                    acc_b = 170000.0 / (br * br)
                    rocket_vel[0] += acc_b * (bdx / br) * dt
                    rocket_vel[1] += acc_b * (bdy / br) * dt
                    achievements["blackhole_survivor"] = True

            # Magnet Tractor Beam Stasiun
            dist_st = math.hypot(rocket_pos[0] - st_x, rocket_pos[1] - st_y)
            if dist_st < 75:
                rocket_vel[0] += (st_x - rocket_pos[0]) * 2.0 * dt
                rocket_vel[1] += (st_y - rocket_pos[1]) * 2.0 * dt

            rocket_pos[0] += rocket_vel[0] * dt
            rocket_pos[1] += rocket_vel[1] * dt

            trail.append((int(rocket_pos[0]), int(rocket_pos[1])))
            if len(trail) > (80 if not is_thruster_active else 130): trail.pop(0)

            # Hit Asteroid dari Laser Player
            for b in bullets[:]:
                for deb in debris_list[:]:
                    db_x = EARTH_POS[0] + math.cos(deb["angle"]) * deb["dist"]
                    db_y = EARTH_POS[1] + math.sin(deb["angle"]) * deb["dist"]
                    if math.hypot(b["x"] - db_x, b["y"] - db_y) < deb["size"] + 5:
                        deb["hp"] -= 1; bullets.remove(b)
                        add_explosion(db_x, db_y, ORANGE, 8)
                        if deb["hp"] <= 0:
                            debris_list.remove(deb); total_score += 150
                            if snd_exp: snd_exp.play()
                        break

            # Hit Boss dari Laser Player
            if lvl_data["has_boss"] and boss["hp"] > 0:
                for b in bullets[:]:
                    if math.hypot(b["x"] - bx, b["y"] - by) < 30:
                        boss["hp"] -= 10; total_score += 50; bullets.remove(b)
                        add_explosion(bx, by, YELLOW, 6)
                        if boss["hp"] <= 0:
                            add_explosion(bx, by, PURPLE, 60); total_score += 3000

            # Tabrakan Debris
            for deb in debris_list:
                db_x = EARTH_POS[0] + math.cos(deb["angle"]) * deb["dist"]
                db_y = EARTH_POS[1] + math.sin(deb["angle"]) * deb["dist"]
                if math.hypot(rocket_pos[0] - db_x, rocket_pos[1] - db_y) < (deb["size"] + 6):
                    shield -= 25; screen_shake = 8
                    achievements["no_damage"] = False
                    add_explosion(rocket_pos[0], rocket_pos[1], ORANGE, 12)
                    if shield <= 0:
                        high_score = save_high_score(total_score)
                        game_state = "GAME_OVER"
                        if snd_fail: snd_fail.play()

            # Collectible
            for col in collectible_list:
                if not col["collected"]:
                    cx = EARTH_POS[0] + math.cos(col["angle"]) * col["dist"]
                    cy = EARTH_POS[1] + math.sin(col["angle"]) * col["dist"]
                    if math.hypot(rocket_pos[0] - cx, rocket_pos[1] - cy) < 20:
                        col["collected"] = True; total_score += 400
                        add_explosion(cx, cy, CYAN, 15)
                        if snd_pickup: snd_pickup.play()

            # Power-Ups
            for pw in powerup_list:
                if not pw["collected"]:
                    px = EARTH_POS[0] + math.cos(pw["angle"]) * pw["dist"]
                    py = EARTH_POS[1] + math.sin(pw["angle"]) * pw["dist"]
                    if math.hypot(rocket_pos[0] - px, rocket_pos[1] - py) < 20:
                        pw["collected"] = True
                        if pw["type"] == "FUEL": fuel = min(150.0, fuel + 40)
                        elif pw["type"] == "SHIELD": shield = min(150.0, shield + 40)
                        elif pw["type"] == "SLOWMO": slowmo_timer = 5.0
                        elif pw["type"] == "TRIPLE": weapon_type = "TRIPLE"; triple_timer = 8.0
                        add_explosion(px, py, GREEN, 20)
                        if snd_powerup: snd_powerup.play()

            # Docking Berhasil (Jika Boss mati / tidak ada)
            if dist_st < 38:
                if not (lvl_data["has_boss"] and boss["hp"] > 0):
                    total_score += int(800 + (fuel * 12) + (shield * 4) - (mission_time * 8))
                    game_state = "CLEAR"
                    if snd_win: snd_win.play()

    # ----------------------------------------------------
    # RENDERING UTAMA
    # ----------------------------------------------------
    canvas = pygame.Surface((WIDTH, HEIGHT))
    canvas.fill(COLOR_BG)

    for s in stars: pygame.draw.circle(canvas, s["color"], (s["x"], s["y"]), s["size"])

    draw_earth(canvas, cloud_rot)
    pygame.draw.circle(canvas, (30, 45, 70), EARTH_POS, int(station_dist), 1)

    if lvl_data["has_moon"]:
        draw_moon(canvas, m_x, m_y)

    if lvl_data["has_blackhole"]:
        draw_blackhole(canvas, blackhole_pos[0], blackhole_pos[1], pulse_timer)

    if lvl_data["has_boss"] and boss["hp"] > 0:
        draw_boss(canvas, bx, by, boss)

    # Debris
    for deb in debris_list:
        db_x = int(EARTH_POS[0] + math.cos(deb["angle"]) * deb["dist"])
        db_y = int(EARTH_POS[1] + math.sin(deb["angle"]) * deb["dist"])
        pygame.draw.rect(canvas, RED if deb["hp"] > 1 else ORANGE, (db_x - deb["size"]//2, db_y - deb["size"]//2, deb["size"], deb["size"]))

    # Science Data
    for col in collectible_list:
        if not col["collected"]:
            cx = int(EARTH_POS[0] + math.cos(col["angle"]) * col["dist"])
            cy = int(EARTH_POS[1] + math.sin(col["angle"]) * col["dist"])
            pygame.draw.circle(canvas, CYAN, (cx, cy), 8, 2)
            pygame.draw.circle(canvas, YELLOW, (cx, cy), 4)

    # Power-Ups
    for pw in powerup_list:
        if not pw["collected"]:
            px = int(EARTH_POS[0] + math.cos(pw["angle"]) * pw["dist"])
            py = int(EARTH_POS[1] + math.sin(pw["angle"]) * pw["dist"])
            col = GREEN if pw["type"] == "FUEL" else (CYAN if pw["type"] == "SHIELD" else PURPLE)
            pygame.draw.circle(canvas, col, (px, py), 10)
            txt = font_ui.render(pw["type"][0], True, WHITE)
            canvas.blit(txt, (px - 4, py - 7))

    draw_space_station(canvas, st_x, st_y, pulse_timer)

    if game_state == "AIMING":
        rad = math.radians(launch_angle)
        sx = EARTH_POS[0] + math.cos(rad) * (EARTH_RADIUS + 10)
        sy = EARTH_POS[1] + math.sin(rad) * (EARTH_RADIUS + 10)
        svx = math.cos(rad) * launch_power
        svy = math.sin(rad) * launch_power
        pygame.draw.line(canvas, ORANGE, (sx, sy), (sx + svx*0.6, sy + svy*0.6), 4)

        for _ in range(55):
            dx = EARTH_POS[0] - sx; dy = EARTH_POS[1] - sy
            r = math.sqrt(dx*dx + dy*dy)
            if r <= EARTH_RADIUS: break
            acc = GM_EARTH / (r * r)
            svx += acc * (dx / r) * 0.03; svy += acc * (dy / r) * 0.03
            sx += svx * 0.03; sy += svy * 0.03
            pygame.draw.circle(canvas, WHITE, (int(sx), int(sy)), 2)

    if len(trail) > 1: pygame.draw.lines(canvas, YELLOW if not is_thruster_active else ORANGE, False, trail, 2)

    # Bullets
    for b in bullets: pygame.draw.circle(canvas, CYAN, (int(b["x"]), int(b["y"])), 4)
    for eb in enemy_bullets: pygame.draw.circle(canvas, RED, (int(eb["x"]), int(eb["y"])), 5)

    if game_state == "FLYING":
        ang = math.atan2(rocket_vel[1], rocket_vel[0])
        p1 = (rocket_pos[0] + math.cos(ang)*16, rocket_pos[1] + math.sin(ang)*16)
        p2 = (rocket_pos[0] + math.cos(ang+2.5)*8, rocket_pos[1] + math.sin(ang+2.5)*8)
        p3 = (rocket_pos[0] + math.cos(ang-2.5)*8, rocket_pos[1] + math.sin(ang-2.5)*8)
        pygame.draw.polygon(canvas, spec["color"], [p1, p2, p3])

        if dist_st < 130:
            draw_docking_cam(canvas, st_x, st_y, rocket_pos[0], rocket_pos[1])

    update_particles(canvas)

    # Telemetri HUD
    pygame.draw.rect(canvas, (15, 20, 38), (10, 10, 460, 140))
    pygame.draw.rect(canvas, CYAN, (10, 10, 460, 140), 2)

    canvas.blit(font_title.render(f"MISI {level}/{max_level}: {lvl_data['name']}", True, YELLOW), (20, 15))
    canvas.blit(font_ui.render(f"SKOR: {total_score} | HIGH: {high_score}", True, GREEN), (300, 20))

    pygame.draw.rect(canvas, GRAY, (20, 50, 150, 10))
    pygame.draw.rect(canvas, GREEN if fuel > 30 else RED, (20, 50, int(min(150, fuel)), 10))
    canvas.blit(font_ui.render(f"FUEL: {int(fuel)}%", True, WHITE), (180, 48))

    pygame.draw.rect(canvas, GRAY, (20, 68, 150, 10))
    pygame.draw.rect(canvas, CYAN if shield > 30 else RED, (20, 68, int(min(150, shield)), 10))
    canvas.blit(font_ui.render(f"SHIELD: {int(shield)}%", True, WHITE), (180, 66))

    canvas.blit(font_ui.render(f"SENJATA: {weapon_type} ([F]/[SPASI]) | NITRO: [SHIFT]", True, PURPLE if weapon_type == "TRIPLE" else WHITE), (20, 90))
    if slowmo_timer > 0: canvas.blit(font_ui.render(f"⏱️ SLOW-MO: {round(slowmo_timer,1)}s", True, PURPLE), (20, 110))

    # OVERLAY MENUS
    if game_state == "MENU":
        pygame.draw.rect(canvas, (0, 0, 0), (0, 0, WIDTH, HEIGHT))
        t1 = font_huge.render("SPACEX ORBIT MASTER (WARFARE)", True, YELLOW)
        t2 = font_sub.render(f"REKOR SKOR SAAT INI: {high_score} PTS", True, CYAN)
        t3 = font_sub.render("Tekan [SPASI] Untuk Masuk Hangar Roket", True, GREEN)
        canvas.blit(t1, (WIDTH//2 - t1.get_width()//2, 240))
        canvas.blit(t2, (WIDTH//2 - t2.get_width()//2, 320))
        canvas.blit(t3, (WIDTH//2 - t3.get_width()//2, 400))

    elif game_state == "HANGAR":
        pygame.draw.rect(canvas, (10, 15, 30), (100, 100, 900, 550))
        pygame.draw.rect(canvas, CYAN, (100, 100, 900, 550), 3)
        t1 = font_title.render("🛸 HANGAR PEMILIHAN ROKET SPACEX", True, YELLOW)
        canvas.blit(t1, (WIDTH//2 - t1.get_width()//2, 130))

        sp = ROCKET_SPECS[selected_rocket]
        t_name = font_huge.render(f"<  {selected_rocket}  >", True, GREEN)
        canvas.blit(t_name, (WIDTH//2 - t_name.get_width()//2, 220))

        t_desc = font_sub.render(f"Spesifikasi: {sp['desc']}", True, WHITE)
        t_f = font_sub.render(f"Kapasitas Tangki: {sp['fuel']}%", True, CYAN)
        t_s = font_sub.render(f"Ketahanan Shield: {sp['shield']}%", True, YELLOW)
        t_m = font_sub.render(f"Kelincahan Pendorong RCS: {int(sp['rcs_mult']*100)}%", True, ORANGE)

        canvas.blit(t_desc, (WIDTH//2 - t_desc.get_width()//2, 310))
        canvas.blit(t_f, (WIDTH//2 - t_f.get_width()//2, 360))
        canvas.blit(t_s, (WIDTH//2 - t_s.get_width()//2, 400))
        canvas.blit(t_m, (WIDTH//2 - t_m.get_width()//2, 440))

        t_hint = font_sub.render("Gunakan [← / →] Pilih Roket | Tekan [SPASI] Lanjut Kuis", True, GREEN)
        canvas.blit(t_hint, (WIDTH//2 - t_hint.get_width()//2, 550))

    elif game_state == "QUIZ":
        pygame.draw.rect(canvas, (15, 25, 45), (150, 150, 800, 450))
        pygame.draw.rect(canvas, YELLOW, (150, 150, 800, 450), 3)
        t1 = font_title.render("🧠 KUIS ANTARIKSA (BONUS FUEL +20%)", True, YELLOW)
        canvas.blit(t1, (WIDTH//2 - t1.get_width()//2, 180))

        q_txt = font_sub.render(current_quiz["q"], True, WHITE)
        canvas.blit(q_txt, (WIDTH//2 - q_txt.get_width()//2, 260))

        for i, opt in enumerate(current_quiz["opt"]):
            ot = font_sub.render(f"Tekan [{i+1}] atau [{chr(97+i).upper()}] : {opt}", True, CYAN)
            canvas.blit(ot, (WIDTH//2 - 150, 340 + i*45))

    elif game_state == "CLEAR":
        pygame.draw.rect(canvas, (0, 40, 20), (150, 200, 800, 280))
        pygame.draw.rect(canvas, GREEN, (150, 200, 800, 280), 3)
        t1 = font_title.render(f"🎉 LEVEL {level} SELESAI - DOCKING BERHASIL!", True, GREEN)
        t2 = font_sub.render("TEKAN [SPASI] UNTUK MISI NEXT LEVEL 🚀", True, YELLOW)
        canvas.blit(t1, (WIDTH//2 - t1.get_width()//2, 260))
        canvas.blit(t2, (WIDTH//2 - t2.get_width()//2, 360))

    elif game_state == "GAME_OVER":
        pygame.draw.rect(canvas, (50, 10, 10), (150, 200, 800, 280))
        pygame.draw.rect(canvas, RED, (150, 200, 800, 280), 3)
        t1 = font_title.render("💥 MISI GAGAL!", True, RED)
        t2 = font_sub.render("TEKAN [R] UNTUK MENCOBA LAGI", True, YELLOW)
        canvas.blit(t1, (WIDTH//2 - t1.get_width()//2, 260))
        canvas.blit(t2, (WIDTH//2 - t2.get_width()//2, 360))

    elif game_state == "FINAL_VICTORY":
        pygame.draw.rect(canvas, (10, 30, 60), (100, 100, 900, 520))
        pygame.draw.rect(canvas, YELLOW, (100, 100, 900, 520), 4)
        t1 = font_huge.render("🏆 SELAMAT! ALL 10 LEVELS CLEARED!", True, YELLOW)
        t2 = font_title.render(f"SKOR AKHIR: {total_score} PTS | HIGH SCORE SAVED!", True, GREEN)
        
        canvas.blit(t1, (WIDTH//2 - t1.get_width()//2, 140))
        canvas.blit(t2, (WIDTH//2 - t2.get_width()//2, 220))

        y_m = 300
        canvas.blit(font_sub.render("🏅 MEDALI PENCAPAIAN:", True, CYAN), (150, y_m))
        
        m1 = "✅ Quiz Master (+20% Fuel)" if achievements["quiz_master"] else "❌ Quiz Master"
        m2 = "✅ Perfect Hull (Tanpa Tabrakan)" if achievements["no_damage"] else "❌ Perfect Hull"
        m3 = "✅ Black Hole Survivor" if achievements["blackhole_survivor"] else "❌ Black Hole Survivor"

        canvas.blit(font_ui.render(m1, True, GREEN if achievements["quiz_master"] else GRAY), (150, y_m + 35))
        canvas.blit(font_ui.render(m2, True, GREEN if achievements["no_damage"] else GRAY), (150, y_m + 65))
        canvas.blit(font_ui.render(m3, True, GREEN if achievements["blackhole_survivor"] else GRAY), (150, y_m + 95))

        t3 = font_sub.render("Tekan [R] Untuk Mengulang dari Level 1", True, WHITE)
        canvas.blit(t3, (WIDTH//2 - t3.get_width()//2, 550))

    screen.blit(canvas, render_offset)
    pygame.display.flip()

pygame.quit()
sys.exit()