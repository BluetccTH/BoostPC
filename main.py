import os
import json
import ctypes
import customtkinter as ctk

from ui.dashboard import build_dashboard
from ui.system_page import build_system_page
from modules import system_boost, memory_cleaner, gpu_boost

APP_NAME = "BoostPC"
STATE_FILE = "config/state.json"

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# ---------------------------
# TRANSLATIONS
# ---------------------------
TRANSLATIONS = {
    "TH": {
        "title": "BoostPC",
        "subtitle": "Safe System Optimizer",
        "dashboard": "แดชบอร์ด",
        "system": "System Boost",
        "boost_button": "เริ่ม Boost",
        "memory_clean": "ล้างแรม",
        "status_boosting": "กำลัง Boost...",
        "status_cleaning": "กำลังเคลียร์แรม...",
        "status_ready": "พร้อมใช้งาน",
        "language_label": "ภาษา / TH-EN-CH",
        "admin_status": "สิทธิ์แอดมิน",
        "admin_yes": "มี",
        "admin_no": "ไม่มี"
    },
    "EN": {
        "title": "BoostPC",
        "subtitle": "Safe System Optimizer",
        "dashboard": "Dashboard",
        "system": "System Boost",
        "boost_button": "Start Boost",
        "memory_clean": "Memory Clean",
        "status_boosting": "Boosting...",
        "status_cleaning": "Cleaning Memory...",
        "status_ready": "Ready",
        "language_label": "Language / TH-EN-CH",
        "admin_status": "Admin Rights",
        "admin_yes": "Yes",
        "admin_no": "No"
    },
    "CH": {
        "title": "BoostPC",
        "subtitle": "安全系统优化",
        "dashboard": "仪表板",
        "system": "系统加速",
        "boost_button": "开始加速",
        "memory_clean": "清理内存",
        "status_boosting": "加速中...",
        "status_cleaning": "清理内存...",
        "status_ready": "可用",
        "language_label": "语言 / TH-EN-CH",
        "admin_status": "管理员权限",
        "admin_yes": "有",
        "admin_no": "无"
    }
}

# ---------------------------
# HELPERS
# ---------------------------
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def load_app_state():
    default_state = {"language": "TH"}
    if not os.path.exists(STATE_FILE):
        return default_state
    try:
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        for key in default_state:
            if key not in data:
                data[key] = default_state[key]
        return data
    except:
        return default_state

def save_app_state(data):
    os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# ---------------------------
# APP
# ---------------------------
class BoostPCApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.app_state = load_app_state()
        self.translations = TRANSLATIONS
        self.current_lang = self.app_state.get("language", "TH")
        self.admin_mode = bool(is_admin())

        self.title(APP_NAME)
        self.geometry("1280x820")
        self.minsize(1100, 700)

        self.sidebar = None
        self.content_frame = None
        self.header_label = None
        self.page_container = None
        self.log_box = None
        self.lang_menu = None

        self.build_ui()
        self.show_page("dashboard")
        self.log(self.t("status_ready"))

    def t(self, key):
        return self.translations.get(self.current_lang, self.translations["TH"]).get(key, key)

    def build_ui(self):
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Sidebar
        self.sidebar = ctk.CTkFrame(self, width=245, corner_radius=0, fg_color="#031a44")
        self.sidebar.grid(row=0, column=0, sticky="nsw")
        self.sidebar.grid_propagate(False)
        self.sidebar.grid_rowconfigure(9, weight=1)

        self.app_title = ctk.CTkLabel(self.sidebar, text=self.t("title"), font=ctk.CTkFont(size=34, weight="bold"), anchor="w")
        self.app_title.grid(row=0, column=0, padx=22, pady=(20, 6), sticky="ew")
        self.app_subtitle = ctk.CTkLabel(self.sidebar, text=self.t("subtitle"), font=ctk.CTkFont(size=22), text_color="#cce2ff", anchor="w")
        self.app_subtitle.grid(row=1, column=0, padx=22, pady=(0,22), sticky="ew")

        # Nav buttons
        self.nav_buttons = {}
        nav_items = [("dashboard", self.t("dashboard")), ("system", self.t("system"))]
        for i, (page_key, label) in enumerate(nav_items, start=2):
            btn = ctk.CTkButton(self.sidebar, text=label, height=38, corner_radius=8,
                                fg_color="#3c8fe6" if page_key=="dashboard" else "#337bc5",
                                hover_color="#4ea0f5",
                                command=lambda p=page_key: self.show_page(p))
            btn.grid(row=i, column=0, padx=18, pady=7, sticky="ew")
            self.nav_buttons[page_key] = btn

        # Language menu
        self.lang_label = ctk.CTkLabel(self.sidebar, text=self.t("language_label"), anchor="w")
        self.lang_label.grid(row=7, column=0, padx=22, pady=(28,8), sticky="ew")
        self.lang_menu = ctk.CTkOptionMenu(self.sidebar, values=["TH","EN","CH"], command=self.change_language, height=32)
        self.lang_menu.set(self.current_lang)
        self.lang_menu.grid(row=8, column=0, padx=18, pady=(0,18), sticky="ew")

        # Admin info
        self.admin_label = ctk.CTkLabel(self.sidebar, text=f"{self.t('admin_status')}: {self.t('admin_yes') if self.admin_mode else self.t('admin_no')}", anchor="w")
        self.admin_label.grid(row=10, column=0, padx=22, pady=(0,8), sticky="ew")

        # Main content
        self.content_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="#02122f")
        self.content_frame.grid(row=0, column=1, sticky="nsew", padx=0, pady=0)
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_rowconfigure(1, weight=1)

        # Header
        self.header_frame = ctk.CTkFrame(self.content_frame, fg_color="#071d4a", corner_radius=18)
        self.header_frame.grid(row=0, column=0, sticky="ew", padx=18, pady=(18,12))
        self.header_label = ctk.CTkLabel(self.header_frame, text=self.t("dashboard"), font=ctk.CTkFont(size=20, weight="bold"), anchor="w")
        self.header_label.pack(fill="x", padx=20, pady=16)

        # Page container
        self.page_container = ctk.CTkFrame(self.content_frame, fg_color="#02122f", corner_radius=0)
        self.page_container.grid(row=1, column=0, sticky="nsew", padx=10, pady=0)
        self.page_container.grid_columnconfigure(0, weight=1)
        self.page_container.grid_rowconfigure(0, weight=1)

        # Log
        self.log_frame = ctk.CTkFrame(self.content_frame, fg_color="#1a1a1a", corner_radius=18)
        self.log_frame.grid(row=2, column=0, sticky="ew", padx=18, pady=(12,18))
        self.log_box = ctk.CTkTextbox(self.log_frame, height=170, corner_radius=12)
        self.log_box.pack(fill="both", expand=True, padx=14, pady=14)
        self.log_box.configure(state="disabled")

    def clear_page(self):
        for widget in self.page_container.winfo_children():
            widget.destroy()

    def show_page(self, page_name):
        self.clear_page()
        for key, btn in self.nav_buttons.items():
            btn.configure(fg_color="#3c8fe6" if key==page_name else "#337bc5")
        if page_name=="dashboard":
            self.header_label.configure(text=self.t("dashboard"))
            build_dashboard(self.page_container, self)
        elif page_name=="system":
            self.header_label.configure(text=self.t("system"))
            build_system_page(self.page_container, self)

    def change_language(self,new_lang):
        self.current_lang=new_lang
        self.app_state["language"]=new_lang
        save_app_state(self.app_state)
        for widget in self.winfo_children():
            widget.destroy()
        self.nav_buttons={}
        self.build_ui()
        self.show_page("dashboard")
        self.log(self.t("status_ready"))

    def log(self,msg):
        self.log_box.configure(state="normal")
        self.log_box.insert("end", msg+"\n")
        self.log_box.see("end")
        self.log_box.configure(state="disabled")

if __name__=="__main__":
    app=BoostPCApp()
    app.mainloop()