try:
    import pynvml
    pynvml.nvmlInit()
    GPU_AVAILABLE = True
except:
    GPU_AVAILABLE = False

import time

def optimize_gpu():
    if GPU_AVAILABLE:
        handle = pynvml.nvmlDeviceGetHandleByIndex(0)
        # Placeholder: อ่าน GPU load
        util = pynvml.nvmlDeviceGetUtilizationRates(handle).gpu
    time.sleep(0.2)