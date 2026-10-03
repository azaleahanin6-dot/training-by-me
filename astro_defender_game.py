import pygame
import math
import sys
import random

# --------------------------------------------------------------------
# 1. INISIALISASI GAME & SYNTHAUDIO
# --------------------------------------------------------------------
pygame.init()
pygame.font.init()

try:
    pygame.mixer.init(22050, -8, 1, 512)
    HAS_SOUND = True
except Exception:
    HAS_SOUND = False

def create_sound(f_start, f_end, dur, vol=0.2):
    if not HAS_SOUND: return None
    sr = 22050
    n = int(sr * dur)
    buf = bytearray()
    for i in range(n):
        t = i / sr
        freq = f_start + (f_end - f_start) * (i / n)
        val = int(128 + 127 * vol * math.sin(2 * math.pi * freq * t))
        buf.append(max(0, min(255, val)))
    try:
        return pygame.mixer.Sound(buffer=bytes(buf))
    except Exception:
        return None

snd_laser   = create_sound(900, 400, 0.05, 0.15)
snd_boom    = create_sound(200, 30, 0.2, 0.3)
snd_powerup = create_sound(400, 900, 0.15, 0.25)
snd_hit     = create_sound(120, 80, 0.04, 0.2)
snd_lvlup   = create_sound(300, 1200, 0.3, 0.3)

WIDTH, HEIGHT = 900, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("⚡ ASTRO DEFENDER: LEVEL UP & VICTORY EDITION")
clock = pygame.time.Clock()

# Palet Warna
BG_COLOR  = (6, 8, 20)
WHITE     = (255, 255, 255)
CYAN      = (0, 240, 255)
YELLOW    = (255, 220, 40)
RED       = (255, 60, 80)
GREEN     = (50, 255, 120)
PURPLE    = (180, 70, 255)
ORANGE    = (255, 140, 30)
GRAY      = (120, 130, 150)
NEBULA_P  = (50, 15, 70)
NEBULA_B  = (10, 35, 75)

font_ui    = pygame.font.SysFont("arial", 13, bold=True)
font_title = pygame.font.SysFont("impact", 28)
font_huge  = pygame.font.SysFont("impact", 56)

# --------------------------------------------------------------------
# 2. SISTEM PARTIKEL & EFEK VISUAL
# --------------------------------------------------------------------
screen_shake = 0

class Particle:
    def __init__(self, x, y, color, size_range=(2, 5), speed=3):
        self.x = x
        self.y = y
        self.color = color
        ang = random.uniform(0, math.pi * 2)
        sp = random.uniform(0.5, speed)
        self.vx = math.cos(ang) * sp
        self.vy = math.sin(ang) * sp
        self.life = random.randint(15, 30)
        self.max_life = self.life
        self.size = random.randint(*size_range)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.life -= 1

    def draw(self, surface):
        if self.life <= 0: return
        alpha = int(255 * (self.life / self.max_life))
        sz = max(1, int(self.size * (self.life / self.max_life)))
        s = pygame.Surface((sz*2, sz*2), pygame.SRCALPHA)
        pygame.draw.circle(s, (*self.color[:3], alpha), (sz, sz), sz)
        surface.blit(s, (int(self.x) - sz, int(self.y) - sz))

class FloatingText:
    def __init__(self, text, x, y, color, size="small"):
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.life = 50
        self.font = font_title if size == "large" else font_ui

    def update(self):
        self.y -= 1.2
        self.life -= 1

    def draw(self, surface):
        if self.life <= 0: return
        txt = self.font.render(self.text, True, self.color)
        surface.blit(txt, (int(self.x) - txt.get_width()//2, int(self.y)))

class ShootingStar:
    def __init__(self):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(-200, 0)
        self.vx = random.uniform(-4, -2)
        self.vy = random.uniform(8, 14)

    def update(self):
        self.x += self.vx
        self.y += self.vy

    def draw(self, surface):
        pygame.draw.line(surface, CYAN, (self.x, self.y), (self.x - self.vx*2, self.y - self.vy*2), 2)

particles = []
floating_texts = []
shooting_stars = [ShootingStar() for _ in range(3)]

def add_explosion(x, y, color, count=22):
    global screen_shake
    screen_shake = max(screen_shake, 10)
    for _ in range(count):
        particles.append(Particle(x, y, color, (3, 7), 6))

# --------------------------------------------------------------------
# 3. ENTITAS GAME
# --------------------------------------------------------------------
class Asteroid:
    def __init__(self, x=None, y=None, size=3):
        self.size = size
        self.radius = size * 12
        self.x = x if x is not None else random.randint(30, WIDTH - 30)
        self.y = y if y is not None else -40
        self.vx = random.uniform(-1.0, 1.0)
        self.vy = random.uniform(1.2, 2.5)
        self.hp = size * 3
        self.angle = 0
        self.rot_speed = random.uniform(-2, 2)
        
        self.points = []
        num_pts = random.randint(7, 10)
        for i in range(num_pts):
            a = (i / num_pts) * math.pi * 2
            r = self.radius * random.uniform(0.75, 1.2)
            self.points.append((math.cos(a)*r, math.sin(a)*r))

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.angle += self.rot_speed

    def draw(self, surface):
        rad = math.radians(self.angle)
        transformed = []
        for px, py in self.points:
            rx = px * math.cos(rad) - py * math.sin(rad) + self.x
            ry = px * math.sin(rad) + py * math.cos(rad) + self.y
            transformed.append((rx, ry))
        pygame.draw.polygon(surface, GRAY, transformed)
        pygame.draw.polygon(surface, (160, 170, 190), transformed, 2)

class Player:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = HEIGHT - 100
        self.speed = 6.8
        self.hp = 100
        self.max_hp = 100
        self.shield = 50
        self.max_shield = 50
        self.shoot_cooldown = 0
        self.triple_shot_timer = 0
        self.drone_timer = 0
        self.lvl_effect_timer = 0
        self.bombs = 1
        self.radius = 16

    def move(self, dx, dy):
        self.x = max(20, min(WIDTH - 20, self.x + dx * self.speed))
        self.y = max(20, min(HEIGHT - 20, self.y + dy * self.speed))

    def update(self):
        if self.shoot_cooldown > 0: self.shoot_cooldown -= 1
        if self.triple_shot_timer > 0: self.triple_shot_timer -= 1
        if self.drone_timer > 0: self.drone_timer -= 1
        if self.lvl_effect_timer > 0: self.lvl_effect_timer -= 1
        if self.shield < self.max_shield:
            self.shield = min(self.max_shield, self.shield + 0.05)

    def draw(self, surface):
        px, py = int(self.x), int(self.y)
        
        # Animasi Aura Gelombang NAIK LEVEL
        if self.lvl_effect_timer > 0:
            rad = 30 + (60 - self.lvl_effect_timer)
            pygame.draw.circle(surface, GREEN, (px, py), rad, 3)
            pygame.draw.circle(surface, YELLOW, (px, py), rad + 8, 1)

        # Shield Glow
        if self.shield > 5:
            pygame.draw.circle(surface, (0, 220, 255, 70), (px, py), self.radius + 9, 2)

        # Body Pesawat Utama
        p1 = (px, py - 18)
        p2 = (px - 16, py + 14)
        p3 = (px, py + 8)
        p4 = (px + 16, py + 14)
        pygame.draw.polygon(surface, CYAN, [p1, p2, p3, p4])
        pygame.draw.polygon(surface, WHITE, [p1, (px-8, py+6), p3, (px+8, py+6)])

        # Support Drone Companion
        if self.drone_timer > 0:
            for side in [-28, 28]:
                dx = px + side
                dy = py + 8
                pygame.draw.circle(surface, GREEN, (dx, dy), 6)
                pygame.draw.circle(surface, WHITE, (dx, dy), 3)

        if random.random() < 0.7:
            particles.append(Particle(px, py + 14, YELLOW, (2, 4), 2))

class Bullet:
    def __init__(self, x, y, vx, vy, is_player=True, color=CYAN):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.is_player = is_player
        self.color = color
        self.radius = 4

    def update(self):
        self.x += self.vx
        self.y += self.vy

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)

class Enemy:
    def __init__(self, etype="scout"):
        self.type = etype
        self.x = random.randint(40, WIDTH - 40)
        self.y = -30

        if etype == "scout":
            self.hp = 2
            self.speed = random.uniform(2.5, 4.0)
            self.color = ORANGE
            self.radius = 14
            self.score_val = 100
        elif etype == "kamikaze":
            self.hp = 1
            self.speed = 5.5
            self.color = RED
            self.radius = 12
            self.score_val = 150
        elif etype == "shooter":
            self.hp = 5
            self.speed = 1.8
            self.color = PURPLE
            self.radius = 18
            self.shoot_cd = random.randint(40, 90)
            self.score_val = 250
        elif etype == "destroyer":
            self.hp = 12
            self.speed = 1.2
            self.color = (255, 80, 0)
            self.radius = 26
            self.shoot_cd = 45
            self.score_val = 500
        elif etype == "boss":
            self.x = WIDTH // 2
            self.hp = 120
            self.max_hp = 120
            self.speed = 1.0
            self.color = RED
            self.radius = 42
            self.shoot_cd = 25
            self.vx = 3.0
            self.score_val = 3000

    def update(self, bullets, player_pos):
        if self.type == "boss":
            self.x += self.vx
            if self.x < 70 or self.x > WIDTH - 70:
                self.vx *= -1
            if self.y < 110: self.y += self.speed

            self.shoot_cd -= 1
            if self.shoot_cd <= 0:
                self.shoot_cd = 30
                for ang in [-0.4, -0.2, 0, 0.2, 0.4]:
                    bullets.append(Bullet(self.x, self.y + 30, math.sin(ang)*6, math.cos(ang)*6, False, RED))
                if snd_laser: snd_laser.play()

        elif self.type == "kamikaze":
            dx = player_pos[0] - self.x
            dy = player_pos[1] - self.y
            dist = max(1, math.hypot(dx, dy))
            self.x += (dx / dist) * self.speed
            self.y += (dy / dist) * self.speed

        else:
            self.y += self.speed
            if self.type == "shooter":
                self.shoot_cd -= 1
                if self.shoot_cd <= 0:
                    self.shoot_cd = 70
                    bullets.append(Bullet(self.x, self.y + 15, 0, 5, False, RED))
            elif self.type == "destroyer":
                self.shoot_cd -= 1
                if self.shoot_cd <= 0:
                    self.shoot_cd = 50
                    bullets.append(Bullet(self.x - 12, self.y + 20, -1, 6, False, ORANGE))
                    bullets.append(Bullet(self.x + 12, self.y + 20, 1, 6, False, ORANGE))

    def draw(self, surface):
        px, py = int(self.x), int(self.y)
        if self.type == "boss":
            pygame.draw.circle(surface, self.color, (px, py), self.radius)
            pygame.draw.circle(surface, YELLOW, (px, py), self.radius - 8, 4)
            pygame.draw.rect(surface, GRAY, (px - 50, py - 58, 100, 8))
            pygame.draw.rect(surface, GREEN, (px - 50, py - 58, int(100 * (self.hp / self.max_hp)), 8))
        elif self.type == "kamikaze":
            pygame.draw.polygon(surface, RED, [(px, py+14), (px-10, py-10), (px+10, py-10)])
        elif self.type == "destroyer":
            pygame.draw.rect(surface, ORANGE, (px-22, py-14, 44, 28))
            pygame.draw.rect(surface, YELLOW, (px-12, py-6, 24, 12))
        else:
            pygame.draw.circle(surface, self.color, (px, py), self.radius)

class PowerUp:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.ptype = random.choice(["triple", "shield", "health", "bomb", "drone"])
        self.vy = 1.8
        self.radius = 12

    def update(self):
        self.y += self.vy

    def draw(self, surface):
        px, py = int(self.x), int(self.y)
        color = YELLOW if self.ptype == "triple" else (CYAN if self.ptype == "shield" else (GREEN if self.ptype in ["health", "drone"] else RED))
        pygame.draw.circle(surface, color, (px, py), self.radius)
        label = self.ptype[0].upper() if self.ptype != "drone" else "D"
        txt = font_ui.render(label, True, BG_COLOR)
        surface.blit(txt, (px - txt.get_width()//2, py - txt.get_height()//2))

# --------------------------------------------------------------------
# 4. RESET & SETUP GAMELOOP
# --------------------------------------------------------------------
player = Player()
bullets = []
enemies = []
asteroids = []
powerups = []
starfield = [[random.randint(0, WIDTH), random.randint(0, HEIGHT), random.uniform(0.5, 2.5)] for _ in range(80)]

score = 0
wave_level = 1
MAX_WAVES = 5
spawn_timer = 0
boss_spawned = False
level_clear_timer = 0  # Timer transisi animasi NAIK LEVEL
game_state = "PLAYING"

def reset_game():
    global player, bullets, enemies, asteroids, powerups, score, wave_level, spawn_timer, boss_spawned, level_clear_timer, game_state
    player = Player()
    bullets.clear()
    enemies.clear()
    asteroids.clear()
    powerups.clear()
    particles.clear()
    floating_texts.clear()
    score = 0
    wave_level = 1
    spawn_timer = 0
    boss_spawned = False
    level_clear_timer = 0
    game_state = "PLAYING"

def trigger_level_up():
    global wave_level, boss_spawned, level_clear_timer, game_state
    boss_spawned = False
    if wave_level >= MAX_WAVES:
        game_state = "VICTORY"
    else:
        level_clear_timer = 150  # ~2.5 detik animasi transisi level berhasil
        if snd_lvlup: snd_lvlup.play()
        # Bonus Pemulihan Naik Level
        player.hp = min(player.max_hp, player.hp + 40)
        player.shield = player.max_shield
        player.bombs += 1
        player.lvl_effect_timer = 60
        add_explosion(player.x, player.y, GREEN, 30)

# --------------------------------------------------------------------
# 5. UTAMA GAME LOOP
# --------------------------------------------------------------------
running = True

while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and game_state in ["GAME_OVER", "VICTORY"]:
                reset_game()
            elif event.key == pygame.K_e and game_state == "PLAYING" and player.bombs > 0 and level_clear_timer == 0:
                player.bombs -= 1
                screen_shake = 22
                for enemy in enemies[:]:
                    add_explosion(enemy.x, enemy.y, enemy.color, 16)
                    score += enemy.score_val
                    enemies.remove(enemy)
                for ast in asteroids[:]:
                    add_explosion(ast.x, ast.y, GRAY, 12)
                    asteroids.remove(ast)
                bullets = [b for b in bullets if b.is_player]
                floating_texts.append(FloatingText("NUKE CLEAR!", WIDTH//2, HEIGHT//2, RED, "large"))
                if snd_boom: snd_boom.play()

    keys = pygame.key.get_pressed()
    if game_state == "PLAYING":
        dx = (keys[pygame.K_RIGHT] or keys[pygame.K_d]) - (keys[pygame.K_LEFT] or keys[pygame.K_a])
        dy = (keys[pygame.K_DOWN] or keys[pygame.K_s]) - (keys[pygame.K_UP] or keys[pygame.K_w])
        player.move(dx, dy)

        if keys[pygame.K_SPACE] and player.shoot_cooldown == 0:
            player.shoot_cooldown = 7
            if player.triple_shot_timer > 0:
                bullets.append(Bullet(player.x, player.y - 15, 0, -12, True, YELLOW))
                bullets.append(Bullet(player.x - 10, player.y - 10, -2.5, -11, True, YELLOW))
                bullets.append(Bullet(player.x + 10, player.y - 10, 2.5, -11, True, YELLOW))
            else:
                bullets.append(Bullet(player.x, player.y - 15, 0, -12, True, CYAN))

            if player.drone_timer > 0:
                bullets.append(Bullet(player.x - 28, player.y, 0, -11, True, GREEN))
                bullets.append(Bullet(player.x + 28, player.y, 0, -11, True, GREEN))

            if snd_laser: snd_laser.play()

    # LOGIKA PERMAINAN
    if game_state == "PLAYING":
        player.update()

        # Update Starfield & Shooting Stars
        for star in starfield:
            star[1] += star[2]
            if star[1] > HEIGHT:
                star[1] = 0
                star[0] = random.randint(0, WIDTH)

        for ss in shooting_stars:
            ss.update()
            if ss.y > HEIGHT or ss.x < 0:
                ss.__init__()

        # PENANGANAN TRANSIKSI LEVEL BERHASIL / NAIK LEVEL
        if level_clear_timer > 0:
            level_clear_timer -= 1
            # Kembang api perayaan mini
            if level_clear_timer % 15 == 0:
                add_explosion(random.randint(100, WIDTH-100), random.randint(100, 300), random.choice([CYAN, GREEN, YELLOW, PURPLE]), 15)
            
            if level_clear_timer == 0:
                wave_level += 1
                floating_texts.append(FloatingText(f"WAVE {wave_level} START!", WIDTH//2, 200, YELLOW, "large"))
        else:
            # Spawning Asteroid
            if random.random() < 0.02 and len(asteroids) < 5:
                asteroids.append(Asteroid())

            # Spawning Musuh
            spawn_timer += 1
            if spawn_timer > max(20, 55 - wave_level * 6) and not boss_spawned:
                spawn_timer = 0
                rnd = random.random()
                if rnd < 0.35: etype = "scout"
                elif rnd < 0.65: etype = "kamikaze"
                elif rnd < 0.85: etype = "shooter"
                else: etype = "destroyer"
                enemies.append(Enemy(etype))

            # Pemicu BOSS Tiap Wave Clear
            if score >= wave_level * 1200 and not boss_spawned:
                boss_spawned = True
                enemies.append(Enemy("boss"))
                msg = "⚠️ ULTIMATE OVERLORD BOSS!" if wave_level == MAX_WAVES else f"⚠️ WAVE {wave_level} BOSS APPROACHING!"
                floating_texts.append(FloatingText(msg, WIDTH//2, 180, RED, "large"))

        # Update Peluru
        for b in bullets[:]:
            b.update()
            if b.y < -10 or b.y > HEIGHT + 10 or b.x < -10 or b.x > WIDTH + 10:
                bullets.remove(b)

        # Update Asteroid
        for ast in asteroids[:]:
            ast.update()
            if ast.y > HEIGHT + 40:
                asteroids.remove(ast)
                continue

            for b in bullets[:]:
                if b.is_player and math.hypot(b.x - ast.x, b.y - ast.y) < ast.radius + b.radius:
                    bullets.remove(b)
                    ast.hp -= 1
                    particles.append(Particle(ast.x, ast.y, GRAY, (2, 4), 3))
                    if ast.hp <= 0:
                        add_explosion(ast.x, ast.y, GRAY, 12)
                        score += ast.size * 50
                        if ast.size > 1:
                            asteroids.append(Asteroid(ast.x - 10, ast.y, ast.size - 1))
                            asteroids.append(Asteroid(ast.x + 10, ast.y, ast.size - 1))
                        if ast in asteroids: asteroids.remove(ast)
                        if snd_boom: snd_boom.play()
                        break

            if math.hypot(player.x - ast.x, player.y - ast.y) < player.radius + ast.radius:
                damage = ast.size * 12
                if player.shield > 0: player.shield = max(0, player.shield - damage)
                else: player.hp -= damage
                add_explosion(player.x, player.y, RED, 12)
                if ast in asteroids: asteroids.remove(ast)

        # Update Musuh
        for e in enemies[:]:
            e.update(bullets, (player.x, player.y))

            for b in bullets[:]:
                if b.is_player and math.hypot(b.x - e.x, b.y - e.y) < e.radius + b.radius:
                    bullets.remove(b)
                    e.hp -= 1
                    particles.append(Particle(e.x, e.y, e.color, (2, 4), 3))
                    if snd_hit: snd_hit.play()

                    if e.hp <= 0:
                        add_explosion(e.x, e.y, e.color)
                        score += e.score_val
                        floating_texts.append(FloatingText(f"+{e.score_val}", e.x, e.y, YELLOW))
                        
                        if random.random() < 0.25:
                            powerups.append(PowerUp(e.x, e.y))

                        # CEK BOS DIBANTAI -> PEMICU LEVEL BERHASIL / NAIK LEVEL
                        if e.type == "boss":
                            trigger_level_up()

                        if e in enemies: enemies.remove(e)
                        if snd_boom: snd_boom.play()
                        break

            if math.hypot(player.x - e.x, player.y - e.y) < player.radius + e.radius:
                damage = 35 if e.type == "boss" else 15
                if player.shield > 0: player.shield = max(0, player.shield - damage)
                else: player.hp -= damage
                add_explosion(player.x, player.y, RED, 15)
                if e.type != "boss" and e in enemies: enemies.remove(e)

        # Peluru Musuh -> Player
        for b in bullets[:]:
            if not b.is_player and math.hypot(b.x - player.x, b.y - player.y) < player.radius + b.radius:
                bullets.remove(b)
                if player.shield > 0: player.shield = max(0, player.shield - 12)
                else: player.hp -= 12
                particles.append(Particle(player.x, player.y, RED, (2, 5), 4))
                if snd_hit: snd_hit.play()

        # Collect Power-Up
        for p in powerups[:]:
            p.update()
            if math.hypot(player.x - p.x, player.y - p.y) < player.radius + p.radius:
                if p.ptype == "triple":
                    player.triple_shot_timer = 350
                    floating_texts.append(FloatingText("TRIPLE SHOT!", player.x, player.y, YELLOW))
                elif p.ptype == "shield":
                    player.shield = player.max_shield
                    floating_texts.append(FloatingText("SHIELD RECHARGED!", player.x, player.y, CYAN))
                elif p.ptype == "health":
                    player.hp = min(player.max_hp, player.hp + 35)
                    floating_texts.append(FloatingText("HP REPAIRED!", player.x, player.y, GREEN))
                elif p.ptype == "bomb":
                    player.bombs += 1
                    floating_texts.append(FloatingText("+1 NUKE BOMB!", player.x, player.y, RED))
                elif p.ptype == "drone":
                    player.drone_timer = 450
                    floating_texts.append(FloatingText("SUPPORT DRONE ACTIVE!", player.x, player.y, GREEN))

                if snd_powerup: snd_powerup.play()
                powerups.remove(p)
            elif p.y > HEIGHT + 20: powerups.remove(p)

        if player.hp <= 0:
            add_explosion(player.x, player.y, RED, 40)
            game_state = "GAME_OVER"

        for pt in particles[:]:
            pt.update()
            if pt.life <= 0: particles.remove(pt)

        for ft in floating_texts[:]:
            ft.update()
            if ft.life <= 0: floating_texts.remove(ft)

    if game_state == "VICTORY" and random.random() < 0.3:
        add_explosion(random.randint(100, WIDTH-100), random.randint(100, HEIGHT-200), random.choice([CYAN, YELLOW, GREEN, PURPLE]), 20)
        for pt in particles[:]: pt.update()

    # --------------------------------------------------------------------
    # 6. RENDERING DISPLAY & UI
    # --------------------------------------------------------------------
    shake_x = random.randint(-screen_shake, screen_shake) if screen_shake > 0 else 0
    shake_y = random.randint(-screen_shake, screen_shake) if screen_shake > 0 else 0
    if screen_shake > 0: screen_shake -= 1

    render_surf = pygame.Surface((WIDTH, HEIGHT))
    render_surf.fill(BG_COLOR)

    # Visual Awan Galaksi
    pygame.draw.circle(render_surf, NEBULA_P, (200, 180), 180)
    pygame.draw.circle(render_surf, NEBULA_B, (700, 500), 220)

    for star in starfield:
        pygame.draw.circle(render_surf, WHITE, (int(star[0]), int(star[1])), int(star[2]))
    for ss in shooting_stars: ss.draw(render_surf)

    for ast in asteroids: ast.draw(render_surf)
    for p in powerups: p.draw(render_surf)
    for b in bullets: b.draw(render_surf)
    for e in enemies: e.draw(render_surf)
    if game_state == "PLAYING": player.draw(render_surf)
    for pt in particles: pt.draw(render_surf)
    for ft in floating_texts: ft.draw(render_surf)

    screen.blit(render_surf, (shake_x, shake_y))

    # Panel HUD UI
    pygame.draw.rect(screen, (12, 18, 35), (10, 10, 330, 95))
    pygame.draw.rect(screen, CYAN, (10, 10, 330, 95), 2)

    screen.blit(font_ui.render("HP:", True, WHITE), (20, 20))
    pygame.draw.rect(screen, GRAY, (70, 22, 150, 10))
    pygame.draw.rect(screen, GREEN if player.hp > 30 else RED, (70, 22, int(150 * max(0, player.hp)/100), 10))

    screen.blit(font_ui.render("SHIELD:", True, WHITE), (20, 40))
    pygame.draw.rect(screen, GRAY, (70, 42, 150, 10))
    pygame.draw.rect(screen, CYAN, (70, 42, int(150 * max(0, player.shield)/50), 10))

    screen.blit(font_ui.render(f"SKOR: {score}  |  LEVEL: {wave_level}/{MAX_WAVES}", True, YELLOW), (20, 62))
    screen.blit(font_ui.render(f"BOMB [E]: {player.bombs} AVAILABLE", True, RED), (20, 80))

    # SPANNER ANIMASI TRANSIKSI "LEVEL BERHASIL & NAIK LEVEL!"
    if level_clear_timer > 0 and game_state == "PLAYING":
        banner_s = pygame.Surface((WIDTH, 140), pygame.SRCALPHA)
        banner_s.fill((10, 30, 50, 210))
        screen.blit(banner_s, (0, HEIGHT//2 - 70))
        pygame.draw.line(screen, GREEN, (0, HEIGHT//2 - 70), (WIDTH, HEIGHT//2 - 70), 3)
        pygame.draw.line(screen, GREEN, (0, HEIGHT//2 + 70), (WIDTH, HEIGHT//2 + 70), 3)

        t_clear = font_huge.render(f"LEVEL {wave_level} BERHASIL!", True, GREEN)
        t_next  = font_title.render(f"⭐ NAIK KE LEVEL {wave_level + 1} ⭐", True, YELLOW)
        t_bonus = font_ui.render("+ BONUS FULL SHIELD, HP REFILL & +1 BOMB!", True, CYAN)

        screen.blit(t_clear, (WIDTH//2 - t_clear.get_width()//2, HEIGHT//2 - 58))
        screen.blit(t_next,  (WIDTH//2 - t_next.get_width()//2, HEIGHT//2 + 2))
        screen.blit(t_bonus, (WIDTH//2 - t_bonus.get_width()//2, HEIGHT//2 + 38))

    # SCREEN TAMPILAN TAMAT / KEMENANGAN AKHIR (VICTORY)
    if game_state == "VICTORY":
        pygame.draw.rect(screen, (10, 25, 20), (WIDTH//2 - 270, 200, 540, 260))
        pygame.draw.rect(screen, GREEN, (WIDTH//2 - 270, 200, 540, 260), 3)

        t1 = font_huge.render("SEMUA LEVEL BERHASIL!", True, GREEN)
        t2 = font_title.render(f"🏆 SELAMAT! SKOR AKHIR: {score}", True, YELLOW)
        t3 = font_ui.render("Kamu telah membebaskan seluruh galaksi!", True, WHITE)
        t4 = font_ui.render("Tekan [R] Untuk Main Lagi dari Level 1", True, CYAN)

        screen.blit(t1, (WIDTH//2 - t1.get_width()//2, 220))
        screen.blit(t2, (WIDTH//2 - t2.get_width()//2, 290))
        screen.blit(t3, (WIDTH//2 - t3.get_width()//2, 340))
        screen.blit(t4, (WIDTH//2 - t4.get_width()//2, 390))

    # SCREEN TAMPILAN GAME OVER
    elif game_state == "GAME_OVER":
        pygame.draw.rect(screen, (25, 10, 15), (WIDTH//2 - 250, 220, 500, 220))
        pygame.draw.rect(screen, RED, (WIDTH//2 - 250, 220, 500, 220), 3)

        t1 = font_huge.render("GAME OVER", True, RED)
        t2 = font_title.render(f"SKOR AKHIR: {score} (LEVEL {wave_level})", True, WHITE)
        t3 = font_ui.render("Tekan [R] Untuk Ulangi Misi", True, GREEN)

        screen.blit(t1, (WIDTH//2 - t1.get_width()//2, 240))
        screen.blit(t2, (WIDTH//2 - t2.get_width()//2, 320))
        screen.blit(t3, (WIDTH//2 - t3.get_width()//2, 380))

    pygame.display.flip()

pygame.quit()
sys.exit()