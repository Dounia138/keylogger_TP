import matplotlib.pyplot as plt

def afficher_graphique(i, keylogger):
    plt.clf()

    # Tracer l'évolution des sentiments
    plt.subplot(2, 1, 1)
    plt.plot(keylogger.sentiment_scores, marker='o', color='b', label='Score de sentiment')
    plt.title("Évolution des Sentiments")
    plt.xlabel("Lignes saisies")
    plt.ylabel("Score de Sentiment")
    plt.axhline(0, color='gray', linestyle='--', linewidth=1)
    plt.legend()

    # Tracer les vitesses de frappe
    plt.subplot(2, 1, 2)
    plt.plot(keylogger.typing_speeds, marker='x', color='r', label='Vitesse de frappe (secondes)')
    plt.title("Vitesse de Frappe")
    plt.xlabel("Index des frappes")
    plt.ylabel("Temps entre les frappes (secondes)")
    plt.legend()

    plt.tight_layout()

    plt.figtext(0.15, 0.85, f"Émotions : {keylogger.emotion_flags[-1] if keylogger.emotion_flags else 'Neutre'}", fontsize=12, color="green")