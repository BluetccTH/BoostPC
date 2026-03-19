import customtkinter as ctk
import psutil
import threading
import time

try:
    import pynvml
    pynvml.nvmlInit()
    GPU_AVAILABLE = True
except:
    GPU_AVAILABLE = False

def build_dashboard(parent, app):
    parent.grid_columnconfigure(0, weight=1)
    parent.grid_rowconfigure(0, weight=1)

    frame = ctk.CTkFrame(parent, fg_color="#02122f")
    frame.pack(fill="both", expand=True, padx=20, pady=20)

    canvas_size = 300
    canvas = ctk.CTkCanvas(frame, width=canvas_size, height=canvas_size, bg="#02122f", highlightthickness=0)
    canvas.pack(pady=20)

    # Background circles
    canvas.create_oval(20, 20, canvas_size-20, canvas_size-20, outline="#3c8fe6", width=15)
    canvas.create_oval(40, 40, canvas_size-40, canvas_size-40, outline="#33e6ff", width=15)
    canvas.create_oval(60, 60, canvas_size-60, canvas_size-60, outline="#ffcc00", width=15)

    # Arcs for CPU, RAM, GPU
    cpu_arc = canvas.create_arc(20, 20, canvas_size-20, canvas_size-20, start=90, extent=0, outline="#ff5555", width=15, style="arc")
    ram_arc = canvas.create_arc(40, 40, canvas_size-40, canvas_size-40, start=90, extent=0, outline="#55ff55", width=15, style="arc")
    gpu_arc = canvas.create_arc(60, 60, canvas_size-60, canvas_size-60, start=90, extent=0, outline="#ffff55", width=15, style="arc")

    # Labels
    cpu_label = ctk.CTkLabel(frame, text="CPU: 0%", font=ctk.CTkFont(size=16, weight="bold"))
    cpu_label.pack(pady=5)
    ram_label = ctk.CTkLabel(frame, text="RAM: 0%", font=ctk.CTkFont(size=16, weight="bold"))
    ram_label.pack(pady=5)
    gpu_label = ctk.CTkLabel(frame, text="GPU: 0%", font=ctk.CTkFont(size=16, weight="bold"))
    gpu_label.pack(pady=5)

    cpu_val = [0.0]
    ram_val = [0.0]
    gpu_val = [0.0]

    def lerp(a, b, t):
        return a + (b - a) * t

    def get_gpu_usage():
        if GPU_AVAILABLE:
            try:
                handle = pynvml.nvmlDeviceGetHandleByIndex(0)
                return pynvml.nvmlDeviceGetUtilizationRates(handle).gpu
            except:
                return 0
        return 0

    def update_graph():
        target_cpu = psutil.cpu_percent()
        target_ram = psutil.virtual_memory().percent
        target_gpu = get_gpu_usage()

        cpu_val[0] = lerp(cpu_val[0], target_cpu, 0.1)
        ram_val[0] = lerp(ram_val[0], target_ram, 0.1)
        gpu_val[0] = lerp(gpu_val[0], target_gpu, 0.1)

        canvas.itemconfig(cpu_arc, extent=-cpu_val[0]*3.6)
        canvas.itemconfig(ram_arc, extent=-ram_val[0]*3.6)
        canvas.itemconfig(gpu_arc, extent=-gpu_val[0]*3.6)

        cpu_label.configure(text=f"CPU: {int(cpu_val[0])}%")
        ram_label.configure(text=f"RAM: {int(ram_val[0])}%")
        gpu_label.configure(text=f"GPU: {int(gpu_val[0])}%")

        frame.after(100, update_graph)

    update_graph()