#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AURA // NETSTRESS - Gen Z Edition WLAN & Network Load Tester
Zero-Disk-I/O | Minimal CPU Overhead | Multi-Location | Live Telemetry
Requires only Python 3 Standard Library (tkinter, urllib, ssl, threading, time)
"""

import tkinter as tk
from tkinter import ttk
import threading
import time
import urllib.request
import ssl
from collections import deque

# --- GEN Z / CYBERPUNK AURA COLOR PALETTE ---
BG_MAIN = "#09090E"        # Deep Obsidian
BG_CARD = "#13131F"        # Dark Bento Card
BG_CARD_ALT = "#1B1B2E"    # Hover / Secondary Card
ACCENT_PURPLE = "#A855F7"  # Electric Purple
ACCENT_CYAN = "#06B6D4"    # Cyber Cyan
ACCENT_LIME = "#84CC16"    # Acid Lime
ACCENT_PINK = "#EC4899"    # Hot Pink
TEXT_MAIN = "#F8FAFC"      # Crisp White
TEXT_MUTED = "#94A3B8"     # Muted Slate
BORDER_COLOR = "#27273A"   # Subtle Border

LOCATIONS = {
    "🇩🇪 Falkenstein (Hetzner FSN1 - 10GB)": "https://fsn1-speed.hetzner.com/10GB.bin",
    "🇩🇪 Nürnberg (Hetzner NBG1 - 10GB)": "https://nbg1-speed.hetzner.com/10GB.bin",
    "🇫🇮 Helsinki (Hetzner HEL1 - 10GB)": "https://hel1-speed.hetzner.com/10GB.bin",
    "🇺🇸 Ashburn, VA (Hetzner ASH - 10GB)": "https://ash-speed.hetzner.com/10GB.bin",
    "🇺🇸 Hillsboro, OR (Hetzner HIL - 10GB)": "https://hil-speed.hetzner.com/10GB.bin",
    "🇸🇬 Singapur (Hetzner SIN - 10GB)": "https://sin-speed.hetzner.com/10GB.bin",
    "🇩🇪 Falkenstein (Hetzner FSN1 - 1GB)": "https://fsn1-speed.hetzner.com/1GB.bin",
}

def get_vibe_status(mbps, running):
    if not running:
        return "💤 AFK / CHILLING (Bereit)"
    if mbps <= 0.1:
        return "⏳ CONNECTING TO THE MATRIX..."
    if mbps < 15:
        return "💀 COOKED (Bambus-Leitung)"
    if mbps < 50:
        return "😐 MID CONNECTION (Solide, aber ausbaufähig)"
    if mbps < 150:
        return "🔥 VALID SPEED (Stabil unterwegs)"
    if mbps < 400:
        return "⚡ LOCKED IN (Router glüht)"
    return "👑 +10000 AURA (Gigabit God Mode)"


class AuraNetStressApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AURA // NETSTRESS ⚡ WLAN Load Engine")
        self.root.geometry("820x680")
        self.root.minsize(780, 650)
        self.root.configure(bg=BG_MAIN)

        # State Variables
        self.is_running = False
        self.total_bytes = 0
        self.interval_bytes = 0
        self.peak_mbps = 0.0
        self.current_mbps = 0.0
        self.start_time = 0.0
        self.last_tick = 0.0
        self.lock = threading.Lock()
        self.speed_history = deque([0.0] * 60, maxlen=60)

        # Control Variables
        self.selected_location = tk.StringVar(value=list(LOCATIONS.keys())[0])
        self.thread_count = tk.IntVar(value=1)
        self.speed_limit = tk.DoubleVar(value=0.0)   # 0 = Unlimited
        self.gb_target = tk.DoubleVar(value=0.0)     # 0 = Infinite

        self._setup_styles()
        self._build_ui()
        self._update_ui_loop()

    def _setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "TCombobox",
            fieldbackground=BG_CARD_ALT,
            background=ACCENT_PURPLE,
            foreground=TEXT_MAIN,
            arrowcolor=TEXT_MAIN,
            borderwidth=0,
        )
        self.root.option_add("*TCombobox*Listbox*Background", BG_CARD_ALT)
        self.root.option_add("*TCombobox*Listbox*Foreground", TEXT_MAIN)
        self.root.option_add("*TCombobox*Listbox*selectBackground", ACCENT_PURPLE)

    def _build_ui(self):
        # --- HEADER ---
        header = tk.Frame(self.root, bg=BG_MAIN, padx=24, pady=16)
        header.pack(fill="x")

        title_lbl = tk.Label(
            header,
            text="AURA // NETSTRESS",
            font=("Segoe UI", 20, "bold"),
            fg=TEXT_MAIN,
            bg=BG_MAIN,
        )
        title_lbl.pack(side="left")

        badge_lbl = tk.Label(
            header,
            text=" ZERO-DISK-I/O • LOW CPU ",
            font=("Segoe UI", 9, "bold"),
            fg=BG_MAIN,
            bg=ACCENT_CYAN,
            padx=6,
            pady=2,
        )
        badge_lbl.pack(side="left", padx=12)

        self.vibe_lbl = tk.Label(
            header,
            text="💤 AFK / CHILLING (Bereit)",
            font=("Segoe UI", 11, "bold"),
            fg=ACCENT_PURPLE,
            bg=BG_MAIN,
        )
        self.vibe_lbl.pack(side="right")

        # --- HERO METRICS (BENTO GRID) ---
        metrics_frame = tk.Frame(self.root, bg=BG_MAIN, padx=20)
        metrics_frame.pack(fill="x", pady=(0, 12))
        for i in range(4):
            metrics_frame.columnconfigure(i, weight=1, uniform="bento")

        self.lbl_speed = self._create_metric_card(
            metrics_frame, 0, "LIVE SPEED", "0.00", "Mbit/s", ACCENT_CYAN
        )
        self.lbl_gb = self._create_metric_card(
            metrics_frame, 1, "DATA YEETED", "0.00", "GB geladen", ACCENT_PURPLE
        )
        self.lbl_peak = self._create_metric_card(
            metrics_frame, 2, "PEAK SPEED", "0.00", "Mbit/s Max", ACCENT_PINK
        )
        self.lbl_time = self._create_metric_card(
            metrics_frame, 3, "UPTIME", "00:00:00", "hh:mm:ss", ACCENT_LIME
        )

        # --- LIVE WAVEFORM GRAPH ---
        graph_card = tk.Frame(
            self.root,
            bg=BG_CARD,
            highlightbackground=BORDER_COLOR,
            highlightthickness=1,
            padx=16,
            pady=12,
        )
        graph_card.pack(fill="x", padx=24, pady=(0, 12))

        graph_header = tk.Frame(graph_card, bg=BG_CARD)
        graph_header.pack(fill="x", pady=(0, 6))

        tk.Label(
            graph_header,
            text="📈 LIVE THROUGHPUT WAVEFORM (60s)",
            font=("Segoe UI", 9, "bold"),
            fg=TEXT_MUTED,
            bg=BG_CARD,
        ).pack(side="left")

        self.lbl_avg = tk.Label(
            graph_header,
            text="Ø 0.00 Mbit/s",
            font=("Segoe UI", 9, "bold"),
            fg=ACCENT_CYAN,
            bg=BG_CARD,
        )
        self.lbl_avg.pack(side="right")

        self.canvas = tk.Canvas(
            graph_card, bg="#0D0D16", height=130, highlightthickness=0
        )
        self.canvas.pack(fill="x")

        # --- CONTROLS & EXTRAS BENTO ---
        ctrl_card = tk.Frame(
            self.root,
            bg=BG_CARD,
            highlightbackground=BORDER_COLOR,
            highlightthickness=1,
            padx=18,
            pady=16,
        )
        ctrl_card.pack(fill="x", padx=24, pady=(0, 14))
        ctrl_card.columnconfigure(0, weight=1)
        ctrl_card.columnconfigure(1, weight=1)

        # Left Column: Server & Threads
        left_col = tk.Frame(ctrl_card, bg=BG_CARD)
        left_col.grid(row=0, column=0, sticky="nsew", padx=(0, 12))

        tk.Label(
            left_col,
            text="🌍 SERVER STANDORT (HETZNER)",
            font=("Segoe UI", 9, "bold"),
            fg=TEXT_MUTED,
            bg=BG_CARD,
        ).pack(anchor="w")

        self.combo_loc = ttk.Combobox(
            left_col,
            textvariable=self.selected_location,
            values=list(LOCATIONS.keys()),
            state="readonly",
            font=("Segoe UI", 10),
        )
        self.combo_loc.pack(fill="x", pady=(4, 12), ipady=4)

        tk.Label(
            left_col,
            text="🚀 PARALLEL-STREAMS (THREADS): Multi-Stream für max. WLAN-Last",
            font=("Segoe UI", 9, "bold"),
            fg=TEXT_MUTED,
            bg=BG_CARD,
        ).pack(anchor="w")

        thread_frame = tk.Frame(left_col, bg=BG_CARD)
        thread_frame.pack(fill="x", pady=(4, 0))

        self.lbl_threads_val = tk.Label(
            thread_frame,
            text="1 Stream",
            font=("Segoe UI", 10, "bold"),
            fg=ACCENT_PURPLE,
            bg=BG_CARD,
            width=10,
            anchor="w",
        )
        self.lbl_threads_val.pack(side="left")

        self.scale_threads = tk.Scale(
            thread_frame,
            from_=1,
            to=8,
            orient="horizontal",
            variable=self.thread_count,
            bg=BG_CARD,
            fg=TEXT_MAIN,
            highlightthickness=0,
            troughcolor=BG_CARD_ALT,
            activebackground=ACCENT_PURPLE,
            showvalue=False,
            command=self._on_thread_change,
        )
        self.scale_threads.pack(side="left", fill="x", expand=True)

        # Right Column: Throttle & Auto-Stop
        right_col = tk.Frame(ctrl_card, bg=BG_CARD)
        right_col.grid(row=0, column=1, sticky="nsew", padx=(12, 0))

        tk.Label(
            right_col,
            text="🛡️ SPEED-LIMITER (0 = UNLIMITED FULL SEND)",
            font=("Segoe UI", 9, "bold"),
            fg=TEXT_MUTED,
            bg=BG_CARD,
        ).pack(anchor="w")

        limit_frame = tk.Frame(right_col, bg=BG_CARD)
        limit_frame.pack(fill="x", pady=(4, 12))

        self.lbl_limit_val = tk.Label(
            limit_frame,
            text="Unlimited",
            font=("Segoe UI", 10, "bold"),
            fg=ACCENT_CYAN,
            bg=BG_CARD,
            width=12,
            anchor="w",
        )
        self.lbl_limit_val.pack(side="left")

        self.scale_limit = tk.Scale(
            limit_frame,
            from_=0,
            to=500,
            resolution=5,
            orient="horizontal",
            variable=self.speed_limit,
            bg=BG_CARD,
            fg=TEXT_MAIN,
            highlightthickness=0,
            troughcolor=BG_CARD_ALT,
            activebackground=ACCENT_CYAN,
            showvalue=False,
            command=self._on_limit_change,
        )
        self.scale_limit.pack(side="left", fill="x", expand=True)

        tk.Label(
            right_col,
            text="🎯 AUTO-STOP ZIEL (0 = ENDLOS DAUERLAST)",
            font=("Segoe UI", 9, "bold"),
            fg=TEXT_MUTED,
            bg=BG_CARD,
        ).pack(anchor="w")

        target_frame = tk.Frame(right_col, bg=BG_CARD)
        target_frame.pack(fill="x", pady=(4, 0))

        self.lbl_target_val = tk.Label(
            target_frame,
            text="Endlos (∞)",
            font=("Segoe UI", 10, "bold"),
            fg=ACCENT_LIME,
            bg=BG_CARD,
            width=12,
            anchor="w",
        )
        self.lbl_target_val.pack(side="left")

        self.scale_target = tk.Scale(
            target_frame,
            from_=0,
            to=250,
            resolution=5,
            orient="horizontal",
            variable=self.gb_target,
            bg=BG_CARD,
            fg=TEXT_MAIN,
            highlightthickness=0,
            troughcolor=BG_CARD_ALT,
            activebackground=ACCENT_LIME,
            showvalue=False,
            command=self._on_target_change,
        )
        self.scale_target.pack(side="left", fill="x", expand=True)

        # --- BOTTOM ACTION BAR ---
        action_frame = tk.Frame(self.root, bg=BG_MAIN, padx=24, pady=4)
        action_frame.pack(fill="x")

        self.btn_toggle = tk.Button(
            action_frame,
            text="🚀 LOCK IN // DAUERLAST STARTEN",
            font=("Segoe UI", 13, "bold"),
            bg=ACCENT_PURPLE,
            fg=TEXT_MAIN,
            activebackground=ACCENT_PINK,
            activeforeground=TEXT_MAIN,
            relief="flat",
            cursor="hand2",
            pady=12,
            command=self.toggle_stress,
        )
        self.btn_toggle.pack(side="left", fill="x", expand=True, padx=(0, 10))

        self.btn_reset = tk.Button(
            action_frame,
            text="↺ RESET STATS",
            font=("Segoe UI", 11, "bold"),
            bg=BG_CARD_ALT,
            fg=TEXT_MUTED,
            activebackground=BORDER_COLOR,
            activeforeground=TEXT_MAIN,
            relief="flat",
            cursor="hand2",
            padx=18,
            pady=12,
            command=self.reset_stats,
        )
        self.btn_reset.pack(side="right")

    def _create_metric_card(self, parent, col, title, val, unit, accent):
        card = tk.Frame(
            parent,
            bg=BG_CARD,
            highlightbackground=BORDER_COLOR,
            highlightthickness=1,
            padx=14,
            pady=12,
        )
        card.grid(row=0, column=col, sticky="nsew", padx=4)

        tk.Label(
            card, text=title, font=("Segoe UI", 8, "bold"), fg=TEXT_MUTED, bg=BG_CARD
        ).pack(anchor="w")

        val_lbl = tk.Label(
            card, text=val, font=("Segoe UI", 20, "bold"), fg=accent, bg=BG_CARD
        )
        val_lbl.pack(anchor="w", pady=(2, 0))

        tk.Label(
            card, text=unit, font=("Segoe UI", 8), fg=TEXT_MUTED, bg=BG_CARD
        ).pack(anchor="w")

        return val_lbl

    # --- SLIDER CALLBACKS ---
    def _on_thread_change(self, val):
        v = int(float(val))
        self.lbl_threads_val.config(text=f"{v} Stream{'s' if v > 1 else ''}")

    def _on_limit_change(self, val):
        v = int(float(val))
        if v == 0:
            self.lbl_limit_val.config(text="Unlimited")
        else:
            self.lbl_limit_val.config(text=f"{v} Mbit/s")

    def _on_target_change(self, val):
        v = int(float(val))
        if v == 0:
            self.lbl_target_val.config(text="Endlos (∞)")
        else:
            self.lbl_target_val.config(text=f"Stop @ {v} GB")

    # --- WORKER LOGIC (ZERO DISK I/O) ---
    def toggle_stress(self):
        if not self.is_running:
            self.is_running = True
            if self.start_time == 0.0:
                self.start_time = time.time()
            self.last_tick = time.time()
            self.btn_toggle.config(
                text="🛑 TOUCH GRASS // DAUERLAST STOPPEN", bg=ACCENT_PINK
            )
            self.combo_loc.config(state="disabled")
            self.scale_threads.config(state="disabled")

            url = LOCATIONS[self.selected_location.get()]
            num_threads = self.thread_count.get()

            for _ in range(num_threads):
                t = threading.Thread(target=self._download_worker, args=(url,), daemon=True)
                t.start()
        else:
            self.is_running = False
            self.btn_toggle.config(
                text="🚀 LOCK IN // DAUERLAST STARTEN", bg=ACCENT_PURPLE
            )
            self.combo_loc.config(state="readonly")
            self.scale_threads.config(state="normal")

    def reset_stats(self):
        with self.lock:
            self.total_bytes = 0
            self.interval_bytes = 0
            self.peak_mbps = 0.0
            self.current_mbps = 0.0
            self.start_time = time.time() if self.is_running else 0.0
            self.speed_history = deque([0.0] * 60, maxlen=60)
        self._draw_graph()

    def _download_worker(self, url):
        # 256 KB reusable RAM buffer -> Zero Disk I/O, no RAM growth
        buf = bytearray(256 * 1024)
        view = memoryview(buf)

        ctx = ssl.create_default_context()
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "AuraNetStress/2.0 (Zero-Disk-IO Benchmark)"},
        )

        while self.is_running:
            try:
                with urllib.request.urlopen(req, timeout=15, context=ctx) as resp:
                    while self.is_running:
                        chunk_start = time.perf_counter()
                        n = resp.readinto(view)
                        if not n:
                            break

                        with self.lock:
                            self.total_bytes += n
                            self.interval_bytes += n
                            total_gb = self.total_bytes / (1024 ** 3)

                        # Check Auto-Stop GB Target
                        target = self.gb_target.get()
                        if target > 0 and total_gb >= target:
                            self.root.after(0, self._trigger_auto_stop)
                            return

                        # Check Bandwidth Limiter (Token-Bucket Style Sleep)
                        limit_mbps = self.speed_limit.get()
                        if limit_mbps > 0:
                            threads = max(1, self.thread_count.get())
                            per_thread_bps = (limit_mbps * 1_000_000 / 8.0) / threads
                            expected_time = n / per_thread_bps
                            elapsed = time.perf_counter() - chunk_start
                            if expected_time > elapsed:
                                time.sleep(expected_time - elapsed)
            except Exception:
                if self.is_running:
                    time.sleep(1.5)

    def _trigger_auto_stop(self):
        if self.is_running:
            self.toggle_stress()
            self.vibe_lbl.config(text="🎯 ZIEL ERREICHT (Auto-Stop aktiv)", fg=ACCENT_LIME)

    # --- UI TELEMETRY & WAVEFORM LOOP ---
    def _update_ui_loop(self):
        now = time.time()
        dt = now - self.last_tick if self.last_tick else 0.5

        if self.is_running and dt >= 0.5:
            with self.lock:
                ibytes = self.interval_bytes
                self.interval_bytes = 0
                tbytes = self.total_bytes

            mbps = (ibytes * 8.0) / (dt * 1_000_000.0)
            self.current_mbps = mbps
            if mbps > self.peak_mbps:
                self.peak_mbps = mbps

            self.speed_history.append(mbps)
            self.last_tick = now

            # Update Labels
            gb_loaded = tbytes / (1024 ** 3)
            elapsed_total = int(now - self.start_time) if self.start_time else 0
            hrs, rem = divmod(elapsed_total, 3600)
            mins, secs = divmod(rem, 60)

            self.lbl_speed.config(text=f"{mbps:,.2f}")
            self.lbl_gb.config(text=f"{gb_loaded:,.2f}")
            self.lbl_peak.config(text=f"{self.peak_mbps:,.2f}")
            self.lbl_time.config(text=f"{hrs:02d}:{mins:02d}:{secs:02d}")

            if elapsed_total > 0:
                avg_mbps = (tbytes * 8.0) / (elapsed_total * 1_000_000.0)
                self.lbl_avg.config(text=f"Ø {avg_mbps:,.2f} Mbit/s")

            self.vibe_lbl.config(text=get_vibe_status(mbps, True))
            self._draw_graph()

        elif not self.is_running:
            self.lbl_speed.config(text="0.00")
            self.vibe_lbl.config(text=get_vibe_status(0, False))

        self.root.after(500, self._update_ui_loop)

    def _draw_graph(self):
        self.canvas.delete("all")
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        if w < 20 or h < 20:
            return

        # Subtle background grid lines
        for i in range(1, 4):
            y = h * (i / 4.0)
            self.canvas.create_line(0, y, w, y, fill="#191928", dash=(4, 4))

        max_val = max(max(self.speed_history), 10.0) * 1.15
        pts = []
        n = len(self.speed_history)
        for idx, val in enumerate(self.speed_history):
            x = (idx / (n - 1)) * w
            y = h - ((val / max_val) * (h - 16)) - 4
            pts.extend([x, y])

        if len(pts) >= 4:
            # Polygon Fill under curve
            poly_pts = [0, h] + pts + [w, h]
            self.canvas.create_polygon(
                poly_pts, fill="#132A3E", outline="", smooth=True
            )
            # Neon Cyan Top Line
            self.canvas.create_line(
                pts, fill=ACCENT_CYAN, width=2.5, smooth=True
            )


if __name__ == "__main__":
    root = tk.Tk()
    app = AuraNetStressApp(root)
    root.mainloop()
