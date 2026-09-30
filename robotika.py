import time

class RobotDynamicsController:
    def __init__(self, surface_type="dry_asphalt"):
        # Parameter Fisika
        self.m = 1000.0  # Massa robot/kendaraan dalam kg
        self.g = 9.81    # Percepatan gravitasi dalam m/s^2
        self.f_gas_max = 35000.0  # Gaya dorong maksimum dalam N
        self.f_rem_max = 45000.0  # Gaya rem maksimum dalam N
        
        # Koefisien gesek kinetis berdasarkan jenis permukaan
        friction_coefficients = {
            "dry_asphalt": 0.50, # Aspal kering
            "wet_asphalt": 0.25, # Aspal basah
            "ice": 0.05          # Es
        }
        self.mu_k = friction_coefficients.get(surface_type, 0.50)
        
        # State variabel robot
        self.position_x = 0.0  # Posisi aksial longitudinal (m)
        self.current_lane = 1  # Jalur aktif (0: Kiri/Atas, 1: Tengah, 2: Kanan/Bawah)
        self.velocity = 0.0    # Kecepatan linear (m/s)
        self.pitch_angle = 0.0 # Kemiringan bodi akibat inersia
        self.is_emergency_stop = False

    def calculate_friction(self):
        # Gaya Normal N = m * g
        normal_force = self.m * self.g
        # Gaya Gesek F_gesek = mu_k * N
        return self.mu_k * normal_force

    def update_physics(self, throttle_input, brake_input, dt):
        if self.is_emergency_stop:
            self.velocity = 0.0
            return

        # Gaya dorong dan gaya rem berdasarkan input kontroler (0.0 - 1.0)
        f_thrust = throttle_input * self.f_gas_max
        f_brake = brake_input * self.f_rem_max
        f_friction = self.calculate_friction()

        # Kalkulasi total gaya bersih (Hukum II Newton)
        if self.velocity > 0:
            net_force = f_thrust - f_brake - f_friction
        else:
            net_force = max(0.0, f_thrust - f_brake)

        # Percepatan a = total_F / m
        acceleration = net_force / self.m

        # Update kecepatan dan posisi linear
        self.velocity += acceleration * dt
        if self.velocity < 0:
            self.velocity = 0.0  # Mencegah gerakan mundur spontan

        self.position_x += self.velocity * dt

        # Simulasi Kelembaman / Inersia (Hukum I Newton)
        # Rotasi bodi (pitch angle) menunduk saat pengereman mendadak
        if brake_input > 0.5 and self.velocity > 0:
            self.pitch_angle = -5.0  
        else:
            self.pitch_angle = 0.0

    def change_lane(self, direction):
        # Navigasi Lateral (Pindah Jalur)
        if direction == "left" and self.current_lane > 0:
            self.current_lane -= 1
        elif direction == "right" and self.current_lane < 2:
            self.current_lane += 1

    def check_collision(self, obstacle_x, obstacle_lane):
        # Transfer gaya benturan (Hukum III Newton / Aksi-Reaksi)
        if self.current_lane == obstacle_lane and abs(self.position_x - obstacle_x) < 2.0:
            self.is_emergency_stop = True
            self.velocity = 0.0
            return True
        return False


# Simulasi eksekusi loop robotik sederhana
if __name__ == "__main__":
    robot = RobotDynamicsController(surface_type="dry_asphalt")
    time_step = 0.1  # dt = 0.1 detik
    
    print("Menjalankan simulasi kontroler robot...")
    
    # Skenario 1: Akselerasi dengan gaya dorong penuh
    for step in range(5):
        robot.update_physics(throttle_input=1.0, brake_input=0.0, dt=time_step)
        print(f"Step {step+1} | Posisi: {robot.position_x:.2f} m | Kecepatan: {robot.velocity:.2f} m/s | Pitch Angle: {robot.pitch_angle}°")

    # Skenario 2: Pengereman mendadak (Inersia)
    print("\nPengereman mendadak diaplikasikan...")
    robot.update_physics(throttle_input=0.0, brake_input=1.0, dt=time_step)
    print(f"Hasil | Kecepatan: {robot.velocity:.2f} m/s | Pitch Angle: {robot.pitch_angle}° (Inersia Bodi)")

    # Skenario 3: Deteksi Rintangan (Aksi-Reaksi)
    obstacle_position = robot.position_x + 1.0
    if robot.check_collision(obstacle_x=obstacle_position, obstacle_lane=robot.current_lane):
        print(f"\n[EMERGENCY STOP] Benturan terdeteksi pada posisi {obstacle_position:.2f} m! Robot dihentikan secara instan.")