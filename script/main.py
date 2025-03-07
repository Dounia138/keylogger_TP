import threading
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from keylogger import KeyLogger
from visualisation import afficher_graphique

def main():
    thresholds = {'fast': 0.1, 'slow': 1.0}
    keylogger = KeyLogger(file_path="log.txt", thresholds=thresholds)
    
    keylogger_thread = threading.Thread(target=keylogger.start_keylogger)
    keylogger_thread.daemon = True
    keylogger_thread.start()

    ani = animation.FuncAnimation(plt.figure(figsize=(10, 5)), afficher_graphique, fargs=(keylogger,), interval=1000)

    plt.show()

if __name__ == "__main__":
    main()
