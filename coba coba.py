import cv2
import mediapipe as mp
import math

# Inisialisasi modul MediaPipe Hands
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

# Membuka kamera web (0 = kamera bawaan)
cap = cv2.VideoCapture(0)

def hitung_jarak(p1, p2):
    return math.hypot(p1.x - p2.x, p1.y - p2.y)

def jari_terlipat(lm, tip_idx, pip_idx):
    return lm[tip_idx].y > lm[pip_idx].y

def jari_terbuka(lm, tip_idx, pip_idx):
    return lm[tip_idx].y < lm[pip_idx].y

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        print("Gagal mengakses kamera.")
        break

    # Cermin tampilan video secara horizontal
    frame = cv2.flip(frame, 1)
    
    # Konversi BGR ke RGB untuk MediaPipe
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)

    teks_tampilan = ""

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Gambar titik kerangka tangan pada layar
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            
            lm = hand_landmarks.landmark

            # 1. Deteksi Jempol (Good Job)
            # Ujung jempol naik ke atas, 4 jari lainnya terlipat
            jempol_ke_atas = lm[4].y < lm[3].y < lm[2].y
            empat_jari_terlipat = (
                jari_terlipat(lm, 8, 6) and
                jari_terlipat(lm, 12, 10) and
                jari_terlipat(lm, 16, 14) and
                jari_terlipat(lm, 20, 18)
            )

            # 2. Deteksi Saranghae / Finger Heart (I Love U)
            # Ujung jempol (4) dan ujung telunjuk (8) saling bersentuhan/dekat
            jarak_jempol_telunjuk = hitung_jarak(lm[4], lm[8])
            tiga_jari_terlipat = (
                jari_terlipat(lm, 12, 10) and
                jari_terlipat(lm, 16, 14) and
                jari_terlipat(lm, 20, 18)
            )

            # 3. Deteksi Melambai / Tangan Terbuka (Hai)
            # Semua 4 jari utama terbuka ke atas
            semua_jari_terbuka = (
                jari_terbuka(lm, 8, 6) and
                jari_terbuka(lm, 12, 10) and
                jari_terbuka(lm, 16, 14) and
                jari_terbuka(lm, 20, 18)
            )

            # Logika keputusan teks
            if jempol_ke_atas and empat_jari_terlipat:
                teks_tampilan = "goodjob"
            elif jarak_jempol_telunjuk < 0.06 and tiga_jari_terlipat:
                teks_tampilan = "i love u"
            elif semua_jari_terbuka:
                teks_tampilan = "hai"

    # Tampilkan teks jika gestur terdeteksi
    if teks_tampilan:
        cv2.putText(
            frame, 
            teks_tampilan, 
            (50, 100), 
            cv2.FONT_HERSHEY_SIMPLEX, 
            2, 
            (0, 255, 0), 
            4, 
            cv2.LINE_AA
        )

    cv2.imshow("Gesture Recognition", frame)

    # Tekan tombol 'q' untuk menutup kamera
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()