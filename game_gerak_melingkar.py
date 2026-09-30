import pygame
import math
import sys
import random

# Inisialisasi Pygame
pygame.init()
pygame.font.init()

# Konfigurasi Layar & Frame Rate
WIDTH, HEIGHT = 1150, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("A1 GP Centripetal Racing Simulation")
clock = pygame.time.Clock()

# Palet Warna HD & Neon Glow
COLOR_BG = (10, 14, 23)
ASPHALT = (35, 39, 47)
ASPHALT_LINE = (70, 78, 92)
GRASS_DARK = (18, 53, 26)
GRASS_LIGHT = (24, 71, 34)
KERB_WHITE = (240, 242, 245)
KERB_RED = (225, 29, 72)

# Warna UI & HUD
PANEL_GLASS = (18, 25, 38, 210)
PANEL_BORDER = (45, 60, 85, 255)
CYAN_GLOW = (6, 182, 212)
GREEN_NEON = (34, 197, 94)
RED_NEON = (239, 68, 68)
YELLOW_NEON = (250, 204, 21)
WHITE = (255, 255, 255)
GRAY = (148, 163, 184)
GOLD = (234, 179, 8)

# Warna Livery Mobil A1 GP
COLOR_PLAYER = (14, 165, 233)   # A1 Indonesia (Electric Blue)
COLOR_AI1 = (225, 29, 72)      # A1 Netherlands (Red)
COLOR_AI2 = (16, 185, 129)     # A1 Great Britain (Green)
COLOR_AI3 = (245, 158, 11)     # A1 South Africa (Gold/Orange)

# Font
FONT_TITLE = pygame.font.SysFont("Segoe UI", 18, bold=True)
FONT_BODY = pygame.font.SysFont("Consolas", 13)
FONT_HUD = pygame.font.SysFont("Segoe UI", 15, bold=True)
FONT_BIG = pygame.font.SysFont("Segoe UI", 25, bold=True)
FONT_SPEED = pygame.font.SysFont("Impact", 36)

# --- PARAMETER FISIKA & SIRKUIT ---
PIXELS_PER_METER = 90.0  # Skala: 90 px = 1 meter
CENTER_X, CENTER_Y = 330, 360  # Pusat Titik Sirkuit
TOTAL_LAPS = 3

R_INNER_LIMIT = 1.6   # Jari-jari dalam (m)
R_OUTER_LIMIT = 3.4   # Jari-jari luar (m)

MASS = 1000.0         # Massa mobil (kg)
G_GRAVITY = 9.8       # Gravitasi (m/s²)
MU_FRICTION = 0.75    # Koefisien gesek ban
F_MAX_GRIP = MU_FRICTION * MASS * G_GRAVITY  # Gaya gesek maks (7350 N)

# --- SISTEM PARTIKEL & BEKAS BAN ---
class Particle:
    def __init__(self, x, y, vx, vy, color, size, lifetime, p_type="smoke"):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.color = color
        self.size = size
        self.lifetime = lifetime
        self.max_lifetime = lifetime
        self.p_type = p_type

    def update(self, dt):
        self.x += self.vx * dt * 60
        self.y += self.vy * dt * 60
        self.lifetime -= dt
        if self.p_type == "smoke":
            self.size += 0.1
        elif self.p_type == "spark":
            self.size = max(0.5, self.size - 0.05)

    def draw(self, surface):
        if self.lifetime <= 0: return
        alpha = int(255 * (self.lifetime / self.max_lifetime))
        if self.p_type == "smoke":
            s = pygame.Surface((int(self.size*2), int(self.size*2)), pygame.SRCALPHA)
            pygame.draw.circle(s, (180, 180, 180, int(alpha * 0.35)), (int(self.size), int(self.size)), int(self.size))
            surface.blit(s, (self.x - self.size, self.y - self.size))
        elif self.p_type == "spark":
            s = pygame.Surface((int(self.size*2), int(self.size*2)), pygame.SRCALPHA)
            pygame.draw.circle(s, (255, 200, 50, alpha), (int(self.size), int(self.size)), int(self.size))
            surface.blit(s, (self.x - self.size, self.y - self.size))

class SkidMark:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.alpha = 150

    def draw(self, surface):
        if self.alpha <= 0: return
        s = pygame.Surface((5, 5), pygame.SRCALPHA)
        pygame.draw.circle(s, (20, 20, 20, int(self.alpha)), (2, 2), 2)
        surface.blit(s, (self.x - 2, self.y - 2))

particles = []
skid_marks = []

# --- KELAS MOBIL BALAP A1 GP (OPEN-WHEEL) ---
class Car:
    def __init__(self, name, color, initial_r, initial_omega, is_player=False):
        self.name = name
        self.color = color
        self.r = initial_r           
        self.omega = initial_omega   # Kecepatan sudut diperlambat
        self.theta = -math.pi / 2    # Start di bagian atas sirkuit
        self.is_player = is_player
        
        self.lap = 1
        self.total_angle = 0.0
        self.is_slipping = False
        self.offroad = False
        self.is_braking = False

        self.v = 0.0
        self.ac = 0.0
        self.Fc = 0.0

    def update_physics(self, dt):
        self.v = self.omega * self.r               # Kecepatan linear (m/s)
        self.ac = (self.omega ** 2) * self.r       # Percepatan sentripetal (m/s²)
        self.Fc = MASS * self.ac                   # Gaya sentripetal (N)

        # Cek Traksi & Slip Tikungan
        if self.Fc > F_MAX_GRIP:
            self.is_slipping = True
            self.r += 0.5 * dt                     # Understeer perlahan keluar
            self.omega = max(0.2, self.omega - 0.8 * dt)
        else:
            self.is_slipping = False

        # Cek Offroad (Rumput)
        if self.r < R_INNER_LIMIT or self.r > R_OUTER_LIMIT:
            self.offroad = True
            self.omega = max(0.3, self.omega - 1.5 * dt)
            if self.r < R_INNER_LIMIT: self.r += 0.3 * dt
            if self.r > R_OUTER_LIMIT: self.r -= 0.3 * dt
        else:
            self.offroad = False

        # Update Sudut & Lap
        d_theta = self.omega * dt
        self.theta += d_theta
        self.total_angle += d_theta

        c_lap = int(self.total_angle / (2 * math.pi)) + 1
        if c_lap > self.lap and self.lap <= TOTAL_LAPS:
            self.lap = min(c_lap, TOTAL_LAPS + 1)

    def draw(self, surface):
        px = int(CENTER_X + self.r * PIXELS_PER_METER * math.cos(self.theta))
        py = int(CENTER_Y + self.r * PIXELS_PER_METER * math.sin(self.theta))

        # Partikel Asap & Bekas Ban
        if self.is_slipping:
            skid_marks.append(SkidMark(px, py))
            if len(skid_marks) > 150: skid_marks.pop(0)
            for _ in range(1):
                particles.append(Particle(
                    px + random.uniform(-3, 3), py + random.uniform(-3, 3),
                    random.uniform(-0.3, 0.3), random.uniform(-0.3, 0.3),
                    (200, 200, 200), random.uniform(2, 5), 0.6, "smoke"
                ))

        if self.offroad:
            for _ in range(1):
                particles.append(Particle(
                    px, py, random.uniform(-0.8, 0.8), random.uniform(-0.8, 0.8),
                    (255, 200, 50), random.uniform(2, 3), 0.25, "spark"
                ))

        # KOREKSI ROTASI: Hidung selalu menghadap depan sesuai pergerakan tangent
        angle_deg = -math.degrees(self.theta + math.pi / 2)

        # DESIGN MOBIL BALAP A1 GRAND PRIX (OPEN-WHEEL)
        car_w, car_h = 44, 22
        car_surf = pygame.Surface((car_w, car_h), pygame.SRCALPHA)

        # Bayangan Mobil
        pygame.draw.ellipse(car_surf, (0, 0, 0, 90), (3, 3, 38, 16))

        # 1. Empat Roda Terbuka (Open Wheels)
        # Roda Depan (Kiri & Kanan)
        pygame.draw.rect(car_surf, (25, 25, 25), (28, 1, 9, 4), border_radius=1)
        pygame.draw.rect(car_surf, (25, 25, 25), (28, 17, 9, 4), border_radius=1)
        # Roda Belakang (Lebih Besar & Lebar)
        pygame.draw.rect(car_surf, (20, 20, 20), (6, 0, 11, 5), border_radius=1)
        pygame.draw.rect(car_surf, (20, 20, 20), (6, 17, 11, 5), border_radius=1)
        # Rim Striping Kuning
        pygame.draw.line(car_surf, YELLOW_NEON, (30, 3), (34, 3), 1)
        pygame.draw.line(car_surf, YELLOW_NEON, (30, 19), (34, 19), 1)

        # 2. Sidepod (Air Intakes Samping)
        body_col = RED_NEON if self.is_slipping else (GRAY if self.offroad else self.color)
        pygame.draw.rect(car_surf, body_col, (15, 4, 12, 4), border_radius=2)
        pygame.draw.rect(car_surf, body_col, (15, 14, 12, 4), border_radius=2)

        # 3. Bodi Ramping & Hidung Runcing A1 GP (Nosecone)
        nose_points = [(7, 7), (25, 7), (39, 10), (42, 11), (39, 12), (25, 15), (7, 15)]
        pygame.draw.polygon(car_surf, body_col, nose_points)

        # 4. Sayap Depan (Front Wing + Endplates)
        pygame.draw.rect(car_surf, (30, 30, 30), (38, 2, 3, 18))
        pygame.draw.rect(car_surf, WHITE, (37, 1, 5, 2))
        pygame.draw.rect(car_surf, WHITE, (37, 19, 5, 2))

        # 5. Sayap Belakang (Rear Wing + Endplates)
        pygame.draw.rect(car_surf, (20, 20, 20), (2, 3, 5, 16))
        pygame.draw.rect(car_surf, WHITE, (0, 2, 7, 2))
        pygame.draw.rect(car_surf, WHITE, (0, 18, 7, 2))

        # 6. Kokpit Terbuka & Helm Pengemudi
        pygame.draw.ellipse(car_surf, (15, 15, 15), (17, 9, 10, 4))
        pygame.draw.circle(car_surf, GOLD, (22, 11), 2)  # Helm

        # 7. Lampu LED Belakang
        brake_col = RED_NEON if self.is_braking else (180, 0, 0)
        pygame.draw.circle(car_surf, brake_col, (2, 11), 2)

        # Render ke Layar Utama dengan Rotasi Presisi
        rotated_surf = pygame.transform.rotate(car_surf, angle_deg)
        rect = rotated_surf.get_rect(center=(px, py))
        surface.blit(rotated_surf, rect.topleft)

        return px, py

def draw_circuit(surface):
    """Sirkuit Balap Sirkular"""
    surface.fill(COLOR_BG)

    # Rumput
    pygame.draw.circle(surface, GRASS_DARK, (CENTER_X, CENTER_Y), 340)
    pygame.draw.circle(surface, GRASS_LIGHT, (CENTER_X, CENTER_Y), 310)

    r_out_px = int(R_OUTER_LIMIT * PIXELS_PER_METER)
    r_in_px = int(R_INNER_LIMIT * PIXELS_PER_METER)

    # Kerb Merah-Putih Luar
    pygame.draw.circle(surface, KERB_WHITE, (CENTER_X, CENTER_Y), r_out_px + 7)
    for a in range(0, 360, 10):
        rad1, rad2 = math.radians(a), math.radians(a + 5)
        p1 = (CENTER_X + (r_out_px + 7) * math.cos(rad1), CENTER_Y + (r_out_px + 7) * math.sin(rad1))
        p2 = (CENTER_X + (r_out_px + 7) * math.cos(rad2), CENTER_Y + (r_out_px + 7) * math.sin(rad2))
        pygame.draw.line(surface, KERB_RED, p1, p2, 7)

    # Aspal Utama
    pygame.draw.circle(surface, ASPHALT, (CENTER_X, CENTER_Y), r_out_px)
    
    # Kerb Dalam
    pygame.draw.circle(surface, KERB_WHITE, (CENTER_X, CENTER_Y), r_in_px)
    for a in range(0, 360, 10):
        rad1, rad2 = math.radians(a), math.radians(a + 5)
        p1 = (CENTER_X + r_in_px * math.cos(rad1), CENTER_Y + r_in_px * math.sin(rad1))
        p2 = (CENTER_X + r_in_px * math.cos(rad2), CENTER_Y + r_in_px * math.sin(rad2))
        pygame.draw.line(surface, KERB_RED, p1, p2, 7)

    pygame.draw.circle(surface, GRASS_DARK, (CENTER_X, CENTER_Y), r_in_px - 7)

    # Bekas Ban
    for sm in skid_marks:
        sm.draw(surface)

    # Marka Putus-putus Jalur Tengah
    r_mid_px = int(((R_INNER_LIMIT + R_OUTER_LIMIT) / 2) * PIXELS_PER_METER)
    for a in range(0, 360, 8):
        rad1, rad2 = math.radians(a), math.radians(a + 4)
        x1, y1 = CENTER_X + r_mid_px * math.cos(rad1), CENTER_Y + r_mid_px * math.sin(rad1)
        x2, y2 = CENTER_X + r_mid_px * math.cos(rad2), CENTER_Y + r_mid_px * math.sin(rad2)
        pygame.draw.line(surface, ASPHALT_LINE, (x1, y1), (x2, y2), 2)

    # Garis Start/Finish Catur
    sf_y_top = CENTER_Y - r_out_px
    sf_y_bottom = CENTER_Y - r_in_px
    blocks = 8
    bh = (sf_y_bottom - sf_y_top) / blocks
    for i in range(blocks):
        c1 = WHITE if i % 2 == 0 else (20, 20, 20)
        c2 = (20, 20, 20) if i % 2 == 0 else WHITE
        pygame.draw.rect(surface, c1, (CENTER_X - 4, sf_y_top + i * bh, 4, bh))
        pygame.draw.rect(surface, c2, (CENTER_X, sf_y_top + i * bh, 4, bh))

def draw_vector_glow(surface, start, end, color, label=""):
    """Panah Vektor Melayang"""
    pygame.draw.line(surface, color, start, end, 3)
    angle = math.atan2(start[1] - end[1], start[0] - end[0])
    arrow_size = 8
    p1 = (end[0] + arrow_size * math.cos(angle + math.pi/6),
          end[1] + arrow_size * math.sin(angle + math.pi/6))
    p2 = (end[0] + arrow_size * math.cos(angle - math.pi/6),
          end[1] + arrow_size * math.sin(angle - math.pi/6))
    pygame.draw.polygon(surface, color, [end, p1, p2])

    if label:
        lbl_surf = FONT_BODY.render(label, True, color)
        surface.blit(lbl_surf, (end[0] + 5, end[1] - 10))

# Inisialisasi Objek Mobil dengan Kecepatan Lebih Santai
player = Car("A1 Indonesia", COLOR_PLAYER, initial_r=2.5, initial_omega=1.0, is_player=True)
ai1 = Car("A1 Netherlands", COLOR_AI1, initial_r=1.9, initial_omega=1.1)
ai2 = Car("A1 Great Britain", COLOR_AI2, initial_r=2.4, initial_omega=0.95)
ai3 = Car("A1 South Africa", COLOR_AI3, initial_r=3.0, initial_omega=0.85)

all_cars = [player, ai1, ai2, ai3]

race_started = False
start_ticks = 0

# Loop Utama Game
running = True
while running:
    dt = clock.tick(60) / 1000.0

    # --- 1. KONTROL KEYBOARD (AKSELERASI DIBUAT HALUS) ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                race_started = True
                start_ticks = pygame.time.get_ticks()
            elif event.key == pygame.K_r:
                player = Car("A1 Indonesia", COLOR_PLAYER, initial_r=2.5, initial_omega=1.0, is_player=True)
                ai1 = Car("A1 Netherlands", COLOR_AI1, initial_r=1.9, initial_omega=1.1)
                ai2 = Car("A1 Great Britain", COLOR_AI2, initial_r=2.4, initial_omega=0.95)
                ai3 = Car("A1 South Africa", COLOR_AI3, initial_r=3.0, initial_omega=0.85)
                all_cars = [player, ai1, ai2, ai3]
                skid_marks.clear()
                particles.clear()
                race_started = True
                start_ticks = pygame.time.get_ticks()

    keys = pygame.key.get_pressed()
    player.is_braking = False
    if race_started and player.lap <= TOTAL_LAPS:
        # GAS (Panah Atas) -> Kecepatan Maksimum Dibatasi (2.2 rad/s)
        if keys[pygame.K_UP]:
            player.omega = min(2.2, player.omega + 0.8 * dt)
        # REM (Panah Bawah)
        if keys[pygame.K_DOWN]:
            player.omega = max(0.2, player.omega - 1.8 * dt)
            player.is_braking = True
        # BELOK DALAM (Panah Kiri)
        if keys[pygame.K_LEFT]:
            player.r = max(R_INNER_LIMIT - 0.2, player.r - 0.6 * dt)
        # BELOK LUAR (Panah Kanan)
        if keys[pygame.K_RIGHT]:
            player.r = min(R_OUTER_LIMIT + 0.2, player.r + 0.6 * dt)

    # --- 2. UPDATE FISIKA & PARTIKEL ---
    if race_started:
        for car in [ai1, ai2, ai3]:
            if car.lap <= TOTAL_LAPS:
                if car.is_slipping:
                    car.omega -= 0.6 * dt
                else:
                    car.omega = min(1.9, car.omega + random.uniform(0.05, 0.2) * dt)
                car.update_physics(dt)

        if player.lap <= TOTAL_LAPS:
            player.update_physics(dt)

    for p in particles[:]:
        p.update(dt)
        if p.lifetime <= 0: particles.remove(p)

    leaderboard = sorted(all_cars, key=lambda c: c.total_angle, reverse=True)
    player_pos = leaderboard.index(player) + 1

    # --- 3. RENDERING GRAFIK ---
    draw_circuit(screen)

    # Render Partikel
    for p in particles: p.draw(screen)

    # Render Mobil
    player_px, player_py = 0, 0
    for car in all_cars:
        px, py = car.draw(screen)
        if car.is_player: player_px, player_py = px, py

    # Render Vektor Panah Melayang (Tepat Berada di Hidung & Pusat Mobil)
    if race_started and not player.is_slipping:
        # Vektor Kecepatan Tangensial v (Hijau Neon - Menunjuk Lurus ke Depan)
        v_len = player.v * 12
        v_end = (player_px - v_len * math.sin(player.theta), player_py + v_len * math.cos(player.theta))
        draw_vector_glow(screen, (player_px, player_py), v_end, GREEN_NEON, "v")

        # Vektor Percepatan Sentripetal ac (Merah Neon - Menunjuk ke Pusat Titik)
        ac_len = min(player.ac * 8, 60)
        ac_end = (player_px - ac_len * math.cos(player.theta), player_py - ac_len * math.sin(player.theta))
        draw_vector_glow(screen, (player_px, player_py), ac_end, RED_NEON, "ac")

    # --- 4. GLASSMORPHISM HUD (DASHBOARD KANAN) ---
    panel_surf = pygame.Surface((470, HEIGHT), pygame.SRCALPHA)
    pygame.draw.rect(panel_surf, PANEL_GLASS, (0, 0, 470, HEIGHT))
    pygame.draw.line(panel_surf, PANEL_BORDER, (0, 0), (0, HEIGHT), 2)
    screen.blit(panel_surf, (680, 0))

    screen.blit(FONT_TITLE.render("DASHBOARD FISIKA A1 GRAND PRIX", True, YELLOW_NEON), (700, 15))

    # Spedometer Digital Neon
    speed_kmh = player.v * 18.0  # Skala visual spedometer km/jam
    speed_color = GREEN_NEON if speed_kmh < 40 else (YELLOW_NEON if speed_kmh < 65 else RED_NEON)
    
    card_speed = pygame.Surface((430, 80), pygame.SRCALPHA)
    pygame.draw.rect(card_speed, (30, 40, 60, 180), (0, 0, 430, 80), border_radius=8)
    pygame.draw.rect(card_speed, speed_color, (0, 0, 430, 80), 1, border_radius=8)
    screen.blit(card_speed, (700, 45))

    speed_txt = FONT_SPEED.render(f"{speed_kmh:.1f}", True, speed_color)
    screen.blit(speed_txt, (720, 55))
    screen.blit(FONT_HUD.render("KM/JAM", True, WHITE), (830, 70))
    screen.blit(FONT_BODY.render("Kecepatan Linear (v = ω × r)", True, GRAY), (720, 98))

    # Indikator Traksi & Bar Gaya Sentripetal
    grip_pct = min(1.0, player.Fc / F_MAX_GRIP)
    bar_col = RED_NEON if player.is_slipping else (YELLOW_NEON if grip_pct > 0.85 else GREEN_NEON)
    
    card_grip = pygame.Surface((430, 55), pygame.SRCALPHA)
    pygame.draw.rect(card_grip, (30, 40, 60, 180), (0, 0, 430, 55), border_radius=8)
    screen.blit(card_grip, (700, 135))

    screen.blit(FONT_BODY.render("Beban Traksi Ban (Gaya Sentripetal / F_max):", True, GRAY), (715, 142))
    pygame.draw.rect(screen, (50, 60, 80), (715, 162, 400, 14), border_radius=3)
    pygame.draw.rect(screen, bar_col, (715, 162, int(400 * grip_pct), 14), border_radius=3)

    # Tabel Data Fisika
    card_data = pygame.Surface((430, 240), pygame.SRCALPHA)
    pygame.draw.rect(card_data, (30, 40, 60, 180), (0, 0, 430, 240), border_radius=8)
    screen.blit(card_data, (700, 200))

    screen.blit(FONT_HUD.render("DATA BESARAN FISIKA (SI)", True, CYAN_GLOW), (715, 210))
    telemetry_data = [
        ("Massa Mobil (m)", f"{MASS:.0f} kg"),
        ("Jari-jari Tikungan (r)", f"{player.r:.2f} m"),
        ("Kecepatan Sudut (ω)", f"{player.omega:.2f} rad/s"),
        ("Percepatan Sentripetal (a_c)", f"{player.ac:.2f} m/s²"),
        ("Gaya Sentripetal (F_c)", f"{player.Fc:.0f} N"),
        ("Batas Gesek Maks (F_max)", f"{F_MAX_GRIP:.0f} N"),
    ]

    sy = 235
    for lbl, val in telemetry_data:
        screen.blit(FONT_BODY.render(f"{lbl}:", True, GRAY), (715, sy))
        screen.blit(FONT_HUD.render(val, True, WHITE), (960, sy))
        sy += 31

    # Status Balapan
    card_race = pygame.Surface((430, 85), pygame.SRCALPHA)
    pygame.draw.rect(card_race, (30, 40, 60, 180), (0, 0, 430, 85), border_radius=8)
    screen.blit(card_race, (700, 450))

    c_time = (pygame.time.get_ticks() - start_ticks) / 1000.0 if race_started else 0.0
    screen.blit(FONT_BIG.render(f"POSISI: P{player_pos}", True, GOLD), (715, 460))
    screen.blit(FONT_HUD.render(f"LAP: {min(player.lap, TOTAL_LAPS)} / {TOTAL_LAPS}", True, WHITE), (920, 465))
    screen.blit(FONT_HUD.render(f"WAKTU: {c_time:.2f} s", True, WHITE), (920, 495))

    # Panduan Kontrol
    card_ctrl = pygame.Surface((430, 140), pygame.SRCALPHA)
    pygame.draw.rect(card_ctrl, (30, 40, 60, 180), (0, 0, 430, 140), border_radius=8)
    screen.blit(card_ctrl, (700, 545))

    screen.blit(FONT_HUD.render("PANDUAN KONTROL DRIVER:", True, YELLOW_NEON), (715, 553))
    ctrls = [
        "Panah ATAS    : GAS (Tambah Kecepatan Linear v)",
        "Panah BAWAH   : REM (Kurangi Kecepatan Saat Tikungan)",
        "Panah KIRI    : BELOK DALAM (Kecilkan Jari-Jari r)",
        "Panah KANAN   : BELOK LUAR (Besarkan Jari-Jari r)",
        "SPASI / R     : Start Balapan / Reset"
    ]
    for i, c in enumerate(ctrls):
        screen.blit(FONT_BODY.render(c, True, WHITE), (715, 575 + (i * 19)))

    # Banner Overlay Start / Finish
    if not race_started:
        box = pygame.Surface((460, 110), pygame.SRCALPHA)
        pygame.draw.rect(box, (15, 22, 35, 230), (0, 0, 460, 110), border_radius=12)
        pygame.draw.rect(box, YELLOW_NEON, (0, 0, 460, 110), 2, border_radius=12)
        screen.blit(box, (100, 290))
        screen.blit(FONT_BIG.render("TEKAN SPASI UNTUK START!", True, YELLOW_NEON), (130, 310))
        screen.blit(FONT_BODY.render("Gunakan Panah Keyboard untuk Mengendalikan Mobil", True, WHITE), (115, 355))
    elif player.lap > TOTAL_LAPS:
        box = pygame.Surface((460, 110), pygame.SRCALPHA)
        pygame.draw.rect(box, (15, 22, 35, 230), (0, 0, 460, 110), border_radius=12)
        pygame.draw.rect(box, GOLD, (0, 0, 460, 110), 3, border_radius=12)
        screen.blit(box, (100, 290))
        screen.blit(FONT_BIG.render(f"FINISH! Posisi Akhir: P{player_pos}", True, GOLD), (130, 310))
        screen.blit(FONT_BODY.render("Tekan 'R' untuk Memulai Balapan Lagi", True, WHITE), (170, 355))

    pygame.display.flip()

pygame.quit()
sys.exit()