import customtkinter as ctk
import threading
import time
from modules import system_boost, memory_cleaner, gpu_boost

def build_system_page(parent, app):
    frame = ctk.CTkFrame(parent, fg_color="#02122f")
    frame.pack(fill="both", expand=True, padx=20, pady=20)

    progress_label = ctk.CTkLabel(frame, text=app.t("progress_status"), font=ctk.CTkFont(size=16, weight="bold"))
    progress_label.pack(pady=(10,5))

    progress_bar = ctk.CTkProgressBar(frame, width=450)
    progress_bar.pack(pady=10)

    boost_btn = ctk.CTkButton(frame, text=app.t("boost_button"), width=200)
    boost_btn.pack(pady=10)

    clean_btn = ctk.CTkButton(frame, text=app.t("memory_clean"), width=200)
    clean_btn.pack(pady=10)

    def smooth_progress(target):
        current = progress_bar.get()
        while abs(current - target) > 0.01:
            current += (target - current) * 0.2
            progress_bar.set(current)
            time.sleep(0.02)
        progress_bar.set(target)

    def run_boost():
        app.log(app.t("status_boosting"))
        progress_bar.set(0.0)
        steps = [
            ("Boost CPU", system_boost.boost_cpu),
            ("Set High Performance", system_boost.set_high_performance_power_plan),
            ("Optimize GPU", gpu_boost.optimize_gpu),
            ("Clean Temp Files", memory_cleaner.clean_temp),
            ("Finalize Boost", lambda: time.sleep(0.2))
        ]
        for i, (desc, func) in enumerate(steps, start=1):
            app.log(f"[BOOST] {desc}")
            func()
            smooth_progress(i / len(steps))
        app.log(app.t("status_ready"))
        progress_bar.set(0.0)

    def run_clean():
        app.log(app.t("status_cleaning"))
        progress_bar.set(0.0)
        steps = [
            ("Clean RAM", memory_cleaner.clean_ram),
            ("Clean Temp", memory_cleaner.clean_temp),
            ("Finalize Clean", lambda: time.sleep(0.2))
        ]
        for i, (desc, func) in enumerate(steps, start=1):
            app.log(f"[CLEAN] {desc}")
            func()
            smooth_progress(i / len(steps))
        app.log(app.t("status_ready"))
        progress_bar.set(0.0)

    boost_btn.configure(command=lambda: threading.Thread(target=run_boost, daemon=True).start())
    clean_btn.configure(command=lambda: threading.Thread(target=run_clean, daemon=True).start())