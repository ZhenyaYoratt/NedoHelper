import datetime

def log(message, level="info"):
    """Логирует сообщение с уровнем."""
    levels = {"info": "[INFO]", "warning": "[WARNING]", "error": "[ERROR]"}
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    level_tag = levels.get(level, "[INFO]")
    formatted_message = f"{timestamp} {level_tag} {message}"
    print(formatted_message)
    with open("system_helper.log", "a") as log_file:
        log_file.write(formatted_message + "\n")
