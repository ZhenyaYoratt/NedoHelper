SETTINGS = {
    "scan_paths": ["C:\\", "D:\\"],
    "admin_mode": False,
    "log_file": "system_helper.log"
}

def get_setting(key):
    return SETTINGS.get(key, None)

def set_setting(key, value):
    SETTINGS[key] = value
