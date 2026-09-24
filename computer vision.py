import cv2
import numpy as np
import pygame
import sys
import mediapipe as mp

# Inisialisasi Pygame
pygame.init()
WIDTH, HEIGHT = 1000, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simulasi Fisika Hukum Newton - Kontrol Computer Vision")
clock = pygame.time.Clock()

# Parameter Fisika
m = 1000.0          
g = 9.81            
mu_k = 0.50         
F_gas_max = 35000.0 
F_rem_max = 45000.0 
F_gesek = mu_k * m * g  

# Variabel Mobil
pos_x = 0.0          
vel_x = 0.0          
acc_x = 0.0          
current_lane = 1     
target_finish = 5300.0 
# Setup MediaPipe Hands untuk Computer Vision
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils
cap = cv2.VideoCapture(0)
lane_y_positions = [150, 300, 450]
running = True
won = False

while running:
    dt = clock.tick(60) / 1000.0  
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Processing Computer Vision dengan OpenCV dan MediaPipe
    ret, frame = cap.read()
    if not ret:
        break
    
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)
    
    F_gas = 0.0
    F_rem = 0.0
    
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            
            index_y = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y
            index_x = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x
            
            # Navigasi Lateral (Perpindahan Jalur)
            if index_y < 0.35:
                current_lane = 0  
            elif index_y > 0.65:
                current_lane = 2  
            else:
                current_lane = 1  
            
            # Navigasi Longitudinal (Gaya Gas dan Rem)
            if index_x > 0.6:
                F_gas = F_gas_max  
            elif index_x < 0.4:
                F_rem = F_rem_max  
    
    cv2.imshow("Umpan Kamera Kontrol Gestur", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    # Perhitungan Dinamika Fisika Hukum II Newton
    if not won:
        if vel_x > 0:
            F_net = F_gas - F_rem - F_gesek
        else:
            F_net = max(0.0, F_gas - F_rem)
            
        acc_x = F_net / m
        vel_x += acc_x * dt
        if vel_x < 0:
            vel_x = 0.0
            
        pos_x += vel_x * dt
        
        if pos_x >= target_finish:
            won = True

    # Visualisasi Pygame
    screen.fill((50, 50, 50))  
    
    pygame.draw.line(screen, (255, 255, 255), (0, 225), (WIDTH, 225), 3)
    pygame.draw.line(screen, (255, 255, 255), (0, 375), (WIDTH, 375), 3)
    
    car_y = lane_y_positions[current_lane]
    pygame.draw.rect(screen, (0, 200, 255), (100, car_y - 25, 60, 40))
    
    font = pygame.font.SysFont(None, 28)
    text_pos = font.render(f"Posisi: {pos_x:.1f} m / {target_finish:.0f} m", True, (255, 255, 255))
    text_vel = font.render(f"Kecepatan: {vel_x * 3.6:.1f} km/jam", True, (255, 255, 255))
    text_acc = font.render(f"Percepatan: {acc_x:.2f} m/s^2", True, (255, 255, 255))
    text_lane = font.render(f"Jalur: {current_lane + 1}", True, (255, 255, 255))
    
    screen.blit(text_pos, (20, 20))
    screen.blit(text_vel, (20, 50))
    screen.blit(text_acc, (20, 80))
    screen.blit(text_lane, (20, 110))
    
    if won:
        text_win = font.render("GARIS FINISH TERCAPAI!", True, (0, 255, 0))
        screen.blit(text_win, (WIDTH // 2 - 120, HEIGHT // 2))

    pygame.display.flip()

cap.release()
cv2.destroyAllWindows()
pygame.quit()