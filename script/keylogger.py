import time
from pynput import keyboard
from sentiments import analyser_sentiment, enregistrer_phrase

class KeyLogger:
    def __init__(self, file_path="log.txt", thresholds=None):
        self.file_path = file_path
        self.thresholds = thresholds or {'fast': 0.2, 'slow': 0.8}  # Seuils par défaut
        self.phrase_en_cours = []
        self.sentiment_scores = []
        self.typing_speeds = []
        self.emotion_flags = []
        self.last_time = None

    def traiter_touche(self, touche):
        try:
            current_time = time.time()
            if self.last_time is not None:
                typing_speed = current_time - self.last_time
                self.typing_speeds.append(typing_speed)
                self.analyser_vitesse_de_frappe(typing_speed)

            self.last_time = current_time

            if hasattr(touche, 'char') and touche.char is not None:
                self.phrase_en_cours.append(touche.char)

            if touche.char in ".!?":
                phrase_complete = "".join(self.phrase_en_cours).strip()
                if phrase_complete:
                    analyser_sentiment(phrase_complete, self.sentiment_scores)
                    enregistrer_phrase(phrase_complete, self.file_path)
                self.phrase_en_cours.clear()
        
        except AttributeError:
            if touche == keyboard.Key.space:
                self.phrase_en_cours.append(" ")
            elif touche == keyboard.Key.enter:
                self.phrase_en_cours.append("\n")
            elif touche == keyboard.Key.backspace and self.phrase_en_cours:
                self.phrase_en_cours.pop()
            elif touche == keyboard.Key.esc:
                print("\n[INFO] Arrêt du keylogger...")
                return False

    def analyser_vitesse_de_frappe(self, typing_speed):
        """Analyse la vitesse de frappe pour détecter l'émotion."""
        if typing_speed < self.thresholds['fast']:
            self.emotion_flags.append("Enervé")
        elif typing_speed > self.thresholds['slow']:
            self.emotion_flags.append("Fatigué ou Chill")
        else:
            self.emotion_flags.append("Neutre")

    def start_keylogger(self):
        with keyboard.Listener(on_press=self.traiter_touche) as ecouteur_clavier:
            ecouteur_clavier.join()