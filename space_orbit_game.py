import pygame
import math
import random
import sys
import array

# 1. Inisialisasi Pygame & Sound Engine
pygame.init()
pygame.font.init()

try:
    pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
except Exception:
    pass

WIDTH, HEIGHT = 850, 650
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Orbit: GOD TIER GACOR EDITION (FIXED LEVEL)")
clock = pygame.time.Clock()

# --- Generator Suara Synthetic SFX & BGM ---
def generate_sound(freq, duration=0.1, volume=0.3, wave_type='sine'):
    try:
        sample_rate = 22050
        n_samples = int(sample_rate * duration)
        buf = array.array('h')
        for i in range(n_samples):
            t = float(i) / sample_rate
            if wave_type == 'square':
                val = 32767.0 if math.sin(2.0 * math.pi * freq * t) > 0 else -32767.0
            else:
                val = 32767.0 * math.sin(2.0 * math.pi * freq * t)
            decay = (1.0 - (i / float(n_samples)))
            sample = int(val * volume * decay)
            buf.append(sample)
            buf.append(sample)
        return pygame.mixer.Sound(buffer=buf)
    except Exception:
        return None

# Preset SFX
SFX_HIT = generate_sound(880, 0.1, 0.3)
SFX_EXPLODE = generate_sound(110, 0.25, 0.5, 'square')
SFX_POWERUP = generate_sound(1200, 0.15, 0.3)
SFX_GEM = generate_sound(1760, 0.08, 0.2)
SFX_EMP = generate_sound(440, 0.4, 0.5, 'square')
SFX_FEVER = generate_sound(1500, 0.3, 0.4)

# Synth BGM Beats
BGM_NOTES = [220, 261, 329, 392, 440, 392, 329, 261]
bgm_index = 0
bgm_timer = 0.0

def play_sfx(sound):
    if sound and pygame.mixer.get_init():
        sound.play()

# Palette Warna
SPACE_BLACK = (5, 5, 12)
SUN_COLOR = (255, 200, 50)
SUN_GLOW = (255, 120, 0)
TARGET_PLANET = (50, 255, 140)
BOSS_PLANET = (230, 80, 255)
HAZARD_ASTEROID = (255, 60, 80)
SHIELD_COLOR = (0, 220, 255)
SLOW_COLOR = (255, 220, 50)
LIFE_COLOR = (255, 80, 150)
GEM_COLOR = (220, 100, 255)
EMP_COLOR = (0, 255, 255)
ORBIT_LINE = (40, 50, 75)
TEXT_COLOR = (245, 245, 245)
GOLD_COLOR = (255, 215, 0)

SKINS = [
    {'name': 'NEPTUNUS', 'color': (70, 170, 255), 'ring': False, 'price': 0, 'owned': True},
    {'name': 'LAVA CORE', 'color': (255, 90, 30), 'ring': False, 'price': 5, 'owned': False},
    {'name': 'SATURN GOLD', 'color': (240, 190, 60), 'ring': True, 'price': 10, 'owned': False},
    {'name': 'CYBERPUNK', 'color': (0, 255, 200), 'ring': True, 'price': 15, 'owned': False},
    {'name': 'GOD GODLIKE', 'color': (255, 0, 128), 'ring': True, 'price': 25, 'owned': False}
]

PIVOT = (WIDTH // 2, HEIGHT // 2)
MIN_RADIUS = 75
MAX_RADIUS = 260
BOB_RADIUS = 16
TARGET_RADIUS = 22

# Parallax Stars
STARS = []
for _ in range(140):
    layer = random.choice([1, 2, 3])
    STARS.append({
        'x': random.randint(0, WIDTH),
        'y': random.randint(0, HEIGHT),
        'layer': layer,
        'size': layer,
        'speed': layer * 25.0,
        'brightness': random.randint(120, 255)
    })

class FloatingText:
    def __init__(self, x, y, text, color):
        self.x, self.y = x, y
        self.text = text
        self.color = color
        self.alpha = 255
        self.vy = -45.0
        self.life = 1.0

    def update(self, dt):
        self.y += self.vy * dt
        self.life -= dt * 1.2
        self.alpha = max(0, int(255 * self.life))

    def draw(self, surface, font):
        if self.life > 0:
            txt_surf = font.render(self.text, True, self.color)
            txt_surf.set_alpha(self.alpha)
            surface.blit(txt_surf, (int(self.x - txt_surf.get_width() // 2), int(self.y)))

class Particle:
    def __init__(self, x, y, color):
        self.x, self.y = x, y
        self.vx = random.uniform(-220, 220)
        self.vy = random.uniform(-220, 220)
        self.color = color
        self.life = 1.0
        self.decay = random.uniform(1.8, 3.5)

    def update(self, dt):
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.life -= self.decay * dt

    def draw(self, surface):
        if self.life > 0:
            r = max(1, int(5 * self.life))
            pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), r)

def get_coords(angle, radius):
    x = PIVOT[0] + radius * math.cos(angle)
    y = PIVOT[1] + radius * math.sin(angle)
    return x, y

def create_game_state():
    return {
        'state': 'START',
        'score': 0,
        'high_score': 0,
        'gems': 0,
        'level': 1,
        'lives': 3,
        'combo': 0,
        'selected_skin': 0,
        'upgrade_magnet_lvl': 0,
        'upgrade_shield_start': False,
        'angle': math.pi / 2,
        'player_radius': 160.0,
        'direction': 1,
        'base_speed': 2.3,
        'target_angle': 0.0,
        'target_orbit_radius': 160.0,
        'is_boss': False,
        'boss_hp': 0,
        'boss_max_hp': 0,
        'hazards': [],
        'powerups': [],
        'gem_items': [],
        'shield_active': False,
        'slow_timer': 0.0,
        'warp_timer': 0.0,
        'emp_cooldown': 0.0,
        'emp_wave': {'active': False, 'radius': 0.0},
        'fever_meter': 0.0,
        'fever_active': False,
        'fever_timer': 0.0,
        'drone_angle': 0.0,
        'screen_shake': 0.0,
        'player_trail': [],
        'particles': [],
        'floating_texts': [],
        'laser_beams': []
    }

def spawn_round(g):
    g['is_boss'] = (g['level'] % 5 == 0)

    if g['is_boss']:
        g['boss_hp'] = 3 + (g['level'] // 5)
        g['boss_max_hp'] = g['boss_hp']
        add_floating_text(g, WIDTH // 2, HEIGHT // 2 - 100, f"⚠️ BOSS LEVEL {g['level']}!", BOSS_PLANET)

    g['target_orbit_radius'] = random.uniform(MIN_RADIUS + 25, MAX_RADIUS - 25)
    g['target_angle'] = random.uniform(0, 2 * math.pi)

    g['direction'] = random.choice([1, -1])
    g['base_speed'] = 2.0 + (g['level'] * 0.18)

    g['hazards'] = []
    count = min(8, 2 + g['level'] // 2)
    for _ in range(count):
        g['hazards'].append({
            'angle': random.uniform(0, 2 * math.pi),
            'radius': random.uniform(MIN_RADIUS + 15, MAX_RADIUS - 15)
        })

    g['powerups'] = []
    if random.random() < 0.5:
        p_type = random.choice(['SHIELD', 'SLOW', 'LIFE'])
        g['powerups'].append({
            'type': p_type,
            'angle': random.uniform(0, 2 * math.pi),
            'radius': random.uniform(MIN_RADIUS + 20, MAX_RADIUS - 20)
        })

    g['gem_items'] = []
    if random.random() < 0.7:
        g['gem_items'].append({
            'angle': random.uniform(0, 2 * math.pi),
            'radius': random.uniform(MIN_RADIUS + 10, MAX_RADIUS - 10)
        })

def add_floating_text(g, x, y, text, color):
    g['floating_texts'].append(FloatingText(x, y, text, color))

def add_particles(g, x, y, color, count=25):
    for _ in range(count):
        g['particles'].append(Particle(x, y, color))

def trigger_emp(g):
    if g['emp_cooldown'] <= 0:
        g['emp_cooldown'] = 12.0
        g['emp_wave']['active'] = True
        g['emp_wave']['radius'] = 10.0
        g['screen_shake'] = 0.4
        play_sfx(SFX_EMP)

        px, py = get_coords(g['angle'], g['player_radius'])
        add_floating_text(g, px, py, "⚡ EMP BLAST ACTIVATED!", EMP_COLOR)

        # Hancurkan semua Asteroid
        for h in g['hazards']:
            hx, hy = get_coords(h['angle'], h['radius'])
            add_particles(g, hx, hy, EMP_COLOR, 15)
        g['hazards'].clear()

        # Damage Boss jika ada
        if g['is_boss'] and g['boss_hp'] > 0:
            g['boss_hp'] -= 1
            tx, ty = get_coords(g['target_angle'], g['target_orbit_radius'])
            add_floating_text(g, tx, ty, "BOSS EMP HIT!", EMP_COLOR)
            if g['boss_hp'] <= 0:
                level_up(g)

def level_up(g):
    g['level'] += 1
    g['warp_timer'] = 1.0
    add_floating_text(g, WIDTH // 2, HEIGHT // 2, f"🚀 STAGE CLEAR! LEVEL {g['level']}", GOLD_COLOR)
    spawn_round(g)

def check_hit(g):
    if g['state'] != 'PLAYING':
        return

    px, py = get_coords(g['angle'], g['player_radius'])

    # Power-up
    for p in g['powerups'][:]:
        ix, iy = get_coords(p['angle'], p['radius'])
        if math.hypot(px - ix, py - iy) <= (BOB_RADIUS + 18):
            play_sfx(SFX_POWERUP)
            if p['type'] == 'SHIELD':
                g['shield_active'] = True
                add_floating_text(g, ix, iy, "SHIELD READY!", SHIELD_COLOR)
            elif p['type'] == 'SLOW':
                g['slow_timer'] = 5.0
                add_floating_text(g, ix, iy, "SLOW MOTION 5s", SLOW_COLOR)
            elif p['type'] == 'LIFE':
                g['lives'] = min(5, g['lives'] + 1)
                add_floating_text(g, ix, iy, "+1 EXTRA LIFE", LIFE_COLOR)

            add_particles(g, ix, iy, GOLD_COLOR, 20)
            g['powerups'].remove(p)

    # Hazard Collision (Abaikan jika sedang FEVER)
    hit_hazard = False
    if not g['fever_active']:
        for h in g['hazards']:
            hx, hy = get_coords(h['angle'], h['radius'])
            if math.hypot(px - hx, py - hy) <= (BOB_RADIUS + TARGET_RADIUS):
                hit_hazard = True
                break

    if hit_hazard:
        play_sfx(SFX_EXPLODE)
        g['screen_shake'] = 0.35
        if g['shield_active']:
            g['shield_active'] = False
            add_particles(g, px, py, SHIELD_COLOR, 25)
            add_floating_text(g, px, py, "SHIELD ABSORBED!", SHIELD_COLOR)
        else:
            g['lives'] -= 1
            g['combo'] = 0
            g['fever_meter'] = max(0, g['fever_meter'] - 30)
            add_particles(g, px, py, HAZARD_ASTEROID, 30)
            add_floating_text(g, px, py, "HIT ASTEROID! -1 LIFE", HAZARD_ASTEROID)

    # Target Collision
    tx, ty = get_coords(g['target_angle'], g['target_orbit_radius'])
    dist_target = math.hypot(px - tx, py - ty)
    radius_check = (BOB_RADIUS + (TARGET_RADIUS * 1.4 if g['is_boss'] else TARGET_RADIUS))
    hit_target = dist_target <= radius_check

    if hit_target and not hit_hazard:
        play_sfx(SFX_HIT)
        g['screen_shake'] = 0.25

        # Isi Fever Meter
        if not g['fever_active']:
            g['fever_meter'] += 25.0
            if g['fever_meter'] >= 100.0:
                g['fever_active'] = True
                g['fever_timer'] = 6.0
                g['fever_meter'] = 100.0
                play_sfx(SFX_FEVER)
                add_floating_text(g, WIDTH // 2, HEIGHT // 2, "🔥 FEVER MODE ACTIVATED! (2X PTS)", GOLD_COLOR)

        if g['is_boss']:
            g['boss_hp'] -= 1
            add_particles(g, tx, ty, BOSS_PLANET, 25)
            if g['boss_hp'] > 0:
                add_floating_text(g, tx, ty, f"BOSS HIT! HP: {g['boss_hp']}", BOSS_PLANET)
                return

        # Hit Berhasil / Boss Mati -> Tambah Skor
        g['combo'] += 1
        pts_multiplier = 2 if g['fever_active'] else 1
        pts = ((50 if g['is_boss'] else 15) * g['combo']) * pts_multiplier
        g['score'] += pts

        if g['score'] > g['high_score']:
            g['high_score'] = g['score']

        add_particles(g, px, py, TARGET_PLANET, 35)
        combo_str = f"COMBO x{g['combo']}! +{pts} PTS" if g['combo'] > 1 else f"+{pts} PTS"
        add_floating_text(g, px, py, combo_str, TARGET_PLANET)

        # LANGSUNG NAIK LEVEL SAAT BERHASIL HIT!
        level_up(g)

    elif not hit_target and not hit_hazard:
        play_sfx(SFX_EXPLODE)
        g['screen_shake'] = 0.2
        g['lives'] -= 1
        g['combo'] = 0
        add_particles(g, px, py, (255, 140, 0), 18)
        add_floating_text(g, px, py, "MISSED TARGET! -1 LIFE", (255, 140, 0))

    if g['lives'] <= 0:
        g['state'] = 'GAMEOVER'

font_large = pygame.font.SysFont("Arial", 38, bold=True)
font_medium = pygame.font.SysFont("Arial", 22, bold=True)
font_small = pygame.font.SysFont("Arial", 16)

g = create_game_state()

running = True
nebula_phase = 0.0

while running:
    dt = clock.tick(60) / 1000.0
    nebula_phase += dt * 0.5

    # BGM Synth
    bgm_timer += dt
    bgm_speed = 0.12 if g['fever_active'] else 0.22
    if bgm_timer >= bgm_speed:
        bgm_timer = 0.0
        if g['state'] == 'PLAYING':
            s_bgm = generate_sound(BGM_NOTES[bgm_index] * (1.25 if g['fever_active'] else 1.0), 0.08, 0.08)
            play_sfx(s_bgm)
            bgm_index = (bgm_index + 1) % len(BGM_NOTES)

    # --- Event Handling ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if g['state'] == 'PLAYING':
                    check_hit(g)
                elif g['state'] in ['START', 'GAMEOVER']:
                    high, gems, skin = g['high_score'], g['gems'], g['selected_skin']
                    mag_lvl, shld_s = g['upgrade_magnet_lvl'], g['upgrade_shield_start']
                    
                    g = create_game_state()
                    g['high_score'], g['gems'], g['selected_skin'] = high, gems, skin
                    g['upgrade_magnet_lvl'], g['upgrade_shield_start'] = mag_lvl, shld_s
                    
                    if g['upgrade_shield_start']:
                        g['shield_active'] = True

                    spawn_round(g)
                    g['state'] = 'PLAYING'

            elif event.key in [pygame.K_LSHIFT, pygame.K_RSHIFT]:
                if g['state'] == 'PLAYING':
                    trigger_emp(g)

            elif event.key in [pygame.K_s, pygame.K_TAB]:
                if g['state'] == 'START':
                    g['state'] = 'SHOP'
                elif g['state'] == 'SHOP':
                    g['state'] = 'START'

            elif event.key == pygame.K_p:
                if g['state'] == 'PLAYING':
                    g['state'] = 'PAUSE'
                elif g['state'] == 'PAUSE':
                    g['state'] = 'PLAYING'

            elif g['state'] == 'START':
                if event.key == pygame.K_LEFT:
                    g['selected_skin'] = (g['selected_skin'] - 1) % len(SKINS)
                elif event.key == pygame.K_RIGHT:
                    g['selected_skin'] = (g['selected_skin'] + 1) % len(SKINS)

            elif g['state'] == 'SHOP':
                if event.key == pygame.K_1:
                    cost = (g['upgrade_magnet_lvl'] + 1) * 8
                    if g['gems'] >= cost and g['upgrade_magnet_lvl'] < 3:
                        g['gems'] -= cost
                        g['upgrade_magnet_lvl'] += 1
                        play_sfx(SFX_POWERUP)
                elif event.key == pygame.K_2:
                    if g['gems'] >= 12 and not g['upgrade_shield_start']:
                        g['gems'] -= 12
                        g['upgrade_shield_start'] = True
                        play_sfx(SFX_POWERUP)

    # Logika Gameplay
    if g['state'] == 'PLAYING':
        keys = pygame.key.get_pressed()
        radius_speed = 220.0

        if keys[pygame.K_UP] or keys[pygame.K_w]:
            g['player_radius'] = min(MAX_RADIUS, g['player_radius'] + radius_speed * dt)
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            g['player_radius'] = max(MIN_RADIUS, g['player_radius'] - radius_speed * dt)

        px, py = get_coords(g['angle'], g['player_radius'])

        # Drone Movement
        g['drone_angle'] += 4.0 * dt
        drone_x = px + 32 * math.cos(g['drone_angle'])
        drone_y = py + 32 * math.sin(g['drone_angle'])

        # Drone Auto-Laser Tembak Asteroid Terdekat
        for h in g['hazards'][:]:
            hx, hy = get_coords(h['angle'], h['radius'])
            if math.hypot(drone_x - hx, drone_y - hy) < 70.0:
                g['laser_beams'].append({'x1': drone_x, 'y1': drone_y, 'x2': hx, 'y2': hy, 'life': 0.15})
                add_particles(g, hx, hy, EMP_COLOR, 15)
                g['hazards'].remove(h)
                play_sfx(SFX_HIT)
                add_floating_text(g, hx, hy, "DRONE DESTROY!", EMP_COLOR)

        # Update Timers
        if g['emp_cooldown'] > 0:
            g['emp_cooldown'] -= dt

        if g['emp_wave']['active']:
            g['emp_wave']['radius'] += 600.0 * dt
            if g['emp_wave']['radius'] > WIDTH:
                g['emp_wave']['active'] = False

        if g['fever_active']:
            g['fever_timer'] -= dt
            g['fever_meter'] = (g['fever_timer'] / 6.0) * 100.0
            if g['fever_timer'] <= 0:
                g['fever_active'] = False
                g['fever_meter'] = 0.0

        # Magnet Gem Effect
        magnet_pull_dist = 40.0 + (g['upgrade_magnet_lvl'] * 35.0)
        for gm in g['gem_items'][:]:
            gx, gy = get_coords(gm['angle'], gm['radius'])
            dist_p = math.hypot(px - gx, py - gy)

            if dist_p < magnet_pull_dist and g['upgrade_magnet_lvl'] > 0:
                gm['radius'] += (g['player_radius'] - gm['radius']) * dt * 4.0

            if dist_p <= (BOB_RADIUS + 14):
                play_sfx(SFX_GEM)
                gem_pts = 2 if g['fever_active'] else 1
                g['gems'] += gem_pts
                add_particles(g, gx, gy, GEM_COLOR, 15)
                add_floating_text(g, gx, gy, f"+{gem_pts} GEM 💎", GEM_COLOR)
                g['gem_items'].remove(gm)

        # Timers Slow & Warp
        if g['slow_timer'] > 0: g['slow_timer'] -= dt
        if g['warp_timer'] > 0: g['warp_timer'] -= dt

        speed_mult = 0.45 if g['slow_timer'] > 0 else 1.0
        current_speed = max(0.8, (g['base_speed'] + 1.1 * math.sin(g['angle'])) * speed_mult)
        
        g['angle'] += g['direction'] * current_speed * dt
        g['angle'] %= (2 * math.pi)

        # Trail
        g['player_trail'].append((px, py))
        if len(g['player_trail']) > 14:
            g['player_trail'].pop(0)

    # Parallax Stars Move
    star_mult = 8.0 if g['warp_timer'] > 0 else 1.0
    for st in STARS:
        st['y'] += st['speed'] * star_mult * dt
        if st['y'] > HEIGHT:
            st['y'] = 0
            st['x'] = random.randint(0, WIDTH)

    # Update Objects
    for ft in g['floating_texts'][:]:
        ft.update(dt)
        if ft.life <= 0: g['floating_texts'].remove(ft)

    for p in g['particles'][:]:
        p.update(dt)
        if p.life <= 0: g['particles'].remove(p)

    for lb in g['laser_beams'][:]:
        lb['life'] -= dt
        if lb['life'] <= 0: g['laser_beams'].remove(lb)

    # --- Rendering ---
    offset_x, offset_y = 0, 0
    if g['screen_shake'] > 0:
        g['screen_shake'] -= dt
        offset_x = random.randint(-6, 6)
        offset_y = random.randint(-6, 6)

    game_surface = pygame.Surface((WIDTH, HEIGHT))
    game_surface.fill(SPACE_BLACK)

    # Background Glow
    neb_r = int(100 + 30 * math.sin(nebula_phase))
    bg_color = (40, 20, 10) if g['fever_active'] else (20, 10, 45)
    pygame.draw.circle(game_surface, bg_color, PIVOT, neb_r + 140)

    # Parallax Stars
    for st in STARS:
        pygame.draw.circle(game_surface, (st['brightness'], st['brightness'], st['brightness']), (int(st['x']), int(st['y'])), st['size'])

    if g['state'] in ['PLAYING', 'PAUSE', 'GAMEOVER']:
        # Orbits
        pygame.draw.circle(game_surface, (20, 60, 45), PIVOT, int(g['target_orbit_radius']), 1)
        pygame.draw.circle(game_surface, ORBIT_LINE, PIVOT, int(g['player_radius']), 1)

        # EMP Wave
        if g['emp_wave']['active']:
            pygame.draw.circle(game_surface, EMP_COLOR, PIVOT, int(g['emp_wave']['radius']), 6)

        # Center Sun
        pygame.draw.circle(game_surface, SUN_GLOW, PIVOT, 32)
        pygame.draw.circle(game_surface, SUN_COLOR, PIVOT, 22)

        # Items
        for p in g['powerups']:
            ix, iy = get_coords(p['angle'], p['radius'])
            col = SHIELD_COLOR if p['type'] == 'SHIELD' else (SLOW_COLOR if p['type'] == 'SLOW' else LIFE_COLOR)
            pygame.draw.circle(game_surface, col, (int(ix), int(iy)), 12)

        for gm in g['gem_items']:
            gx, gy = get_coords(gm['angle'], gm['radius'])
            pygame.draw.circle(game_surface, GEM_COLOR, (int(gx), int(gy)), 9)

        # Hazards
        for h in g['hazards']:
            hx, hy = get_coords(h['angle'], h['radius'])
            pygame.draw.circle(game_surface, HAZARD_ASTEROID, (int(hx), int(hy)), TARGET_RADIUS)

        # Target / Boss
        tx, ty = get_coords(g['target_angle'], g['target_orbit_radius'])
        if g['is_boss']:
            b_rad = int(TARGET_RADIUS * 1.5)
            pygame.draw.circle(game_surface, BOSS_PLANET, (int(tx), int(ty)), b_rad)
            hp_ratio = g['boss_hp'] / g['boss_max_hp']
            pygame.draw.rect(game_surface, (50, 50, 50), (int(tx)-25, int(ty)-b_rad-12, 50, 6))
            pygame.draw.rect(game_surface, BOSS_PLANET, (int(tx)-25, int(ty)-b_rad-12, int(50 * hp_ratio), 6))
        else:
            pygame.draw.circle(game_surface, TARGET_PLANET, (int(tx), int(ty)), TARGET_RADIUS)

        # Player & Drone
        active_skin = SKINS[g['selected_skin']]
        trail_col = GOLD_COLOR if g['fever_active'] else active_skin['color']
        
        for idx, (tx_pos, ty_pos) in enumerate(g['player_trail']):
            alpha_r = int(BOB_RADIUS * ((idx + 1) / len(g['player_trail'])))
            pygame.draw.circle(game_surface, trail_col, (int(tx_pos), int(ty_pos)), max(1, alpha_r))

        px, py = get_coords(g['angle'], g['player_radius'])
        pygame.draw.line(game_surface, trail_col, PIVOT, (px, py), 2)
        pygame.draw.circle(game_surface, trail_col, (int(px), int(py)), BOB_RADIUS)

        # Draw Drone & Laser
        drone_x = px + 32 * math.cos(g['drone_angle'])
        drone_y = py + 32 * math.sin(g['drone_angle'])
        pygame.draw.circle(game_surface, EMP_COLOR, (int(drone_x), int(drone_y)), 6)
        pygame.draw.circle(game_surface, (255, 255, 255), (int(drone_x), int(drone_y)), 6, 1)

        for lb in g['laser_beams']:
            pygame.draw.line(game_surface, EMP_COLOR, (lb['x1'], lb['y1']), (lb['x2'], lb['y2']), 3)

        if g['shield_active']:
            pygame.draw.circle(game_surface, SHIELD_COLOR, (int(px), int(py)), BOB_RADIUS + 8, 3)

        # Particles & Floating Text
        for p in g['particles']: p.draw(game_surface)
        for ft in g['floating_texts']: ft.draw(game_surface, font_medium)

        # UI Headers
        score_txt = font_medium.render(f"SKOR: {g['score']} | HIGH: {g['high_score']} | 💎 {g['gems']}", True, TEXT_COLOR)
        level_txt = font_medium.render(f"LEVEL: {g['level']}", True, GOLD_COLOR)
        lives_txt = font_medium.render(f"NYAWA: {'❤️ ' * g['lives']}", True, HAZARD_ASTEROID)

        game_surface.blit(score_txt, (20, 20))
        game_surface.blit(level_txt, (20, 50))
        game_surface.blit(lives_txt, (WIDTH - 180, 20))

        # FEVER METER UI
        pygame.draw.rect(game_surface, (40, 40, 60), (20, 85, 180, 14))
        pygame.draw.rect(game_surface, GOLD_COLOR if g['fever_active'] else (255, 100, 0), (20, 85, int(180 * (g['fever_meter'] / 100.0)), 14))
        fever_label = font_small.render("🔥 FEVER MODE" if g['fever_active'] else "FEVER METER", True, TEXT_COLOR)
        game_surface.blit(fever_label, (25, 83))

        # EMP COOLDOWN UI
        emp_status = "READY [SHIFT]" if g['emp_cooldown'] <= 0 else f"EMP ({int(g['emp_cooldown'])}s)"
        emp_col = EMP_COLOR if g['emp_cooldown'] <= 0 else (120, 120, 120)
        emp_txt = font_medium.render(f"⚡ {emp_status}", True, emp_col)
        game_surface.blit(emp_txt, (20, 110))

    # Menu Start
    elif g['state'] == 'START':
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(230)
        overlay.fill((5, 5, 12))
        game_surface.blit(overlay, (0, 0))

        t1 = font_large.render("SPACE ORBIT: GOD TIER GACOR", True, TARGET_PLANET)
        t2 = font_small.render("Sistem Fixed: Tiap Nembak Berhasil = LANGSUNG NAIK LEVEL!", True, TEXT_COLOR)
        
        active_skin = SKINS[g['selected_skin']]
        skin_txt = font_medium.render(f"< SKIN: {active_skin['name']} >", True, GOLD_COLOR)
        pygame.draw.circle(game_surface, active_skin['color'], (WIDTH // 2, 290), 28)

        t4 = font_medium.render("TEKAN [SPASI] UNTUK MULAI MAIN", True, TEXT_COLOR)
        t5 = font_medium.render("TEKAN [S] ATAU [TAB] UNTUK BUKA TOKO GEM 💎", True, GEM_COLOR)

        game_surface.blit(t1, (WIDTH // 2 - t1.get_width() // 2, 120))
        game_surface.blit(t2, (WIDTH // 2 - t2.get_width() // 2, 170))
        game_surface.blit(skin_txt, (WIDTH // 2 - skin_txt.get_width() // 2, 220))
        game_surface.blit(t4, (WIDTH // 2 - t4.get_width() // 2, 400))
        game_surface.blit(t5, (WIDTH // 2 - t5.get_width() // 2, 440))

    # Menu Toko
    elif g['state'] == 'SHOP':
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(240)
        overlay.fill((8, 5, 20))
        game_surface.blit(overlay, (0, 0))

        shop_title = font_large.render("💎 TOKO KOSMIK & UPGRADE", True, GEM_COLOR)
        gem_bal = font_medium.render(f"Saldo Gem Anda: 💎 {g['gems']}", True, GOLD_COLOR)
        game_surface.blit(shop_title, (WIDTH // 2 - shop_title.get_width() // 2, 60))
        game_surface.blit(gem_bal, (WIDTH // 2 - gem_bal.get_width() // 2, 110))

        i1 = font_medium.render(f"[1] Upgrade Magnet Gem (Lvl {g['upgrade_magnet_lvl']}/3)", True, SHIELD_COLOR)
        i2 = font_medium.render(f"[2] Start With Shield (Perisai Awal)", True, SHIELD_COLOR)
        exit_txt = font_small.render("Tekan [S] atau [TAB] Untuk Kembali", True, TEXT_COLOR)

        game_surface.blit(i1, (100, 200))
        game_surface.blit(i2, (100, 260))
        game_surface.blit(exit_txt, (WIDTH // 2 - exit_txt.get_width() // 2, 520))

    elif g['state'] == 'GAMEOVER':
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(225)
        overlay.fill((5, 5, 12))
        game_surface.blit(overlay, (0, 0))

        t1 = font_large.render("GAME OVER - MISSION FAILED", True, HAZARD_ASTEROID)
        t2 = font_medium.render(f"Skor Akhir: {g['score']} | High Score: {g['high_score']} | Total Gem: 💎 {g['gems']}", True, TEXT_COLOR)
        t3 = font_medium.render("TEKAN [SPASI] UNTUK COBA LAGI", True, GOLD_COLOR)

        game_surface.blit(t1, (WIDTH // 2 - t1.get_width() // 2, 200))
        game_surface.blit(t2, (WIDTH // 2 - t2.get_width() // 2, 270))
        game_surface.blit(t3, (WIDTH // 2 - t3.get_width() // 2, 350))

    screen.blit(game_surface, (offset_x, offset_y))
    pygame.display.flip()

pygame.quit()
sys.exit()