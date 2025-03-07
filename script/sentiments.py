from deep_translator import GoogleTranslator
from nltk.sentiment import SentimentIntensityAnalyzer

analyseur_sentiments = SentimentIntensityAnalyzer()
traducteur = GoogleTranslator(source='fr', target='en')

def analyser_sentiment(texte, sentiment_scores):
    try:
        texte_traduit = traducteur.translate(texte)
        scores_sentiments = analyseur_sentiments.polarity_scores(texte_traduit)
        score_global = scores_sentiments['compound']
        sentiment_scores.append(score_global)

        afficher_analyse_sentiment(texte, score_global)
    except Exception as e:
        print(f"[ERREUR] Impossible d'analyser le texte : {e}")

def afficher_analyse_sentiment(texte, score_global):
    print("\n[ANALYSE DES SENTIMENTS]")
    print(f"Texte : {texte}")
    if score_global >= 0.05:
        print(f"[POSITIF] Score : {score_global:.2f}")
    elif score_global <= -0.05:
        print(f"[NÉGATIF] Score : {score_global:.2f}")
    else:
        print(f"[NEUTRE] Score : {score_global:.2f}")

def enregistrer_phrase(texte, file_path):
    with open(file_path, "a") as fichier:
        fichier.write(texte + "\n")