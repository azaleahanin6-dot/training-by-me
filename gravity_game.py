import pygame
import math
import sys
import random
import array

# ==============================================================================
# INISIALISASI & AUDIO ENGINE SINTETIS
# ==============================================================================
pygame.init()
pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
pygame.font.init()

WIDTH, HEIGHT = 1000, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Physics Precision Arcades - Authentic Cavendish Edition")

def generate_synth_sound(freq, duration, wave_type="sine", volume=0.25):
    sample_rate = 44100
    n_samples = int(sample_rate * duration)
    buf = array.array('h')
    
    for i in range(n_samples):
        t = i / sample_rate
        fade = 1.0 - (i / n_samples)
        
        if wave_type == "sine":
            val = math.sin(2 * math.pi * freq * t)
        elif wave_type == "square":
            val = 1.0 if (t * freq) % 1.0 < 0.5 else -1.0
        elif wave_type == "noise":
            val = random.uniform(-1, 1)
        elif wave_type == "saw":
            val = 2.0 * ((t * freq) % 1.0) - 1.0
        else:
            val = math.sin(2 * math.pi * freq * t)
            
        sample = int(val * fade * volume * 32767)
        buf.append(sample)
        buf.append(sample)
        
    return pygame.mixer.Sound(buffer=buf)

# Sound Bank
SND_CLICK = generate_synth_sound(800, 0.04, "sine", 0.2)
SND_THRUST = generate_synth_sound(110, 0.06, "noise", 0.12)
SND_EXPLODE = generate_synth_sound(60, 0.4, "noise", 0.4)
SND_WIN = generate_synth_sound(523, 0.3, "saw", 0.3)

# Background Music Synthesizer
def start_bgm():
    sample_rate = 44100
    duration = 4.0
    n_samples = int(sample_rate * duration)
    buf = array.array('h')
    for i in range(n_samples):
        t = i / sample_rate
        val = 0.15 * math.sin(2 * math.pi * 110 * t) + 0.1 * math.sin(2 * math.pi * 164.81 * t)
        sample = int(val * 32767)
        buf.append(sample)
        buf.append(sample)
    snd = pygame.mixer.Sound(buffer=buf)
    snd.play(loops=-1)

start_bgm()

# Warna Visual Sci-Fi & Laboratorium Vintage
BG_SPACE = (8, 12, 22)
PANEL_BG = (18, 24, 38)
WHITE = (245, 245, 245)
GRAY = (140, 150, 170)
DARK_GRAY = (35, 42, 55)
GREEN_GLOW = (46, 204, 113)
RED_WARN = (231, 76, 60)
EARTH_BLUE = (41, 128, 185)
EARTH_ATMOS = (52, 152, 219)
CYAN_BEAM = (52, 231, 228)
SOLAR_GOLD = (241, 196, 15)

# Warna Elemen Cavendish Asli
WOOD_DARK = (78, 52, 34)
WOOD_LIGHT = (130, 88, 55)
LEAD_BASE = (120, 130, 140)
LEAD_HIGHLIGHT = (200, 210, 220)
BRASS_GOLD = (212, 175, 55)

# Fonts
FONT_BODY = pygame.font.SysFont("Segoe UI", 13)
FONT_BOLD = pygame.font.SysFont("Segoe UI", 13, bold=True)
FONT_BIG = pygame.font.SysFont("Segoe UI", 28, bold=True)

# Navigation States
game_state = "MODE_SELECT"  # "MODE_SELECT", "LEVEL_SELECT", "PLAYING"
selected_mode = 1           # 1: Orbit, 2: Moon Lander, 3: Cavendish
current_sub_level = 1
screen_shake = 0

# Stars background
STARS = [{"x": random.randint(0, WIDTH), "y": random.randint(0, HEIGHT), 
          "size": random.uniform(0.8, 2.2), "bright": random.randint(100, 255)} for _ in range(120)]

def draw_space_background(surface):
    surface.fill(BG_SPACE)
    for star in STARS:
        star["bright"] += random.choice([-2, 2])
        star["bright"] = max(80, min(255, star["bright"]))
        col = (star["bright"], star["bright"], min(255, star["bright"] + 20))
        pygame.draw.circle(surface, col, (int(star["x"]), int(star["y"])), int(star["size"]))

# ==============================================================================
# UI COMPONENTS & CONFETTI SYSTEM
# ==============================================================================
class Button:
    def __init__(self, x, y, w, h, text, color, hover_color, action_id=None):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.action_id = action_id
        self.is_hovered = False

    def draw(self, surface):
        col = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(surface, (5, 8, 15), self.rect.move(2, 2), border_radius=8)
        pygame.draw.rect(surface, col, self.rect, border_radius=8)
        pygame.draw.rect(surface, WHITE if self.is_hovered else GRAY, self.rect, width=1, border_radius=8)

        t_surf = FONT_BOLD.render(self.text, True, WHITE)
        surface.blit(t_surf, (self.rect.centerx - t_surf.get_width()//2, self.rect.centery - t_surf.get_height()//2))

    def update_hover(self, pos):
        self.is_hovered = self.rect.collidepoint(pos)
        return self.is_hovered

    def is_clicked(self, pos, event):
        if self.rect.collidepoint(pos) and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            SND_CLICK.play()
            return True
        return False

def draw_star(surface, x, y, radius, filled=True):
    points = []
    for i in range(10):
        r = radius if i % 2 == 0 else radius / 2.2
        angle = i * math.pi / 5 - math.pi / 2
        points.append((x + r * math.cos(angle), y + r * math.sin(angle)))
    col = SOLAR_GOLD if filled else DARK_GRAY
    pygame.draw.polygon(surface, col, points)
    pygame.draw.polygon(surface, WHITE if filled else GRAY, points, width=1)

class Confetti:
    def __init__(self):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(-50, -10)
        self.vx = random.uniform(-2, 2)
        self.vy = random.uniform(3, 7)
        self.color = random.choice([GREEN_GLOW, CYAN_BEAM, SOLAR_GOLD, (235, 77, 75), (155, 89, 182)])
        self.size = random.randint(4, 8)

    def update(self):
        self.x += self.vx
        self.y += self.vy

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (int(self.x), int(self.y), self.size, self.size))

class Particle:
    def __init__(self, x, y, vx, vy, color, size, lifetime):
        self.x, self.y = x, y
        self.vx, self.vy = vx, vy
        self.color = color
        self.size = size
        self.lifetime = lifetime
        self.max_life = lifetime

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.lifetime -= 1
        self.size = max(0, self.size - 0.04)

    def draw(self, surface):
        if self.lifetime > 0 and self.size > 0:
            alpha = int((self.lifetime / self.max_life) * 255)
            s = pygame.Surface((int(self.size*2), int(self.size*2)), pygame.SRCALPHA)
            pygame.draw.circle(s, (*self.color, alpha), (int(self.size), int(self.size)), int(self.size))
            surface.blit(s, (self.x - self.size, self.y - self.size))

# Helper: Gambar Bola Metalik 3D dengan Shading Efek Timbal/Seng
def draw_metallic_sphere(surface, center_x, center_y, radius, is_large=False):
    cx, cy = int(center_x), int(center_y)
    pygame.draw.circle(surface, LEAD_BASE, (cx, cy), radius)
    
    # Gradient overlay highlight 3D
    hl_size = max(1, radius // 3)
    hl_x = cx - radius // 3
    hl_y = cy - radius // 3
    pygame.draw.circle(surface, LEAD_HIGHLIGHT, (hl_x, hl_y), hl_size)
    
    border_col = BRASS_GOLD if is_large else WHITE
    pygame.draw.circle(surface, border_col, (cx, cy), radius, width=1)

# ==============================================================================
# MODE 1: ORBIT MASTER (3 LEVELS)
# ==============================================================================
earth_center = (500, 380)
earth_radius = 50

class OrbitGame:
    def __init__(self):
        self.particles = []
        self.asteroids = []
        self.confetti_list = []
        self.reset(1)

    def reset(self, sub_level):
        self.sub_level = sub_level
        self.sat_x = earth_center[0]
        self.sat_y = earth_center[1] - earth_radius - 12
        self.vx, self.vy = 0, 0
        self.launched = False
        self.dragging = False
        self.drag_start = (0, 0)
        self.drag_end = (0, 0)
        self.timer_in_orbit = 0
        self.status_msg = f"LEVEL {sub_level}: Tarik Satelit dengan Mouse lalu lepas!"
        self.status_color = WHITE
        self.game_over = False
        self.win = False
        self.stars_earned = 0
        self.lock_angle = 0
        self.lock_radius = 185
        self.particles.clear()
        self.confetti_list.clear()

        if sub_level == 1:
            self.clarke_r_min, self.clarke_r_max = 120, 250
            ast_count = 1
        elif sub_level == 2:
            self.clarke_r_min, self.clarke_r_max = 130, 240
            ast_count = 3
        else:
            self.clarke_r_min, self.clarke_r_max = 150, 210
            ast_count = 5
        
        self.asteroids = []
        for _ in range(ast_count):
            ang = random.uniform(0, math.tau)
            r = random.uniform(140, 220)
            self.asteroids.append({"angle": ang, "r": r, "speed": random.uniform(0.006, 0.012)})

    def handle_event(self, event):
        if self.launched: return

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = event.pos
            if math.hypot(mx - self.sat_x, my - self.sat_y) < 80:
                self.dragging = True
                self.drag_start = (self.sat_x, self.sat_y)

        elif event.type == pygame.MOUSEMOTION and self.dragging:
            self.drag_end = event.pos

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1 and self.dragging:
            self.dragging = False
            mx, my = event.pos
            self.vx = (self.sat_x - mx) * 0.038
            self.vy = (self.sat_y - my) * 0.038
            self.launched = True
            self.status_msg = "Satelit Meluncur! Masuk Zona Hijau..."

    def update(self):
        global screen_shake

        for ast in self.asteroids:
            ast["angle"] += ast["speed"]

        for p in self.particles[:]:
            p.update()
            if p.lifetime <= 0: self.particles.remove(p)

        if self.win:
            self.lock_angle += 0.02
            self.sat_x = earth_center[0] + self.lock_radius * math.cos(self.lock_angle)
            self.sat_y = earth_center[1] + self.lock_radius * math.sin(self.lock_angle)
            self.particles.append(Particle(self.sat_x, self.sat_y, random.uniform(-0.5,0.5), random.uniform(-0.5,0.5), GREEN_GLOW, 3, 20))
            if len(self.confetti_list) < 50:
                self.confetti_list.append(Confetti())
            for c in self.confetti_list: c.update()
            return

        if not self.launched or self.game_over: return

        self.particles.append(Particle(self.sat_x, self.sat_y, random.uniform(-0.3,0.3), random.uniform(-0.3,0.3), CYAN_BEAM, 3, 12))

        dx = earth_center[0] - self.sat_x
        dy = earth_center[1] - self.sat_y
        r_sq = dx**2 + dy**2
        r = math.sqrt(r_sq)

        if r < earth_radius + 6:
            self.status_msg = "Hancur! Menabrak Atmosfer Bumi."
            self.status_color = RED_WARN
            self.game_over = True
            screen_shake = 10
            SND_EXPLODE.play()
            return
        elif r > 700:
            self.status_msg = "Satelit Terlempar Keluar Ruang Angkasa!"
            self.status_color = RED_WARN
            self.game_over = True
            return

        for ast in self.asteroids:
            ax = earth_center[0] + ast["r"] * math.cos(ast["angle"])
            ay = earth_center[1] + ast["r"] * math.sin(ast["angle"])
            if math.hypot(self.sat_x - ax, self.sat_y - ay) < 16:
                self.status_msg = "Hancur! Menabrak Sampah Asteroid!"
                self.status_color = RED_WARN
                self.game_over = True
                screen_shake = 10
                SND_EXPLODE.play()
                return

        G_CONST = 12000.0
        acc = G_CONST / r_sq
        self.vx += acc * (dx / r)
        self.vy += acc * (dy / r)

        self.sat_x += self.vx
        self.sat_y += self.vy

        if self.clarke_r_min <= r <= self.clarke_r_max:
            self.timer_in_orbit += 1 / 60.0
            self.status_msg = f"Menstabilkan Orbit... ({self.timer_in_orbit:.1f}s / 1.0s)"
            self.status_color = GREEN_GLOW

            if self.timer_in_orbit >= 1.0:
                self.win = True
                self.game_over = True
                self.lock_radius = r
                self.lock_angle = math.atan2(self.sat_y - earth_center[1], self.sat_x - earth_center[0])
                self.status_msg = "MISI BERHASIL! Orbit Geostasioner Terbentuk!"
                self.status_color = GREEN_GLOW
                self.stars_earned = 3
                SND_WIN.play()

    def draw(self, surface):
        pygame.draw.circle(surface, GREEN_GLOW, earth_center, self.clarke_r_max, width=2)
        pygame.draw.circle(surface, GREEN_GLOW, earth_center, self.clarke_r_min, width=2)

        zone_surf = pygame.Surface((self.clarke_r_max*2, self.clarke_r_max*2), pygame.SRCALPHA)
        pygame.draw.circle(zone_surf, (*GREEN_GLOW, 25), (self.clarke_r_max, self.clarke_r_max), self.clarke_r_max)
        pygame.draw.circle(zone_surf, (0, 0, 0, 0), (self.clarke_r_max, self.clarke_r_max), self.clarke_r_min)
        surface.blit(zone_surf, (earth_center[0] - self.clarke_r_max, earth_center[1] - self.clarke_r_max))

        for i in range(10, 0, -3):
            s = pygame.Surface((earth_radius*2 + i*4, earth_radius*2 + i*4), pygame.SRCALPHA)
            pygame.draw.circle(s, (*EARTH_ATMOS, int(100/i)), (earth_radius + i*2, earth_radius + i*2), earth_radius + i)
            surface.blit(s, (earth_center[0] - earth_radius - i*2, earth_center[1] - earth_radius - i*2))
        pygame.draw.circle(surface, EARTH_BLUE, earth_center, earth_radius)

        for ast in self.asteroids:
            ax = earth_center[0] + ast["r"] * math.cos(ast["angle"])
            ay = earth_center[1] + ast["r"] * math.sin(ast["angle"])
            pygame.draw.circle(surface, DARK_GRAY, (int(ax), int(ay)), 8)
            pygame.draw.circle(surface, RED_WARN, (int(ax), int(ay)), 8, width=1)

        for p in self.particles: p.draw(surface)
        for c in self.confetti_list: c.draw(surface)

        if self.dragging:
            mx, my = self.drag_end
            sim_vx = (self.sat_x - mx) * 0.038
            sim_vy = (self.sat_y - my) * 0.038
            sim_x, sim_y = self.sat_x, self.sat_y
            
            for _ in range(140):
                dx = earth_center[0] - sim_x
                dy = earth_center[1] - sim_y
                r_sq = max(100, dx**2 + dy**2)
                r = math.sqrt(r_sq)
                acc = 12000.0 / r_sq
                sim_vx += acc * (dx / r)
                sim_vy += acc * (dy / r)
                sim_x += sim_vx
                sim_y += sim_vy
                pygame.draw.circle(surface, SOLAR_GOLD, (int(sim_x), int(sim_y)), 2)

            pygame.draw.line(surface, RED_WARN, (int(self.sat_x), int(self.sat_y)), (mx, my), 2)

        sat_angle = math.degrees(math.atan2(self.vy, self.vx)) if self.launched else 0
        sat_surf = pygame.Surface((36, 20), pygame.SRCALPHA)
        pygame.draw.rect(sat_surf, SOLAR_GOLD, (0, 5, 10, 10), border_radius=2)
        pygame.draw.rect(sat_surf, SOLAR_GOLD, (26, 5, 10, 10), border_radius=2)
        pygame.draw.rect(sat_surf, WHITE, (10, 3, 16, 14), border_radius=3)
        rot = pygame.transform.rotate(sat_surf, -sat_angle)
        surface.blit(rot, rot.get_rect(center=(int(self.sat_x), int(self.sat_y))).topleft)

        status_s = FONT_BOLD.render(self.status_msg, True, self.status_color)
        surface.blit(status_s, (500 - status_s.get_width()//2, 660))

# ==============================================================================
# MODE 2: MOON LANDER (3 LEVELS)
# ==============================================================================
class LanderGame:
    def __init__(self):
        self.particles = []
        self.confetti_list = []
        self.reset(1)

    def reset(self, sub_level):
        self.sub_level = sub_level
        self.x, self.y = 500, 100
        self.vx, self.vy = 0.0, 0.0
        self.angle = 0.0
        self.fuel = 100.0
        self.particles.clear()
        self.confetti_list.clear()

        if sub_level == 1:
            self.gravity = 0.005
            self.pad_w = 400
            self.wind = 0.0
            self.max_v = 7.0
            self.max_ang = 45.0
            self.fuel_drain = 0.03
            self.status_msg = "LEVEL 1 (SANGAT EASY): Mendarat santai di landasan lebar!"
        elif sub_level == 2:
            self.gravity = 0.008
            self.pad_w = 250
            self.wind = random.uniform(-0.004, 0.004)
            self.max_v = 4.5
            self.max_ang = 25.0
            self.fuel_drain = 0.08
            self.status_msg = "LEVEL 2 (SEDANG): Kontrol kecepatan & perhatikan angin!"
        else:
            self.gravity = 0.012
            self.pad_w = 160
            self.wind = random.uniform(-0.009, 0.009)
            self.max_v = 3.0
            self.max_ang = 15.0
            self.fuel_drain = 0.15
            self.status_msg = "LEVEL 3 (PRESISI TINGGI): Butuh pendaratan sempurna!"

        self.status_color = WHITE
        self.game_over = False
        self.win = False
        self.stars_earned = 0

    def update(self):
        global screen_shake
        for p in self.particles[:]:
            p.update()
            if p.lifetime <= 0: self.particles.remove(p)

        if self.win:
            if len(self.confetti_list) < 50:
                self.confetti_list.append(Confetti())
            for c in self.confetti_list: c.update()
            return

        if self.game_over: return

        self.vy += self.gravity
        self.vx += self.wind

        keys = pygame.key.get_pressed()
        if (keys[pygame.K_w] or keys[pygame.K_UP]) and self.fuel > 0:
            thrust = 0.25
            rad = math.radians(self.angle - 90)
            self.vx += thrust * math.cos(rad)
            self.vy += thrust * math.sin(rad)
            self.fuel = max(0.0, self.fuel - self.fuel_drain)
            SND_THRUST.play()

            tail_x = self.x - 12 * math.cos(rad)
            tail_y = self.y - 12 * math.sin(rad)
            for _ in range(2):
                self.particles.append(Particle(tail_x, tail_y, random.uniform(-0.8,0.8), random.uniform(-0.8,0.8), SOLAR_GOLD, 4, 10))

        if keys[pygame.K_a] or keys[pygame.K_LEFT]: self.angle -= 1.6
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]: self.angle += 1.6

        self.x += self.vx
        self.y += self.vy

        if self.y >= 550:
            self.y = 550
            speed = math.hypot(self.vx, self.vy)
            angle_err = abs(self.angle % 360)
            if angle_err > 180: angle_err = 360 - angle_err

            pad_left = 500 - (self.pad_w // 2)
            pad_right = 500 + (self.pad_w // 2)

            is_on_pad = (pad_left <= self.x <= pad_right)
            is_slow = (speed <= self.max_v)
            is_upright = (angle_err <= self.max_ang)

            if is_on_pad and is_slow and is_upright:
                self.win = True
                self.status_msg = "PENDARATAN MULUS BERHASIL! SELAMAT!"
                self.status_color = GREEN_GLOW
                self.stars_earned = 3 if self.fuel > 40 else 2
                SND_WIN.play()
            else:
                self.win = False
                self.status_color = RED_WARN
                if not is_on_pad:
                    self.status_msg = "GAGAL! Mendarat di luar area Landing Pad!"
                elif not is_slow:
                    self.status_msg = f"HANCUR! Kecepatan terlalu tinggi ({speed:.1f} m/s)!"
                else:
                    self.status_msg = f"HANCUR! Posisi roket terlalu miring ({angle_err:.1f} deg)!"
                screen_shake = 10
                SND_EXPLODE.play()

            self.game_over = True

    def draw(self, surface):
        pad_left = 500 - (self.pad_w // 2)
        pad_right = 500 + (self.pad_w // 2)

        pygame.draw.polygon(surface, (70, 78, 92), [(0, 560), (pad_left, 560), (pad_left - 30, 680), (0, 680)])
        pygame.draw.polygon(surface, (70, 78, 92), [(pad_right, 560), (WIDTH, 560), (WIDTH, 680), (pad_right + 30, 680)])
        pygame.draw.rect(surface, (45, 52, 65), (0, 620, WIDTH, 100))
        
        pygame.draw.rect(surface, GREEN_GLOW, (pad_left, 555, self.pad_w, 8), border_radius=4)
        pad_lbl = FONT_BOLD.render(f"LANDING PAD ({self.pad_w}m)", True, GREEN_GLOW)
        surface.blit(pad_lbl, (500 - pad_lbl.get_width()//2, 535))

        for p in self.particles: p.draw(surface)
        for c in self.confetti_list: c.draw(surface)

        if not (self.game_over and not self.win):
            lander_s = pygame.Surface((26, 30), pygame.SRCALPHA)
            pygame.draw.polygon(lander_s, WHITE, [(13,0), (2,22), (24,22)])
            pygame.draw.line(lander_s, SOLAR_GOLD, (0, 30), (5, 22), 2)
            pygame.draw.line(lander_s, SOLAR_GOLD, (26, 30), (21, 22), 2)
            pygame.draw.circle(lander_s, CYAN_BEAM, (13, 11), 4)

            rot = pygame.transform.rotate(lander_s, -self.angle)
            surface.blit(rot, rot.get_rect(center=(int(self.x), int(self.y))).topleft)

        hud_s = pygame.Surface((290, 110), pygame.SRCALPHA)
        hud_s.fill(PANEL_BG)
        pygame.draw.rect(hud_s, CYAN_BEAM, (0,0, 290, 110), width=1, border_radius=8)
        surface.blit(hud_s, (20, 60))

        speed_val = math.hypot(self.vx, self.vy)
        angle_err = abs(self.angle % 360)
        if angle_err > 180: angle_err = 360 - angle_err

        surface.blit(FONT_BOLD.render(f"TELEMETRI LEVEL {self.sub_level}", True, SOLAR_GOLD), (30, 68))
        surface.blit(FONT_BODY.render(f"Bahan Bakar : {self.fuel:.0f} %", True, WHITE), (30, 88))
        surface.blit(FONT_BODY.render(f"Kecepatan   : {speed_val:.2f} m/s (Maks: {self.max_v:.1f} m/s)", True, GREEN_GLOW if speed_val<=self.max_v else RED_WARN), (30, 108))
        surface.blit(FONT_BODY.render(f"Kemiringan  : {angle_err:.1f} deg (Maks: {self.max_ang:.1f} deg)", True, GREEN_GLOW if angle_err<=self.max_ang else RED_WARN), (30, 128))

        status_s = FONT_BOLD.render(self.status_msg, True, self.status_color)
        surface.blit(status_s, (500 - status_s.get_width()//2, 660))

# ==============================================================================
# MODE 3: LAB CAVENDISH AUTHENTIC (3 LEVELS)
# ==============================================================================
class CavendishGame:
    def __init__(self):
        self.confetti_list = []
        self.reset(1)

    def reset(self, sub_level):
        self.sub_level = sub_level
        self.dist_cm = 28.0
        self.angle_curr = 0.0
        self.angle_vel = 0.0
        self.timer_in_target = 0.0
        self.win = False
        self.game_over = False
        self.stars_earned = 0
        self.confetti_list.clear()

        if sub_level == 1:
            self.target_cm = 12.0
            self.M_mass = 158.0
            self.m_mass = 0.73
            self.tolerance = 0.50
            self.status_msg = "LEVEL 1: Atur Posisi Bola Besar M sampai Sinar Laser menunjuk Target 12.0 cm!"
        elif sub_level == 2:
            self.target_cm = 8.5
            self.M_mass = 180.0
            self.m_mass = 0.85
            self.tolerance = 0.35
            self.status_msg = "LEVEL 2: Ukuran massa bertambah, Target berpindah ke 8.5 cm!"
        else:
            self.target_cm = 16.5
            self.M_mass = 120.0
            self.m_mass = 0.50
            self.tolerance = 0.25
            self.status_msg = "LEVEL 3 (SENSITIF): Posisikan Bola M dengan presisi tinggi ke Target 16.5 cm!"

        self.status_color = WHITE

    def handle_input(self):
        if self.win or self.game_over: return
        keys = pygame.key.get_pressed()
        step = 0.08 if (keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]) else 0.20
        if keys[pygame.K_LEFT]: self.dist_cm = max(10.0, self.dist_cm - step)
        if keys[pygame.K_RIGHT]: self.dist_cm = min(45.0, self.dist_cm + step)

    def update(self):
        if self.win:
            if len(self.confetti_list) < 50:
                self.confetti_list.append(Confetti())
            for c in self.confetti_list: c.update()
            return

        r_m = self.dist_cm / 100.0
        G_const = 6.674e-11
        fg_N = G_const * (self.M_mass * self.m_mass) / (r_m**2)
        self.fg_nN = fg_N * 1e9

        target_angle = (35.0 / self.dist_cm) - 1.25
        accel = (target_angle - self.angle_curr) * 0.05
        self.angle_vel = (self.angle_vel + accel) * 0.90
        self.angle_curr += self.angle_vel

        self.laser_scale_cm = 10.0 + (self.angle_curr * 5.0)
        
        is_centered = abs(self.laser_scale_cm - self.target_cm) <= self.tolerance
        is_stable = abs(self.angle_vel) < 0.01

        if is_centered and is_stable:
            self.timer_in_target += 1.0 / 60.0
            if self.timer_in_target >= 1.5:
                self.win = True
                self.game_over = True
                self.stars_earned = 3
                self.status_msg = "STABIL! Nilai Gravitasi G Cavendish Berhasil Diukur!"
                self.status_color = GREEN_GLOW
                SND_WIN.play()
            else:
                self.status_msg = f"MENAHAN KESEIMBANGAN OPTIK: {int((self.timer_in_target/1.5)*100)} %..."
                self.status_color = SOLAR_GOLD
        else:
            self.timer_in_target = max(0.0, self.timer_in_target - 0.02)

    def draw(self, surface):
        # 1. Ruang Laboratorium
        pygame.draw.rect(surface, DARK_GRAY, (80, 80, 840, 520), border_radius=12)
        pygame.draw.rect(surface, GRAY, (80, 80, 840, 520), width=2, border_radius=12)

        # 2. Kotak Pelindung Kayu Asli Cavendish (Chamber Kaca)
        box_x, box_y, box_w, box_h = 320, 180, 360, 320
        pygame.draw.rect(surface, WOOD_DARK, (box_x, box_y, box_w, box_h), border_radius=8)
        pygame.draw.rect(surface, WOOD_LIGHT, (box_x, box_y, box_w, box_h), width=4, border_radius=8)
        
        # Panel Kaca Transparan Inner
        glass_surf = pygame.Surface((box_w - 16, box_h - 16), pygame.SRCALPHA)
        glass_surf.fill((180, 220, 255, 20))
        surface.blit(glass_surf, (box_x + 8, box_y + 8))

        # Stand & Gantungan Atas
        cx, cy = box_x + box_w // 2, box_y + box_h // 2
        pygame.draw.line(surface, BRASS_GOLD, (cx, 100), (cx, box_y), 6)
        
        # 3. Kawat Tuntir & Cermin Pemantul
        pygame.draw.line(surface, WHITE, (cx, box_y), (cx, cy), 1)  # Kawat Tuntir Halus
        
        # Cermin Kecil Pemantul Sinar di Tengah Kawat
        rad_rot = math.radians(self.angle_curr)
        mirror_w, mirror_h = 16, 6
        mirror_s = pygame.Surface((mirror_w, mirror_h), pygame.SRCALPHA)
        pygame.draw.rect(mirror_s, CYAN_BEAM, (0, 0, mirror_w, mirror_h), border_radius=2)
        pygame.draw.rect(mirror_s, WHITE, (0, 0, mirror_w, mirror_h), width=1, border_radius=2)
        rot_mirror = pygame.transform.rotate(mirror_s, math.degrees(-rad_rot))
        surface.blit(rot_mirror, rot_mirror.get_rect(center=(cx, cy)).topleft)

        # 4. Batang Horisontal Gantungan Bola Kecil (Inside Box)
        arm_len = 100
        x1 = cx + arm_len * math.cos(rad_rot)
        y1 = cy + arm_len * math.sin(rad_rot)
        x2 = cx - arm_len * math.cos(rad_rot)
        y2 = cy - arm_len * math.sin(rad_rot)

        pygame.draw.line(surface, WOOD_LIGHT, (x1, y1), (x2, y2), 4)

        # Bola Timbal Kecil (m)
        draw_metallic_sphere(surface, x1, y1, 10, is_large=False)
        draw_metallic_sphere(surface, x2, y2, 10, is_large=False)

        # 5. Bola Timbal Raksasa (M) & Lengan Pemutar Luar (Outside Box)
        offset_px = 30 + (self.dist_cm * 2.1)
        mx1 = x1 + offset_px * math.sin(rad_rot)
        my1 = y1 - offset_px * math.cos(rad_rot)
        mx2 = x2 - offset_px * math.sin(rad_rot)
        my2 = y2 + offset_px * math.cos(rad_rot)

        # Struktur Lengan Penahan Bola Raksasa
        pygame.draw.line(surface, BRASS_GOLD, (int(mx1), int(my1)), (int(mx2), int(my2)), 2)
        
        draw_metallic_sphere(surface, mx1, my1, 28, is_large=True)
        draw_metallic_sphere(surface, mx2, my2, 28, is_large=True)

        # 6. Pemancar Laser & Skala Penggaris Dinding
        laser_emitter_pos = (120, 480)
        pygame.draw.rect(surface, BRASS_GOLD, (laser_emitter_pos[0]-15, laser_emitter_pos[1]-10, 30, 20), border_radius=4)
        lbl_laser = FONT_BODY.render("LASER", True, WHITE)
        surface.blit(lbl_laser, (laser_emitter_pos[0]-16, laser_emitter_pos[1]+12))

        # Skala Penggaris Dinding
        ruler_x = 120
        pygame.draw.rect(surface, PANEL_BG, (ruler_x, 120, 45, 320), border_radius=4)
        pygame.draw.rect(surface, WHITE, (ruler_x, 120, 45, 320), width=1, border_radius=4)
        
        for cm_mark in range(0, 21, 2):
            mark_y = 140 + (cm_mark * 13)
            pygame.draw.line(surface, WHITE, (ruler_x + 28, mark_y), (ruler_x + 45, mark_y), 1)
            lbl = FONT_BODY.render(f"{cm_mark}", True, GRAY)
            surface.blit(lbl, (ruler_x + 8, mark_y - 6))

        # Mark Target pada Penggaris
        target_y = 140 + (self.target_cm * 13)
        pygame.draw.rect(surface, GREEN_GLOW, (ruler_x + 2, target_y - 7, 41, 14), width=2, border_radius=3)
        tgt_txt = FONT_BOLD.render("TARGET", True, GREEN_GLOW)
        surface.blit(tgt_txt, (ruler_x - 55, target_y - 7))

        # Sinar Laser Masuk -> Memantul di Cermin -> Jatuh di Penggaris
        laser_hit_y = 140 + (self.laser_scale_cm * 13.0)
        pygame.draw.line(surface, RED_WARN, laser_emitter_pos, (cx, cy), 2)
        pygame.draw.line(surface, RED_WARN, (cx, cy), (ruler_x + 45, int(laser_hit_y)), 2)
        pygame.draw.circle(surface, RED_WARN, (ruler_x + 45, int(laser_hit_y)), 4)

        for c in self.confetti_list: c.draw(surface)

        # Panel HUD Data
        hud_x, hud_y = 700, 100
        hud_bg = pygame.Surface((200, 170), pygame.SRCALPHA)
        hud_bg.fill(PANEL_BG)
        pygame.draw.rect(hud_bg, CYAN_BEAM, (0, 0, 200, 170), width=1, border_radius=8)
        surface.blit(hud_bg, (hud_x, hud_y))

        surface.blit(FONT_BOLD.render(f"LAB CAVENDISH LV {self.sub_level}", True, SOLAR_GOLD), (hud_x + 12, hud_y + 10))
        surface.blit(FONT_BODY.render(f"Bola Timbal M : {self.M_mass:.0f} kg", True, WHITE), (hud_x + 12, hud_y + 35))
        surface.blit(FONT_BODY.render(f"Bola Timbal m : {self.m_mass:.2f} kg", True, WHITE), (hud_x + 12, hud_y + 57))
        surface.blit(FONT_BODY.render(f"Jarak Antar-Bola: {self.dist_cm:.1f} cm", True, CYAN_BEAM), (hud_x + 12, hud_y + 79))
        surface.blit(FONT_BODY.render(f"Gaya Gravitasi F: {self.fg_nN:.2f} nN", True, SOLAR_GOLD), (hud_x + 12, hud_y + 101))
        surface.blit(FONT_BODY.render(f"Posisi Pantul   : {self.laser_scale_cm:.1f} cm", True, GREEN_GLOW if abs(self.laser_scale_cm-self.target_cm)<=self.tolerance else RED_WARN), (hud_x + 12, hud_y + 123))
        surface.blit(FONT_BODY.render(f"Target Skala    : {self.target_cm:.1f} cm", True, GREEN_GLOW), (hud_x + 12, hud_y + 143))

        status_s = FONT_BOLD.render(self.status_msg, True, self.status_color)
        surface.blit(status_s, (500 - status_s.get_width()//2, 660))

# ==============================================================================
# MENU SYSTEM & RESULT MODAL
# ==============================================================================
PHYSICS_FACTS = {
    1: "Fakta Orbit: Orbit Geostasioner berada di ketinggian sekitar 35.786 km!",
    2: "Fakta Lander: Gravitasi Bulan hanya sekitar 1/6 dari gravitasi Bumi!",
    3: "Fakta Cavendish: Percobaan Cavendish pada tahun 1798 berhasil 'menimbang' massa planet Bumi!"
}

btn_next_lvl = Button(350, 420, 300, 44, "LANJUT LEVEL BERIKUTNYA [ENTER]", GREEN_GLOW, CYAN_BEAM)
btn_retry_game = Button(350, 472, 300, 40, "COBA LAGI LEVEL INI [R]", SOLAR_GOLD, WHITE)
btn_select_lvl = Button(350, 520, 300, 40, "PILIH LEVEL [L]", PANEL_BG, CYAN_BEAM)
btn_main_menu = Button(350, 568, 300, 40, "MENU UTAMA [M]", PANEL_BG, GRAY)

def draw_result_modal(surface, is_win, mode, sub_level, stars, mouse_pos):
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((5, 8, 15, 220))
    surface.blit(overlay, (0,0))

    box = pygame.Rect(200, 120, 600, 500)
    pygame.draw.rect(surface, PANEL_BG, box, border_radius=12)
    pygame.draw.rect(surface, GREEN_GLOW if is_win else RED_WARN, box, width=2, border_radius=12)

    title_text = f"LEVEL {sub_level} SELESAI!" if is_win else "MISI GAGAL!"
    t_surf = FONT_BIG.render(title_text, True, GREEN_GLOW if is_win else RED_WARN)
    surface.blit(t_surf, (WIDTH//2 - t_surf.get_width()//2, 145))

    if is_win:
        for i in range(3):
            sx = 420 + (i * 80)
            draw_star(surface, sx, 225, 22, filled=(i < stars))

        fact_txt = PHYSICS_FACTS.get(mode, "Fakta Fisika Keren!")
        f_surf = FONT_BODY.render(fact_txt, True, SOLAR_GOLD)
        surface.blit(f_surf, (WIDTH//2 - f_surf.get_width()//2, 275))

    btn_retry_game.update_hover(mouse_pos)
    btn_retry_game.draw(surface)

    btn_select_lvl.update_hover(mouse_pos)
    btn_select_lvl.draw(surface)

    btn_main_menu.update_hover(mouse_pos)
    btn_main_menu.draw(surface)

    if is_win and sub_level < 3:
        btn_next_lvl.update_hover(mouse_pos)
        btn_next_lvl.draw(surface)

# Mode Selection Buttons
mode_buttons = [
    Button(320, 250, 360, 55, "MODE 1: Orbit Master (3 Level)", EARTH_BLUE, CYAN_BEAM, action_id=1),
    Button(320, 330, 360, 55, "MODE 2: Moon Lander (3 Level)", SOLAR_GOLD, WHITE, action_id=2),
    Button(320, 410, 360, 55, "MODE 3: Lab Cavendish (3 Level)", (155, 89, 182), CYAN_BEAM, action_id=3)
]

# Sub-level Selection Buttons
level_buttons = [
    Button(350, 250, 300, 50, "Level 1: Santai / Easy", GREEN_GLOW, CYAN_BEAM, action_id=1),
    Button(350, 320, 300, 50, "Level 2: Sedang / Medium", SOLAR_GOLD, WHITE, action_id=2),
    Button(350, 390, 300, 50, "Level 3: Presisi / Hard", RED_WARN, SOLAR_GOLD, action_id=3),
    Button(350, 480, 300, 40, "< Kembali ke Pilih Mode", PANEL_BG, GRAY, action_id=0)
]

def main():
    global game_state, selected_mode, current_sub_level, screen_shake
    clock = pygame.time.Clock()

    orbit_game = OrbitGame()
    lander_game = LanderGame()
    cavendish_game = CavendishGame()

    running = True
    while running:
        clock.tick(60)
        mouse_pos = pygame.mouse.get_pos()

        if selected_mode == 1: curr_game = orbit_game
        elif selected_mode == 2: curr_game = lander_game
        else: curr_game = cavendish_game

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if game_state == "MODE_SELECT":
                for btn in mode_buttons:
                    if btn.is_clicked(mouse_pos, event):
                        selected_mode = btn.action_id
                        game_state = "LEVEL_SELECT"

            elif game_state == "LEVEL_SELECT":
                for btn in level_buttons:
                    if btn.is_clicked(mouse_pos, event):
                        if btn.action_id == 0:
                            game_state = "MODE_SELECT"
                        else:
                            current_sub_level = btn.action_id
                            curr_game.reset(current_sub_level)
                            game_state = "PLAYING"

            elif game_state == "PLAYING":
                if curr_game.game_over:
                    if curr_game.win and current_sub_level < 3 and (btn_next_lvl.is_clicked(mouse_pos, event) or (event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN)):
                        current_sub_level += 1
                        curr_game.reset(current_sub_level)
                    elif btn_retry_game.is_clicked(mouse_pos, event) or (event.type == pygame.KEYDOWN and event.key == pygame.K_r):
                        curr_game.reset(current_sub_level)
                    elif btn_select_lvl.is_clicked(mouse_pos, event) or (event.type == pygame.KEYDOWN and event.key == pygame.K_l):
                        game_state = "LEVEL_SELECT"
                    elif btn_main_menu.is_clicked(mouse_pos, event) or (event.type == pygame.KEYDOWN and event.key == pygame.K_m):
                        game_state = "MODE_SELECT"
                else:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_m: game_state = "MODE_SELECT"
                        elif event.key == pygame.K_l: game_state = "LEVEL_SELECT"
                        elif event.key == pygame.K_r: curr_game.reset(current_sub_level)

                    if selected_mode == 1:
                        orbit_game.handle_event(event)

        render_offset = [0, 0]
        if screen_shake > 0:
            render_offset[0] = random.randint(-screen_shake, screen_shake)
            render_offset[1] = random.randint(-screen_shake, screen_shake)
            screen_shake -= 1

        canvas = pygame.Surface((WIDTH, HEIGHT))
        draw_space_background(canvas)

        if game_state == "MODE_SELECT":
            title = FONT_BIG.render("PILIH MODE PERMAINAN FISIKA", True, SOLAR_GOLD)
            canvas.blit(title, (WIDTH//2 - title.get_width()//2, 150))
            for btn in mode_buttons:
                btn.update_hover(mouse_pos)
                btn.draw(canvas)

        elif game_state == "LEVEL_SELECT":
            mode_names = {1: "ORBIT MASTER", 2: "MOON LANDER", 3: "LAB CAVENDISH"}
            title = FONT_BIG.render(f"PILIH LEVEL: {mode_names[selected_mode]}", True, CYAN_BEAM)
            canvas.blit(title, (WIDTH//2 - title.get_width()//2, 150))
            for btn in level_buttons:
                btn.update_hover(mouse_pos)
                btn.draw(canvas)

        elif game_state == "PLAYING":
            if selected_mode == 1:
                orbit_game.update()
                orbit_game.draw(canvas)
            elif selected_mode == 2:
                lander_game.update()
                lander_game.draw(canvas)
            elif selected_mode == 3:
                cavendish_game.handle_input()
                cavendish_game.update()
                cavendish_game.draw(canvas)

            pygame.draw.rect(canvas, PANEL_BG, (0, 0, WIDTH, 45))
            pygame.draw.line(canvas, GRAY, (0, 45), (WIDTH, 45), 1)
            canvas.blit(FONT_BODY.render("[M] Menu Utama  |  [L] Pilih Level  |  [R] Reset Level  |  [Panah Kiri/Kanan + Shift] Kontrol Presisi Laser", True, CYAN_BEAM), (20, 12))

            if curr_game.game_over:
                draw_result_modal(canvas, curr_game.win, selected_mode, current_sub_level, curr_game.stars_earned, mouse_pos)

        screen.blit(canvas, render_offset)
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()