import cv2
import pygame
import mediapipe as mp
import random

# 1. Inisialisasi Pygame & Layar
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Car Game - Traffic Moving")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 28)
font_big = pygame.font.SysFont(None, 54)

# 2. Setup MediaPipe & Webcam
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
cap = cv2.VideoCapture(0)

# 3. Parameter Fisika Mobil Utama
m = 1000.0
g = 9.81
mu_k = 0.50
F_gas_max = 45000.0
F_rem_max = 60000.0
F_gesek = mu_k * m * g

# 4. Fungsi Reset Game
def reset_game():
    global pos_x, vel_x, acc_x, current_lane, won, game_over, traffic_cars
    pos_x = 0.0
    vel_x = 0.0
    acc_x = 0.0
    current_lane = 1
    won = False
    game_over = False

    # Buat mobil-mobil NPC dengan KECEPATAN (SPEED) masing-masing
    traffic_cars = []
    for i in range(25):
        npc_x = random.randint(300, int(target_finish - 100))
        npc_lane = random.randint(0, 2)
        # Kecepatan acak mobil lain (sekitar 50 - 110 km/jam dalam m/s)
        npc_speed = random.uniform(15.0, 30.0) 
        npc_color = (random.randint(50, 220), random.randint(50, 220), random.randint(50, 220))
        traffic_cars.append({
            "x": npc_x,
            "lane": npc_lane,
            "speed": npc_speed,
            "color": npc_color
        })

# Inisialisasi Variabel Awal
target_finish = 5300.0
lane_y_positions = [150, 300, 450]
PLAYER_SCREEN_X = 100
running = True
traffic_cars = []
pos_x = vel_x = acc_x = 0.0
current_lane = 1
won = game_over = False

reset_game()

# 5. Loop Utama
while running:
    dt = clock.tick(60) / 1000.0  # Delta time per frame

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                reset_game()

    # Baca frame dari webcam
    ret, frame = cap.read()
    F_gas = 0.0
    F_rem = 0.0
    status_sensor = "NETRAL"

    if ret:
        frame = cv2.flip(frame, 1)
        h, w, _ = frame.shape
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb_frame)

        # Gambar Garis Panduan Sensor di Kamera
        cv2.line(frame, (int(w * 0.45), 0), (int(w * 0.45), h), (255, 255, 0), 2)
        cv2.line(frame, (int(w * 0.55), 0), (int(w * 0.55), h), (255, 255, 0), 2)

        # Deteksi Gerakan Tangan
        if results.multi_hand_landmarks and not game_over and not won:
            for hand_landmarks in results.multi_hand_landmarks:
                cx = hand_landmarks.landmark[8].x
                cy = hand_landmarks.landmark[8].y

                # A. KONTROL JALUR (Y)
                if cy < 0.35:
                    current_lane = 0
                elif cy < 0.65:
                    current_lane = 1
                else:
                    current_lane = 2

                # B. KONTROL GAS & REM (X)
                if cx > 0.55:
                    F_gas = F_gas_max
                    status_sensor = "GAS!"
                elif cx < 0.45:
                    F_rem = F_rem_max
                    status_sensor = "REM!"

        cv2.putText(frame, f"SENSOR: {status_sensor}", (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.imshow("Webcam Controller", frame)

        if cv2.waitKey(1) & 0xFF == 27:
            break

    # --- HITUNG FISIKA PERGERAKAN ---
    if not game_over and not won:
        # 1. Pergerakan Mobil Utama
        f_gesek_aktuil = F_gesek if vel_x > 0 else 0.0
        F_net = F_gas - F_rem - f_gesek_aktuil
        
        acc_x = F_net / m
        vel_x += acc_x * dt
        if vel_x < 0:
            vel_x = 0.0

        pos_x += vel_x * dt

        # 2. PERGERAKAN MOBIL-MOBIL NPC (LALU LINTAS BERJALAN)
        for npc in traffic_cars:
            npc["x"] += npc["speed"] * dt

        # Cek Garis Finish
        if pos_x >= target_finish:
            won = True

        # 3. DETEKSI TABRAKAN
        for npc in traffic_cars:
            if npc["lane"] == current_lane:
                if abs(npc["x"] - pos_x) < 45:
                    game_over = True
                    vel_x = 0.0

    # --- GAMBAR LAYAR PYGAME ---
    screen.fill((30, 30, 30))

    # 1. Garis Jalanan Bergerak
    offset_x = int(pos_x) % 80
    for lane_y in lane_y_positions:
        pygame.draw.line(screen, (80, 80, 80), (0, lane_y + 40), (WIDTH, lane_y + 40), 2)
        for x_dash in range(-offset_x, WIDTH, 80):
            pygame.draw.line(screen, (200, 200, 200), (x_dash, lane_y + 20), (x_dash + 40, lane_y + 20), 2)

    # 2. Gambar Mobil NPC yang Bergerak
    for npc in traffic_cars:
        npc_screen_x = npc["x"] - pos_x + PLAYER_SCREEN_X
        npc_screen_y = lane_y_positions[npc["lane"]]
        if -100 < npc_screen_x < WIDTH + 100:
            pygame.draw.rect(screen, npc["color"], (int(npc_screen_x), npc_screen_y, 60, 30))

    # 3. Garis Finish
    finish_screen_x = target_finish - pos_x + PLAYER_SCREEN_X
    if -50 < finish_screen_x < WIDTH + 50:
        pygame.draw.rect(screen, (255, 255, 255), (int(finish_screen_x), 100, 20, 400))

    # 4. Mobil Player (Merah)
    player_y = lane_y_positions[current_lane]
    player_color = (150, 0, 0) if game_over else (255, 50, 50)
    pygame.draw.rect(screen, player_color, (PLAYER_SCREEN_X, player_y, 60, 30))

    # 5. Teks UI Info
    text_pos = font.render(f"Posisi: {pos_x:.1f} m / {target_finish:.0f} m", True, (255, 255, 255))
    text_vel = font.render(f"Kecepatan: {vel_x * 3.6:.1f} km/jam", True, (255, 255, 255))
    text_acc = font.render(f"Percepatan: {acc_x:.2f} m/s^2", True, (255, 255, 255))
    text_lane = font.render(f"Jalur: {current_lane + 1}", True, (255, 255, 255))

    screen.blit(text_pos, (20, 20))
    screen.blit(text_vel, (20, 50))
    screen.blit(text_acc, (20, 80))
    screen.blit(text_lane, (20, 110))

    # 6. Teks Game Over & Win
    if game_over:
        txt_go = font_big.render("GAME OVER!", True, (255, 50, 50))
        txt_sub = font.render("Menabrak Mobil Lain! Tekan 'R' untuk Restart", True, (255, 255, 255))
        screen.blit(txt_go, (WIDTH // 2 - 130, HEIGHT // 2 - 40))
        screen.blit(txt_sub, (WIDTH // 2 - 180, HEIGHT // 2 + 20))

    elif won:
        txt_win = font_big.render("GARIS FINISH TERCAPAI!", True, (0, 255, 0))
        txt_sub = font.render("Selamat! Tekan 'R' untuk Main Lagi", True, (255, 255, 255))
        screen.blit(txt_win, (WIDTH // 2 - 200, HEIGHT // 2 - 40))
        screen.blit(txt_sub, (WIDTH // 2 - 150, HEIGHT // 2 + 20))

    pygame.display.flip()

cap.release()
cv2.destroyAllWindows()
pygame.quit()