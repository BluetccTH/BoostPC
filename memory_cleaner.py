import psutil
import time
import os

def clean_ram():
    # Placeholder: เคลียร์ RAM แบบ safe
    if os.name == "nt":
        os.system("echo Freeing RAM")  # สามารถใส่ Win32 API ต่อได้
    time.sleep(0.2)

def clean_temp():
    # Placeholder: เคลียร์ Temp folder
    temp_dirs = [os.environ.get("TEMP"), os.environ.get("TMP")]
    for d in temp_dirs:
        if d and os.path.exists(d):
            for f in os.listdir(d):
                try:
                    path = os.path.join(d, f)
                    if os.path.isfile(path):
                        os.remove(path)
                except:
                    pass
    time.sleep(0.2)