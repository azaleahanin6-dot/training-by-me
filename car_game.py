import pygame
import sys
import random
import math

# Inisialisasi Pygame
pygame.init()
WIDTH, HEIGHT = 900, 500
WORLD_WIDTH = 6000  
FINISH_X = 5300     

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game Fisika Mobil - Lalu Lintas Pintar & View Luas")
clock = pygame.time.Clock()

# --- KONSTANTA FISIKA ---
MASSA_MOBIL = 1000.0      
GRAVITASI = 9.81          
GAYA_NORMAL = MASSA_MOBIL * GRAVITASI  

SURFACES = {
    "1: Aspal Kering": 0.50,
    "2: Aspal Basah": 0.25,
    "3: Jalan Es/Licin": 0.05
}
surface_key = "1: Aspal Kering"
mu_k = SURFACES[surface_key]

GAYA_GAS_MAX = 35000.0    
GAYA_REM_MAX = 45000.0    

# Konfigurasi 3 Jalur Jalan (Lanes)
LANE_Y = [295, 345, 395]  
player_lane = 1
player_y = float(LANE_Y[player_lane])

pos_x = 50.0
vel_x = 0.0
acc_x = 0.0
pitch_angle = 0.0

# Generasi Lalu Lintas
def generate_traffic():
    traffic = []
    colors = [
        (50, 120, 220), (220, 150, 30), (150, 50, 180), 
        (30, 180, 180), (200, 70, 70), (100, 100, 100),
        (210, 210, 50), (40, 160, 80)
    ]
    
    for x_pos in range(400, WORLD_WIDTH - 400, 160):
        if random.random() < 0.7:  
            lane = random.choice([0, 1, 2])
            traffic.append({
                "x": float(x_pos),
                "lane": lane,
                "y": float(LANE_Y[lane]),
                "base_vel": float(random.uniform(7.0, 18.0)),
                "vel": 10.0,
                "color": random.choice(colors),
                "width": 80,
                "phase": random.uniform(0, 10),
                "cooldown": random.uniform(0, 2.0)
            })
    return traffic

traffic_cars = generate_traffic()

# Perkotaan Latar Gedung
BUILDINGS = []
bx = 0
while bx < WORLD_WIDTH + 1000:
    bw = random.randint(60, 120)
    bh = random.randint(110, 210)
    bcolor = (random.randint(20, 50), random.randint(25, 55), random.randint(40, 70))
    BUILDINGS.append((bx, bw, bh, bcolor))
    bx += bw + random.randint(5, 20)

# FONT DIPERKECIL UNTUK MENGHEMAT RUANG VISUAL
font_title = pygame.font.SysFont("Arial", 13, bold=True)
font_hud = pygame.font.SysFont("Consolas", 11)
font_screen = pygame.font.SysFont("Arial", 32, bold=True)

def draw_vector(screen, color, start_pos, length):
    if abs(length) > 2:
        end_pos = (start_pos[0] + length, start_pos[1])
        pygame.draw.line(screen, color, start_pos, end_pos, 3)
        direction = 1 if length > 0 else -1
        pygame.draw.polygon(screen, color, [
            end_pos,
            (end_pos[0] - 6 * direction, end_pos[1] - 4),
            (end_pos[0] - 6 * direction, end_pos[1] + 4)
        ])

status_game = "Salip mobil lain! Panah Kanan (Gas), Panah Kiri (Rem), Atas/Bawah (Ganti Jalur)"
game_over = False
win = False
time_elapsed = 0.0

running = True
while running:
    dt = clock.tick(60) / 1000.0
    time_elapsed += dt

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if not game_over:
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    if player_lane > 0:
                        player_lane -= 1
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    if player_lane < 2:
                        player_lane += 1

            if event.key == pygame.K_1:
                surface_key = "1: Aspal Kering"
                mu_k = SURFACES[surface_key]
            elif event.key == pygame.K_2:
                surface_key = "2: Aspal Basah"
                mu_k = SURFACES[surface_key]
            elif event.key == pygame.K_3:
                surface_key = "3: Jalan Es/Licin"
                mu_k = SURFACES[surface_key]
            elif event.key == pygame.K_r:
                pos_x = 50.0
                vel_x = 0.0
                acc_x = 0.0
                pitch_angle = 0.0
                player_lane = 1
                player_y = float(LANE_Y[player_lane])
                traffic_cars = generate_traffic()
                game_over = False
                win = False
                status_game = "Game di-reset. Selamat jalan!"

    keys = pygame.key.get_pressed()
    gaya_gas = 0.0
    gaya_rem = 0.0

    if not game_over:
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            gaya_gas = GAYA_GAS_MAX
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            gaya_rem = GAYA_REM_MAX

        # --- SIMULASI FISIKA HUKUM NEWTON ---
        f_gesek_dasar = mu_k * GAYA_NORMAL
        
        if vel_x > 0:
            gaya_hambat = f_gesek_dasar + gaya_rem
            gaya_total = gaya_gas - gaya_hambat
        elif vel_x < 0:
            gaya_hambat = f_gesek_dasar + gaya_rem
            gaya_total = -gaya_gas + gaya_hambat
        else:
            gaya_hambat = 0.0
            if gaya_gas > f_gesek_dasar:
                gaya_total = gaya_gas - f_gesek_dasar
            else:
                gaya_total = 0.0

        acc_x = gaya_total / MASSA_MOBIL
        vel_x += acc_x * dt

        if gaya_gas == 0 and abs(vel_x) < 0.2:
            vel_x = 0.0
            acc_x = 0.0

        pos_x += vel_x * dt * 3.5

        target_pitch = -acc_x * 0.25
        pitch_angle += (target_pitch - pitch_angle) * 0.2

        target_y = LANE_Y[player_lane]
        player_y += (target_y - player_y) * 0.2

        # --- LOGIKA LALU LINTAS PINTAR & TANGKAS (NO OVERLAPPING + PINDAH JALUR AI) ---
        for i, car in enumerate(traffic_cars):
            car["cooldown"] = max(0.0, car["cooldown"] - dt)
            
            # Cari mobil di depannya pada jalur yang sama
            car_ahead = None
            min_dist = 9999.0
            for j, other in enumerate(traffic_cars):
                if i != j and other["lane"] == car["lane"]:
                    dist = other["x"] - car["x"]
                    if 0 < dist < min_dist:
                        min_dist = dist
                        car_ahead = other

            target_vel = max(3.0, car["base_vel"] + math.sin(time_elapsed * 1.5 + car["phase"]) * 3.0)

            # Jika terhalang mobil lain di depannya
            if car_ahead and min_dist < 120:
                if car["cooldown"] <= 0:
                    # Cari jalur samping yang kosong
                    possible_lanes = []
                    if car["lane"] > 0: possible_lanes.append(car["lane"] - 1)
                    if car["lane"] < 2: possible_lanes.append(car["lane"] + 1)
                    
                    target_lane = None
                    for p_lane in possible_lanes:
                        lane_clear = True
                        for other in traffic_cars:
                            if other["lane"] == p_lane and abs(other["x"] - car["x"]) < 100:
                                lane_clear = False
                                break
                        if lane_clear:
                            target_lane = p_lane
                            break

                    if target_lane is not None:
                        car["lane"] = target_lane
                        car["cooldown"] = 2.5
                    else:
                        # Rem / Perlambat agar tidak menembus mobil depan
                        target_vel = min(target_vel, max(1.0, car_ahead["vel"] - 1.5))
                else:
                    target_vel = min(target_vel, max(1.0, car_ahead["vel"] - 1.5))
            else:
                # Pindah jalur acak sesekali layaknya pengemudi manusia
                if car["cooldown"] <= 0 and random.random() < 0.003:
                    possible_lanes = []
                    if car["lane"] > 0: possible_lanes.append(car["lane"] - 1)
                    if car["lane"] < 2: possible_lanes.append(car["lane"] + 1)
                    if possible_lanes:
                        p_lane = random.choice(possible_lanes)
                        lane_clear = all(not (o["lane"] == p_lane and abs(o["x"] - car["x"]) < 100) for o in traffic_cars)
                        if lane_clear:
                            car["lane"] = p_lane
                            car["cooldown"] = 3.5

            # Transisi kecepatan dan pergerakan
            car["vel"] += (target_vel - car["vel"]) * 0.1
            car["x"] += car["vel"] * dt * 3.5
            car["y"] += (LANE_Y[car["lane"]] - car["y"]) * 0.1

            # DETEKSI TABRAKAN PLAYER
            if abs(player_y - car["y"]) < 20 and abs(pos_x - car["x"]) < 70:
                game_over = True
                win = False
                vel_x = 0.0
                acc_x = 0.0
                pitch_angle = 15.0
                status_game = "GAME OVER! Kamu menabrak mobil lain!"

        if pos_x < 10:
            pos_x = 10
            vel_x = 0

        if pos_x >= FINISH_X and not win:
            win = True
            game_over = True
            status_game = "FINISH! Kamu Berhasil Menyelesaikan Lintasan!"

    # Kamera Bergeser
    camera_x = pos_x - 150
    if camera_x < 0:
        camera_x = 0

    # --- RENDERING GAMBAR ---
    screen.fill((160, 175, 200))
    road_top_y = 260

    # Gedung Latar
    for bx, bw, bh, bcolor in BUILDINGS:
        screen_bx = bx - camera_x
        if -bw < screen_bx < WIDTH:
            by = road_top_y - bh
            pygame.draw.rect(screen, bcolor, (screen_bx, by, bw, bh))
            for wx in range(int(screen_bx) + 8, int(screen_bx) + bw - 10, 15):
                for wy in range(by + 15, road_top_y - 20, 25):
                    window_color = (240, 220, 130) if (wx + wy) % 7 != 0 else (60, 65, 80)
                    pygame.draw.rect(screen, window_color, (wx, wy, 8, 12))

    # Trotoar & Jalan 3 Jalur
    pygame.draw.rect(screen, (200, 200, 200), (0, road_top_y - 10, WIDTH, 10))
    pygame.draw.rect(screen, (55, 60, 65), (0, road_top_y, WIDTH, 180))
    
    for lane_divider_y in [320, 370]:
        for dash_x in range(0, WORLD_WIDTH, 50):
            screen_dash_x = dash_x - camera_x
            if -50 < screen_dash_x < WIDTH:
                pygame.draw.line(screen, (240, 240, 240), (screen_dash_x, lane_divider_y), (screen_dash_x + 25, lane_divider_y), 3)

    # Garis Finish Papan Catur
    finish_screen_x = FINISH_X - camera_x
    if -100 < finish_screen_x < WIDTH:
        square_size = 15
        for row in range(0, 180 // square_size):
            for col in range(3):
                color = (255, 255, 255) if (row + col) % 2 == 0 else (0, 0, 0)
                pygame.draw.rect(screen, color, (finish_screen_x + col * square_size, road_top_y + row * square_size, square_size, square_size))
        
        banner_text = font_title.render("FINISH LINE", True, (255, 215, 0))
        screen.blit(banner_text, (finish_screen_x - 10, road_top_y - 25))

    # Render Lalu Lintas
    for car in traffic_cars:
        car_screen_x = car["x"] - camera_x
        if -100 < car_screen_x < WIDTH:
            car_draw_y = car["y"] - 20
            pygame.draw.circle(screen, (20, 20, 20), (int(car_screen_x) + 18, int(car_draw_y) + 30), 8)
            pygame.draw.circle(screen, (20, 20, 20), (int(car_screen_x) + 62, int(car_draw_y) + 30), 8)
            pygame.draw.rect(screen, car["color"], (car_screen_x, car_draw_y + 10, car["width"], 20), border_radius=4)
            pygame.draw.rect(screen, (40, 40, 40), (car_screen_x + 15, car_draw_y, 45, 12), border_radius=3)

    # Render Mobil Player
    car_width = 80
    player_screen_x = pos_x - camera_x
    player_draw_y = player_y - 20
    
    pygame.draw.circle(screen, (20, 20, 20), (int(player_screen_x) + 18, int(player_draw_y) + 30), 8)
    pygame.draw.circle(screen, (20, 20, 20), (int(player_screen_x) + 62, int(player_draw_y) + 30), 8)

    car_surface = pygame.Surface((car_width, 35), pygame.SRCALPHA)
    car_color = (220, 40, 40) if not (game_over and not win) else (120, 30, 30)
    pygame.draw.rect(car_surface, car_color, (0, 10, car_width, 20), border_radius=4)
    pygame.draw.rect(car_surface, (170, 20, 20), (15, 0, 45, 12), border_radius=3)

    rotated_car = pygame.transform.rotate(car_surface, pitch_angle)
    rotated_rect = rotated_car.get_rect(center=(int(player_screen_x) + car_width // 2, int(player_draw_y) + 15))
    screen.blit(rotated_car, rotated_rect.topleft)

    # Vektor Gaya Real-Time
    center_car_x = int(player_screen_x) + car_width // 2
    center_car_y = int(player_draw_y) + 15
    if gaya_gas > 0 and not game_over:
        draw_vector(screen, (0, 200, 0), (center_car_x, center_car_y), int(gaya_gas / 250))
    if (abs(vel_x) > 0.1 or gaya_rem > 0) and not game_over:
        draw_vector(screen, (230, 0, 0), (center_car_x, center_car_y), -int((f_gesek_dasar + gaya_rem) / 250))

    # --- DASHBOARD COMPACT HUD (UKURAN LEBIH KECIL & MINIMALIS) ---
    pygame.draw.rect(screen, (255, 255, 255), (10, 8, 420, 118), border_radius=6)
    pygame.draw.rect(screen, (180, 180, 180), (10, 8, 420, 118), 2, border_radius=6)

    kmh = abs(vel_x * 3.6)
    t1 = font_title.render("DASHBOARD FISIKA MOBIL", True, (0, 50, 100))
    t2 = font_hud.render(f"Kecepatan (v)   : {vel_x:6.2f} m/s ({kmh:5.1f} km/h)", True, (0, 0, 0))
    t3 = font_hud.render(f"Percepatan (a)  : {acc_x:6.2f} m/s^2", True, (0, 0, 0))
    t4 = font_hud.render(f"Posisi Lintasan : {pos_x:.0f} / {FINISH_X} m | Jalur: {player_lane + 1}", True, (0, 0, 0))
    t5 = font_hud.render(f"Kondisi Jalan   : {surface_key} (mu_k = {mu_k})", True, (0, 100, 200))
    t6 = font_hud.render(f"Status Fisika   : Hukum I & II Newton", True, (200, 50, 0))

    screen.blit(t1, (18, 12))
    screen.blit(t2, (18, 28))
    screen.blit(t3, (18, 43))
    screen.blit(t4, (18, 58))
    screen.blit(t5, (18, 73))
    screen.blit(t6, (18, 88))

    pygame.draw.rect(screen, (240, 248, 255), (440, 8, 450, 118), border_radius=6)
    pygame.draw.rect(screen, (180, 200, 220), (440, 8, 450, 118), 2, border_radius=6)
    
    c1 = font_title.render("KONTROL GAME", True, (0, 50, 100))
    c2 = font_hud.render("[PANAH KANAN / D]   : INJAK GAS", True, (0, 0, 0))
    c3 = font_hud.render("[PANAH KIRI  / A]   : REM MENDADAK", True, (0, 0, 0))
    c4 = font_hud.render("[PANAH ATAS / BAWAH]: PINDAH JALUR", True, (0, 0, 0))
    c5 = font_hud.render("[1, 2, 3] / [R]     : Opsi Jalan / Reset", True, (0, 0, 0))

    screen.blit(c1, (448, 12))
    screen.blit(c2, (448, 28))
    screen.blit(c3, (448, 43))
    screen.blit(c4, (448, 58))
    screen.blit(c5, (448, 73))

    msg = font_hud.render(status_game, True, (180, 40, 40) if game_over and not win else (20, 120, 20))
    screen.blit(msg, (18, 103))

    # Layar Akhir
    if game_over:
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        screen.blit(overlay, (0, 0))
        
        if win:
            main_text = font_screen.render("SELAMAT! KAMU MENCAPAI FINISH!", True, (255, 215, 0))
        else:
            main_text = font_screen.render("GAME OVER! KAMU MENABRAK MOBIL!", True, (230, 50, 50))

        sub_text = font_hud.render("Tekan [R] untuk mencoba lagi", True, (255, 255, 255))
        screen.blit(main_text, (WIDTH // 2 - main_text.get_width() // 2, HEIGHT // 2 - 30))
        screen.blit(sub_text, (WIDTH // 2 - sub_text.get_width() // 2, HEIGHT // 2 + 20))

    pygame.display.flip()

pygame.quit()
sys.exit()