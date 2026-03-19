import time
import psutil
import os

def boost_cpu():
    # Placeholder: ปรับ priority process ปัจจุบัน
    p = psutil.Process(os.getpid())
    try:
        p.nice(psutil.HIGH_PRIORITY_CLASS)
    except:
        pass
    time.sleep(0.2)

def set_high_performance_power_plan():
    # Placeholder: Windows High Performance
    try:
        os.system("powercfg /setactive SCHEME_MIN")
    except:
        pass
    time.sleep(0.2)