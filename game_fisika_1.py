import tkinter as tk
from tkinter import ttk, messagebox
import math
import random
import time

class ApexSuperbikeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("🏍️ Apex MotoGP Championship - High Performance Edition")
        self.root.geometry("1280x850")
        self.root.configure(bg="#0f172a")

        self.colors = {
            "bg": "#1e293b",
            "panel": "#0f172a",
            "card": "#1e293b",
            "border": "#334155",
            "text": "#f8fafc",
            "subtext": "#94a3b8",
            "accent": "#38bdf8",
            "green": "#22c55e",
            "red": "#ef4444",
            "yellow": "#facc15",
            "orange": "#f97316",
            "sky_top": "#0284c7",
            "sky_bottom": "#bae6fd",
            "grass": "#15803d",
            "asphalt_light": "#475569",
            "asphalt_dark": "#334155",
            "mountain": "#64748b",
            "tree_bark": "#78350f",
            "tree_leaves": "#16a34a"
        }

        self.keys_pressed = set()
        self.root.bind("<KeyPress>", self._on_key_down)
        self.root.bind("<KeyRelease>", self._on_key_up)

        self.last_time = time.time()
        self.frame_count = 0

        # Fisika & Status Pemain
        self.speed = 0.0          
        self.max_speed = 88.0     
        self.lean_angle = 0.0     
        self.target_lean = 0.0
        self.track_distance = 0.0 
        self.player_x = 0.0       
        self.shake_offset = 0.0   
        self.pitch_offset = 0.0   
        
        # Status Game
        self.game_state = "READY"
        self.crash_reason = ""
        self.lap = 1
        self.max_laps = 3
        self.track_length = 3800  
        self.mu_s = 1.25          

        # Segmentasi Trek
        self.track_segments = [
            (600, 0.0),            
            (400, 0.022),          
            (350, -0.028),         
            (650, 0.0),            
            (400, -0.018),         
            (350, 0.035),          
            (400, 0.0),            
            (400, -0.024),         
        ]
        
        self.roadside_objects = []
        self._generate_roadside_objects()

        self.opponents = [
            {"id": 1, "name": "Rider #1 (Ducati)", "color": "#dc2626", "accent": "#ffffff", "dist": 90.0, "x": -0.3, "speed": 68.0, "lean": 0.0},
            {"id": 2, "name": "Rider #93 (KTM)", "color": "#ea580c", "accent": "#0f172a", "dist": 180.0, "x": 0.3, "speed": 70.0, "lean": 0.0},
            {"id": 3, "name": "Rider #72 (Yamaha)", "color": "#2563eb", "accent": "#fde047", "dist": 280.0, "x": -0.1, "speed": 67.0, "lean": 0.0},
            {"id": 4, "name": "Rider #20 (Aprilia)", "color": "#16a34a", "accent": "#dc2626", "dist": 400.0, "x": 0.4, "speed": 66.0, "lean": 0.0},
            {"id": 5, "name": "Rider #89 (Honda)", "color": "#9333ea", "accent": "#ffffff", "dist": 520.0, "x": -0.4, "speed": 65.0, "lean": 0.0},
        ]

        self._create_header()
        self._create_main_layout()
        
        self.update_game_loop()

    def _generate_roadside_objects(self):
        obj_types = ["TREE", "SIGN", "POLE"]
        dist = 0.0
        while dist < self.track_length:
            side = random.choice([-1, 1])
            offset_dist = random.uniform(1.6, 2.4) * side
            obj_type = random.choice(obj_types)
            self.roadside_objects.append({
                "dist": dist,
                "x_side": offset_dist,
                "type": obj_type
            })
            dist += random.uniform(25.0, 45.0)

    def _create_header(self):
        header = tk.Frame(self.root, bg=self.colors["panel"], height=55, bd=1, relief=tk.SOLID)
        header.pack(fill=tk.X, side=tk.TOP, padx=10, pady=(10, 5))

        title = tk.Label(header, text="🏍️ APEX MOTOGP CHAMPIONSHIP",
                         font=("Segoe UI", 14, "bold"), bg=self.colors["panel"], fg=self.colors["accent"])
        title.pack(side=tk.LEFT, padx=15, pady=10)

        self.lbl_pos = tk.Label(header, text="POSISI: 6 / 6", font=("Segoe UI", 11, "bold"),
                                bg="#0284c7", fg="#ffffff", padx=12, pady=5)
        self.lbl_pos.pack(side=tk.RIGHT, padx=15, pady=8)

        self.lbl_lap = tk.Label(header, text="LAP: 1 / 3", font=("Segoe UI", 11, "bold"),
                                bg="#7e22ce", fg="#ffffff", padx=12, pady=5)
        self.lbl_lap.pack(side=tk.RIGHT, padx=(0, 5), pady=8)

    def _create_main_layout(self):
        main = tk.Frame(self.root, bg=self.colors["bg"])
        main.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        left_panel = tk.Frame(main, bg=self.colors["panel"], bd=1, relief=tk.SOLID)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))

        self.canvas = tk.Canvas(left_panel, bg=self.colors["sky_bottom"], highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        right_panel = tk.Frame(main, bg=self.colors["panel"], width=330, bd=1, relief=tk.SOLID)
        right_panel.pack(side=tk.RIGHT, fill=tk.Y, padx=(5, 0))
        right_panel.pack_propagate(False)

        tk.Label(right_panel, text="🎮 KONTROL STANG & GAS", font=("Segoe UI", 11, "bold"),
                 bg=self.colors["panel"], fg=self.colors["accent"]).pack(anchor="w", padx=15, pady=(12, 5))

        controls_text = (
            "• [Panah UP / ↑]    : Gas / Akselerasi\n"
            "• [Panah DOWN / ↓]  : Rem Depan Keras\n"
            "• [Panah LEFT / ←]  : Rebah KIRI\n"
            "• [Panah RIGHT / →] : Rebah KANAN\n"
            "• [SPACE]           : Mulai / Reset Balapan"
        )
        lbl_ctrl = tk.Label(right_panel, text=controls_text, font=("Consolas", 9),
                            bg=self.colors["card"], fg=self.colors["text"], justify=tk.LEFT, padx=10, pady=8, bd=1, relief=tk.SOLID)
        lbl_ctrl.pack(fill=tk.X, padx=15, pady=2)

        tk.Label(right_panel, text="📊 TELEMETRI MOTOGP", font=("Segoe UI", 11, "bold"),
                 bg=self.colors["panel"], fg=self.colors["green"]).pack(anchor="w", padx=15, pady=(12, 5))

        self.telemetry_text = tk.Text(right_panel, bg=self.colors["card"], fg=self.colors["text"],
                                      font=("Consolas", 9), height=11, bd=1, relief=tk.SOLID, padx=10, pady=8)
        self.telemetry_text.pack(fill=tk.X, padx=15, pady=5)

        tk.Label(right_panel, text="🏆 KEDUDUKAN BALAPAN", font=("Segoe UI", 11, "bold"),
                 bg=self.colors["panel"], fg=self.colors["yellow"]).pack(anchor="w", padx=15, pady=(10, 5))

        self.lb_text = tk.Text(right_panel, bg=self.colors["card"], fg=self.colors["text"],
                               font=("Consolas", 9), height=7, bd=1, relief=tk.SOLID, padx=10, pady=5)
        self.lb_text.pack(fill=tk.X, padx=15, pady=5)

        self.btn_reset = tk.Button(right_panel, text="🔄 MULAI / RESET BALAPAN", command=self.reset_race,
                                   font=("Segoe UI", 10, "bold"), bg=self.colors["accent"], fg="#0f172a",
                                   activebackground="#0284c7", activeforeground="#ffffff", bd=0, pady=9, cursor="hand2")
        self.btn_reset.pack(fill=tk.X, padx=15, pady=12, side=tk.BOTTOM)

    def _on_key_down(self, event):
        self.keys_pressed.add(event.keysym)
        if event.keysym == "space":
            self.reset_race()

    def _on_key_up(self, event):
        self.keys_pressed.discard(event.keysym)

    def get_track_info(self, dist):
        norm_dist = dist % self.track_length
        accum = 0.0
        for seg_len, curvature in self.track_segments:
            if accum <= norm_dist < accum + seg_len:
                return curvature
            accum += seg_len
        return 0.0

    def get_upcoming_turn_info(self, dist):
        norm_dist = dist % self.track_length
        accum = 0.0
        for i, (seg_len, curvature) in enumerate(self.track_segments):
            if accum <= norm_dist < accum + seg_len:
                rem_in_seg = (accum + seg_len) - norm_dist
                if abs(curvature) > 0.005:
                    direction = "KANAN" if curvature > 0 else "KIRI"
                    severity = "TAJAM!" if abs(curvature) >= 0.025 else "SEDANG"
                    return f"TIKUNGAN {direction} ({severity}) - {int(rem_in_seg)}m", curvature
                else:
                    next_idx = (i + 1) % len(self.track_segments)
                    next_len, next_curv = self.track_segments[next_idx]
                    if abs(next_curv) > 0.005 and rem_in_seg < 400:
                        direction = "KANAN" if next_curv > 0 else "KIRI"
                        severity = "TAJAM!" if abs(next_curv) >= 0.025 else "SEDANG"
                        return f"⮞ TIKUNGAN {direction} {severity} ({int(rem_in_seg)}m DI DEPAN) ⮞", next_curv
                    return "TREK LURUS PANJANG", 0.0
            accum += seg_len
        return "TREK LURUS", 0.0

    def update_physics(self, dt):
        if self.game_state != "RACING":
            return

        accel = 0.0
        if "Up" in self.keys_pressed:
            accel += 18.0
            self.pitch_offset = min(12.0, self.pitch_offset + 25.0 * dt)
        elif "Down" in self.keys_pressed:
            accel -= 45.0
            self.pitch_offset = max(-18.0, self.pitch_offset - 45.0 * dt)
        else:
            self.pitch_offset *= (1.0 - 5.0 * dt)

        off_track_penalty = 0.0
        if abs(self.player_x) > 1.0:
            off_track_penalty = 30.0 * (abs(self.player_x) - 1.0)
            self.shake_offset = random.uniform(-3, 3)
        else:
            self.shake_offset = 0.0

        drag = 0.0010 * (self.speed ** 2) + off_track_penalty
        self.speed += (accel - drag) * dt
        self.speed = max(0.0, min(self.max_speed, self.speed))

        lean_speed = 135.0
        if "Left" in self.keys_pressed:
            self.target_lean = max(-62.0, self.target_lean - lean_speed * dt)
        elif "Right" in self.keys_pressed:
            self.target_lean = min(62.0, self.target_lean + lean_speed * dt)
        else:
            if self.target_lean > 0:
                self.target_lean = max(0.0, self.target_lean - lean_speed * 1.8 * dt)
            elif self.target_lean < 0:
                self.target_lean = min(0.0, self.target_lean + lean_speed * 1.8 * dt)

        self.lean_angle += (self.target_lean - self.lean_angle) * 14.0 * dt
        self.track_distance += self.speed * dt

        if self.track_distance >= self.lap * self.track_length:
            if self.lap >= self.max_laps:
                self.game_state = "FINISHED"
            else:
                self.lap += 1

        curvature = self.get_track_info(self.track_distance)
        g = 9.81
        
        steering_effect = (self.lean_angle / 60.0) * (self.speed / 20.0) * dt
        curve_drift = curvature * (self.speed ** 1.08) * 0.35 * dt
        
        self.player_x += steering_effect - curve_drift

        if abs(curvature) < 0.001 and abs(self.lean_angle) < 3.0 and not ("Left" in self.keys_pressed or "Right" in self.keys_pressed):
            self.player_x *= (1.0 - 1.2 * dt)

        if abs(curvature) > 0.002:
            r = 1.0 / abs(curvature)
            v_max_grip = math.sqrt(self.mu_s * g * r)

            if self.speed > v_max_grip * 1.28 and abs(self.lean_angle) > 20:
                self.trigger_crash("LOWSIDE CRASH! Ban Kehilangan Grip Akibat Terlalu Cepat Saat Rebah")
            
            if abs(self.player_x) > 2.2:
                self.trigger_crash("OFF-TRACK! Terlempar Keluar Area Sirkuit")

            if (curvature > 0 and self.lean_angle < -20) or (curvature < 0 and self.lean_angle > 20):
                if self.speed > 25:
                    self.trigger_crash("HIGHSIDE CRASH! Miring Berlawanan Arah Tikungan")
        else:
            if abs(self.player_x) > 2.2:
                self.trigger_crash("OFF-TRACK! Menabrak Pembatas Luar")

        for opp in self.opponents:
            opp_curr_curve = self.get_track_info(opp["dist"])
            target_ai_speed = opp["speed"]
            if abs(opp_curr_curve) > 0.010:
                target_ai_speed *= 0.70
                opp["lean"] = 45.0 if opp_curr_curve > 0 else -45.0
            else:
                opp["lean"] = 0.0

            opp["dist"] += target_ai_speed * dt
            opp["x"] += random.uniform(-0.002, 0.002)
            opp["x"] = max(-0.65, min(0.65, opp["x"]))

    def trigger_crash(self, reason):
        self.game_state = "CRASHED"
        self.crash_reason = reason
        self.speed = 0.0

    def reset_race(self):
        self.game_state = "RACING"
        self.speed = 0.0
        self.lean_angle = 0.0
        self.target_lean = 0.0
        self.track_distance = 0.0
        self.player_x = 0.0
        self.lap = 1
        self.crash_reason = ""
        
        for idx, opp in enumerate(self.opponents):
            opp["dist"] = 120.0 + idx * 110.0
            opp["x"] = random.choice([-0.4, -0.2, 0.2, 0.4])

    def render(self):
        self.canvas.delete("all")
        w = self.canvas.winfo_width() or 850
        h = self.canvas.winfo_height() or 550

        cam_roll_rad = math.radians(-self.lean_angle * 0.55)
        cos_cam, sin_cam = math.cos(cam_roll_rad), math.sin(cam_roll_rad)
        
        horizon_y = (h * 0.38) + self.shake_offset + self.pitch_offset
        cx_screen, cy_screen = w / 2, h * 0.55

        def rot_world(x, y):
            dx, dy = x - cx_screen, y - cy_screen
            return dx * cos_cam - dy * sin_cam + cx_screen, dx * sin_cam + dy * cos_cam + cy_screen

        # 1. Sky & Background Environment
        sky_pts = [
            *rot_world(-w*0.5, -h*0.5), *rot_world(w*1.5, -h*0.5),
            *rot_world(w*1.5, horizon_y), *rot_world(-w*0.5, horizon_y)
        ]
        self.canvas.create_polygon(sky_pts, fill=self.colors["sky_top"], outline="")

        # Gunung
        curvature = self.get_track_info(self.track_distance)
        mountain_offset = (self.track_distance * 0.05 + curvature * 2000) % w
        m_pts_raw = [
            (-w + mountain_offset, horizon_y),
            (-w*0.7 + mountain_offset, horizon_y - 45),
            (-w*0.4 + mountain_offset, horizon_y),
            (0 + mountain_offset, horizon_y - 65),
            (w*0.3 + mountain_offset, horizon_y),
            (w*0.6 + mountain_offset, horizon_y - 50),
            (w + mountain_offset, horizon_y),
            (w*1.4 + mountain_offset, horizon_y - 55),
            (w*2.0 + mountain_offset, horizon_y)
        ]
        m_pts_rot = []
        for x, y in m_pts_raw:
            rx, ry = rot_world(x, y)
            m_pts_rot.extend([rx, ry])
        self.canvas.create_polygon(m_pts_rot, fill=self.colors["mountain"], outline="")

        # Rumput Latar Belakang Solid
        grass_bg = [
            *rot_world(-w*0.5, horizon_y), *rot_world(w*1.5, horizon_y),
            *rot_world(w*1.5, h*1.5), *rot_world(-w*0.5, h*1.5)
        ]
        self.canvas.create_polygon(grass_bg, fill=self.colors["grass"], outline="")

        # 2. Pseudo-3D Road Optimization (24 Segmen untuk 60 FPS Sangat Mulus)
        n_segments = 24
        max_depth = 550.0

        seg_points = []
        accum_curve_x = 0.0

        for i in range(n_segments + 1):
            y_norm = i / n_segments
            scale = y_norm ** 2.5
            screen_y = horizon_y + (h - horizon_y) * scale
            road_w = 12 + (w * 0.92) * scale

            z_dist = (1.0 - y_norm) * max_depth
            sample_dist = self.track_distance + z_dist
            seg_curv = self.get_track_info(sample_dist)

            accum_curve_x += seg_curv * (1.0 - y_norm)**1.2 * 1400.0
            center_x = (w / 2) - (self.player_x * road_w * 0.55) + accum_curve_x

            seg_points.append({
                "y": screen_y,
                "w": road_w,
                "cx": center_x,
                "z": z_dist,
                "dist": sample_dist
            })

        # Render Aspal Jalan, Kerbs, dan Markah
        for i in range(n_segments):
            p1 = seg_points[i]
            p2 = seg_points[i + 1]

            is_stripe = int(p1["dist"] * 0.15) % 2 == 0
            road_color = self.colors["asphalt_dark"] if is_stripe else self.colors["asphalt_light"]
            curb_color = self.colors["red"] if is_stripe else "#ffffff"

            curb_w1 = p1["w"] * 0.09
            curb_w2 = p2["w"] * 0.09

            # Kerbs Merah-Putih Kiri & Kanan
            rx1, ry1 = rot_world(p1["cx"] - p1["w"]/2 - curb_w1, p1["y"])
            rx2, ry2 = rot_world(p1["cx"] - p1["w"]/2, p1["y"])
            rx3, ry3 = rot_world(p2["cx"] - p2["w"]/2, p2["y"])
            rx4, ry4 = rot_world(p2["cx"] - p2["w"]/2 - curb_w2, p2["y"])
            self.canvas.create_polygon([rx1, ry1, rx2, ry2, rx3, ry3, rx4, ry4], fill=curb_color, outline="")

            rx1, ry1 = rot_world(p1["cx"] + p1["w"]/2, p1["y"])
            rx2, ry2 = rot_world(p1["cx"] + p1["w"]/2 + curb_w1, p1["y"])
            rx3, ry3 = rot_world(p2["cx"] + p2["w"]/2 + curb_w2, p2["y"])
            rx4, ry4 = rot_world(p2["cx"] + p2["w"]/2, p2["y"])
            self.canvas.create_polygon([rx1, ry1, rx2, ry2, rx3, ry3, rx4, ry4], fill=curb_color, outline="")

            # Aspal Utama
            rx1, ry1 = rot_world(p1["cx"] - p1["w"]/2, p1["y"])
            rx2, ry2 = rot_world(p1["cx"] + p1["w"]/2, p1["y"])
            rx3, ry3 = rot_world(p2["cx"] + p2["w"]/2, p2["y"])
            rx4, ry4 = rot_world(p2["cx"] - p2["w"]/2, p2["y"])
            self.canvas.create_polygon([rx1, ry1, rx2, ry2, rx3, ry3, rx4, ry4], fill=road_color, outline="")

            # Markah Kuning Tengah
            if int(p1["dist"] * 0.3) % 2 == 0 and p2["w"] > 40:
                mw1 = max(1.0, p1["w"] * 0.015)
                mw2 = max(1.0, p2["w"] * 0.015)
                rx1, ry1 = rot_world(p1["cx"] - mw1, p1["y"])
                rx2, ry2 = rot_world(p1["cx"] + mw1, p1["y"])
                rx3, ry3 = rot_world(p2["cx"] + mw2, p2["y"])
                rx4, ry4 = rot_world(p2["cx"] - mw2, p2["y"])
                self.canvas.create_polygon([rx1, ry1, rx2, ry2, rx3, ry3, rx4, ry4], fill=self.colors["yellow"], outline="")

        def get_road_transform(rel_dist):
            y_norm = max(0.0, min(1.0, 1.0 - (rel_dist / max_depth)))
            float_idx = y_norm * n_segments
            idx = min(n_segments - 1, int(float_idx))
            frac = float_idx - idx
            
            p1 = seg_points[idx]
            p2 = seg_points[min(n_segments, idx + 1)]

            seg_cx = p1["cx"] + (p2["cx"] - p1["cx"]) * frac
            seg_w = p1["w"] + (p2["w"] - p1["w"]) * frac
            seg_y = p1["y"] + (p2["y"] - p1["y"]) * frac
            scale = max(0.001, (seg_y - horizon_y) / max(1.0, (h - horizon_y)))
            return seg_cx, seg_w, seg_y, scale

        # 3. Render Pinggir Jalan
        for obj in self.roadside_objects:
            rel_dist = (obj["dist"] - (self.track_distance % self.track_length))
            if rel_dist < 0:
                rel_dist += self.track_length

            if 10.0 < rel_dist < max_depth:
                seg_cx, seg_w, seg_y, scale = get_road_transform(rel_dist)
                obj_x = seg_cx + (obj["x_side"] * seg_w * 0.50)
                rx, ry = rot_world(obj_x, seg_y)
                self._draw_roadside_object(rx, ry, scale, obj["type"])

        # 4. Render AI Lawan
        sorted_opponents = sorted(self.opponents, key=lambda o: o["dist"], reverse=True)

        for opp in sorted_opponents:
            rel_dist = opp["dist"] - self.track_distance
            if 0 < rel_dist < max_depth:
                seg_cx, seg_w, seg_y, scale = get_road_transform(rel_dist)
                if scale > 0.015:
                    opp_x = seg_cx + (opp["x"] * seg_w * 0.40)
                    rx, ry = rot_world(opp_x, seg_y)
                    self._draw_detailed_opponent(rx, ry, scale, opp)

        # 5. Kokpit & Dashboard
        self._draw_cockpit(w, h)

        # 6. Peringatan Tikungan & Minimap
        self._draw_turn_warning_hud(w, h)
        self._draw_minimap(w, h)

        # 7. Status Game Overlay
        if self.game_state == "CRASHED":
            self.canvas.create_rectangle(w*0.1, h*0.35, w*0.9, h*0.65, fill="#0f172a", outline=self.colors["red"], width=3)
            self.canvas.create_text(w/2, h*0.43, text="💥 CRASH! KECELAKAAN BALAPAN", fill=self.colors["red"], font=("Segoe UI", 18, "bold"))
            self.canvas.create_text(w/2, h*0.52, text=self.crash_reason, fill="#f8fafc", font=("Segoe UI", 11))
            self.canvas.create_text(w/2, h*0.59, text="Tekan [SPACE] untuk Ulang Balapan", fill=self.colors["accent"], font=("Segoe UI", 10, "bold"))

        elif self.game_state == "READY":
            self.canvas.create_rectangle(w*0.15, h*0.35, w*0.85, h*0.65, fill="#0f172a", outline=self.colors["accent"], width=3)
            self.canvas.create_text(w/2, h*0.44, text="🏁 APEX MOTOGP CHAMPIONSHIP", fill=self.colors["accent"], font=("Segoe UI", 18, "bold"))
            self.canvas.create_text(w/2, h*0.54, text="Tekan [SPACE] atau Tombol [PANAH UP / ↑] untuk Gas", fill="#f8fafc", font=("Segoe UI", 11))

        elif self.game_state == "FINISHED":
            self.canvas.create_rectangle(w*0.15, h*0.35, w*0.85, h*0.65, fill="#0f172a", outline=self.colors["green"], width=3)
            self.canvas.create_text(w/2, h*0.48, text="🏆 FINISH! BALAPAN SELESAI", fill=self.colors["green"], font=("Segoe UI", 20, "bold"))

    def _draw_roadside_object(self, x, y, scale, obj_type):
        if obj_type == "TREE":
            tw, th = 35 * scale, 100 * scale
            self.canvas.create_rectangle(x - tw*0.15, y - th*0.4, x + tw*0.15, y, fill=self.colors["tree_bark"], outline="")
            self.canvas.create_oval(x - tw*0.8, y - th, x + tw*0.8, y - th*0.3, fill=self.colors["tree_leaves"], outline="")

        elif obj_type == "SIGN":
            sw, sh = 60 * scale, 70 * scale
            self.canvas.create_line(x, y, x, y - sh, fill="#64748b", width=max(1, int(3*scale)))
            self.canvas.create_rectangle(x - sw*0.5, y - sh - 25*scale, x + sw*0.5, y - sh + 5*scale, fill="#38bdf8", outline="#ffffff")
            if scale > 0.18:
                self.canvas.create_text(x, y - sh - 10*scale, text="MOTOGP", fill="#0f172a", font=("Segoe UI", max(6, int(9*scale)), "bold"))

        elif obj_type == "POLE":
            pw, ph = 12 * scale, 90 * scale
            self.canvas.create_rectangle(x - pw*0.2, y - ph, x + pw*0.2, y, fill="#94a3b8", outline="")
            self.canvas.create_oval(x - pw*0.8, y - ph - 5*scale, x + pw*0.8, y - ph + 5*scale, fill="#facc15", outline="")

    def _draw_detailed_opponent(self, x, y, scale, opp):
        bw = 120 * scale
        bh = 140 * scale
        
        opp_roll = math.radians(opp["lean"] * 0.5)
        cos_o, sin_o = math.cos(opp_roll), math.sin(opp_roll)

        def rot_opp(px, py):
            dx, dy = px - x, py - y
            return x + dx * cos_o - dy * sin_o, y + dx * sin_o + dy * cos_o

        self.canvas.create_oval(x - bw*0.5, y - 4*scale, x + bw*0.5, y + 6*scale, fill="#020617", outline="")

        tire_w, tire_h = max(2, 24 * scale), max(3, 52 * scale)
        self.canvas.create_oval(x - tire_w/2, y - tire_h, x + tire_w/2, y, fill="#090d16", outline="#334155", width=max(1, int(1*scale)))

        b1 = rot_opp(x - bw*0.38, y - bh*0.22)
        b2 = rot_opp(x - bw*0.48, y - bh*0.55)
        b3 = rot_opp(x - bw*0.22, y - bh*0.82)
        b4 = rot_opp(x + bw*0.22, y - bh*0.82)
        b5 = rot_opp(x + bw*0.48, y - bh*0.55)
        b6 = rot_opp(x + bw*0.38, y - bh*0.22)
        self.canvas.create_polygon([*b1, *b2, *b3, *b4, *b5, *b6], fill=opp["color"], outline="#020617", width=max(1, int(1.5*scale)))

        rider_y = y - bh*0.48
        r1 = rot_opp(x - bw*0.32, rider_y)
        r2 = rot_opp(x - bw*0.22, rider_y - bh*0.32)
        r3 = rot_opp(x + bw*0.22, rider_y - bh*0.32)
        r4 = rot_opp(x + bw*0.32, rider_y)
        self.canvas.create_polygon([*r1, *r2, *r3, *r4], fill="#1e293b", outline=opp["color"], width=max(1, int(1.5*scale)))

        helm_r = max(2, 18 * scale)
        hx, hy = rot_opp(x, rider_y - bh*0.32)
        self.canvas.create_oval(hx - helm_r, hy - helm_r, hx + helm_r, hy + helm_r,
                                fill=opp.get("accent", "#ffffff"), outline="#020617", width=max(1, int(1.5*scale)))

        if scale > 0.20:
            self.canvas.create_text(x, y - bh - (18*scale), text=opp["name"], fill="#ffffff",
                                    font=("Segoe UI", max(8, int(11*scale)), "bold"))

    def _draw_cockpit(self, w, h):
        cx, cy = w / 2, h + 25
        
        cockpit_roll = math.radians(self.lean_angle * 0.15)
        cos_c, sin_c = math.cos(cockpit_roll), math.sin(cockpit_roll)

        def rot_cp(px, py):
            dx, dy = px - cx, py - cy
            return cx + dx * cos_c - dy * sin_c, cy + dx * sin_c + dy * cos_c

        p1 = rot_cp(cx - 140, h)
        p2 = rot_cp(cx - 90, h - 85)
        p3 = rot_cp(cx + 90, h - 85)
        p4 = rot_cp(cx + 140, h)
        self.canvas.create_polygon([*p1, *p2, *p3, *p4], fill="#0f172a", outline=self.colors["accent"], width=2)

        speed_kmh = int(self.speed * 3.6)
        hud_pt = rot_cp(cx, h - 52)
        self.canvas.create_text(hud_pt[0], hud_pt[1], text=f"{speed_kmh}", fill="#38bdf8", font=("Consolas", 26, "bold"))
        hud_lbl = rot_cp(cx, h - 24)
        self.canvas.create_text(hud_lbl[0], hud_lbl[1], text="KM/H", fill="#94a3b8", font=("Segoe UI", 8, "bold"))

        lb1 = rot_cp(cx - 140, h - 65)
        lb2 = rot_cp(cx - 260, h - 20)
        self.canvas.create_line(lb1[0], lb1[1], lb2[0], lb2[1], fill="#1e293b", width=14)
        self.canvas.create_line(lb1[0], lb1[1], lb2[0], lb2[1], fill="#0284c7", width=5)

        rb1 = rot_cp(cx + 140, h - 65)
        rb2 = rot_cp(cx + 260, h - 20)
        self.canvas.create_line(rb1[0], rb1[1], rb2[0], rb2[1], fill="#1e293b", width=14)
        self.canvas.create_line(rb1[0], rb1[1], rb2[0], rb2[1], fill="#0284c7", width=5)

    def _draw_turn_warning_hud(self, w, h):
        turn_msg, curv_val = self.get_upcoming_turn_info(self.track_distance)
        if "TIKUNGAN" in turn_msg:
            r_val = 1.0 / abs(curv_val) if abs(curv_val) > 0.001 else 999.0
            v_max_safe = math.sqrt(self.mu_s * 9.81 * r_val) * 3.6
            
            box_color = self.colors["red"] if self.speed * 3.6 > v_max_safe else self.colors["green"]
            warning_text = turn_msg
            if self.speed * 3.6 > v_max_safe:
                warning_text += f" | ⚠️ REM! KECEPATAN AMAN {int(v_max_safe)} KM/H"

            self.canvas.create_rectangle(w*0.15, 15, w*0.85, 48, fill="#0f172a", outline=box_color, width=2)
            self.canvas.create_text(w/2, 31, text=warning_text, fill=box_color, font=("Segoe UI", 10, "bold"))

    def _draw_minimap(self, w, h):
        map_cx, map_cy = w - 85, 85
        r = 60
        self.canvas.create_oval(map_cx - r, map_cy - r, map_cx + r, map_cy + r, fill="#020617", outline="#334155", width=2)
        self.canvas.create_text(map_cx, map_cy - r + 12, text="MINIMAP", fill="#94a3b8", font=("Segoe UI", 7, "bold"))

        num_pts = 24
        pts = []
        for i in range(num_pts):
            angle = (i / num_pts) * 2 * math.pi
            rx = (r - 18) * (1.0 + 0.15 * math.sin(2 * angle))
            ry = (r - 28) * (1.0 + 0.10 * math.cos(3 * angle))
            px = map_cx + rx * math.cos(angle)
            py = map_cy + ry * math.sin(angle)
            pts.extend([px, py])
        self.canvas.create_polygon(pts, fill="", outline="#64748b", width=3)

        player_angle = ((self.track_distance % self.track_length) / self.track_length) * 2 * math.pi
        prx = (r - 18) * (1.0 + 0.15 * math.sin(2 * player_angle))
        pry = (r - 28) * (1.0 + 0.10 * math.cos(3 * player_angle))
        ppx = map_cx + prx * math.cos(player_angle)
        ppy = map_cy + pry * math.sin(player_angle)
        self.canvas.create_oval(ppx - 4, ppy - 4, ppx + 4, ppy + 4, fill="#facc15", outline="#ffffff", width=1)

        for opp in self.opponents:
            opp_angle = ((opp["dist"] % self.track_length) / self.track_length) * 2 * math.pi
            orx = (r - 18) * (1.0 + 0.15 * math.sin(2 * opp_angle))
            ory = (r - 28) * (1.0 + 0.10 * math.cos(3 * opp_angle))
            opx = map_cx + orx * math.cos(opp_angle)
            opy = map_cy + ory * math.sin(opp_angle)
            self.canvas.create_oval(opx - 3, opy - 3, opx + 3, opy + 3, fill=opp["color"], outline="")

    def update_ui_text(self):
        curr_curve = self.get_track_info(self.track_distance)
        r_val = 1.0 / abs(curr_curve) if abs(curr_curve) > 0.001 else 999.0
        g = 9.81
        
        ideal_tan = (self.speed ** 2) / (r_val * g) if r_val < 999 else 0.0
        ideal_lean = math.degrees(math.atan(ideal_tan))
        if curr_curve < 0:
            ideal_lean = -ideal_lean

        a_c = (self.speed ** 2) / r_val if r_val < 999 else 0.0
        g_force = a_c / g

        tele =  f"Kecepatan Real   : {self.speed*3.6:.1f} km/h\n"
        tele += f"Sudut Miring (θ) : {self.lean_angle:.1f}°\n"
        tele += f"Sudut Req Ideal  : {ideal_lean:.1f}°\n"
        tele += f"G-Force Lateral  : {g_force:.2f} G\n"
        tele += f"Radius Tikungan  : {r_val:.1f} m\n"
        tele += f"Grip Ban (μs)    : {self.mu_s:.2f}\n"
        tele += f"Offset Posisi    : {self.player_x:.2f}\n"

        self.telemetry_text.delete("1.0", tk.END)
        self.telemetry_text.insert(tk.END, tele)

        all_racers = [{"name": "ANDA (Rider)", "dist": self.track_distance, "is_player": True}]
        for opp in self.opponents:
            all_racers.append({"name": opp["name"], "dist": opp["dist"], "is_player": False})

        sorted_racers = sorted(all_racers, key=lambda x: x["dist"], reverse=True)
        player_rank = 1
        lb_str = ""
        for idx, r in enumerate(sorted_racers, 1):
            if r["is_player"]:
                player_rank = idx
                lb_str += f" > {idx}. {r['name']:<14} (YOU)\n"
            else:
                lb_str += f"   {idx}. {r['name']:<14}\n"

        self.lbl_pos.config(text=f"POSISI: {player_rank} / 6")
        self.lbl_lap.config(text=f"LAP: {self.lap} / {self.max_laps}")

        self.lb_text.delete("1.0", tk.END)
        self.lb_text.insert(tk.END, lb_str)

    def update_game_loop(self):
        now = time.time()
        dt = now - self.last_time
        self.last_time = now

        dt = min(dt, 0.033) # Cap delta time ke max ~30 FPS step untuk hindari physics skip

        self.frame_count += 1

        self.update_physics(dt)
        self.render()
        
        # Throttling update teks GUI (setiap 6 frame ~10 kali/detik) untuk efisiensi CPU
        if self.frame_count % 6 == 0:
            self.update_ui_text()

        self.root.after(15, self.update_game_loop)

if __name__ == "__main__":
    root = tk.Tk()
    app = ApexSuperbikeGame(root)
    root.mainloop()