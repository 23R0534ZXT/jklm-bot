# JKLM.fun Bot

**FR** : Un bot Python pour automatiser le jeu de mots [JKLM.fun](https://jklm.fun), créé par **23R**.  
**EN** : A Python bot to automate the JKLM.fun word game, built by **23R**.

Ce projet utilise **Selenium** pour simuler la saisie de mots et **Tkinter** pour une interface graphique simple.  
This project uses **Selenium** for typing simulation and **Tkinter** for a simple GUI.

---

## Fonctionnalités / Features

- **Interface intuitive / Intuitive GUI**  
  Champs pour pseudo, code lobby, sélection de la liste de mots, avec boutons "Lancer" et "Arrêter".

- **Saisie humaine / Human-like typing**  
  Délais aléatoires et corrections d’erreurs pour imiter un joueur réel.

- **Logs détaillés / Detailed logs**  
  Suivi des actions et erreurs pour un débogage plus facile.

- **Support de liste de mots / Wordlist support**  
  Utilise un fichier texte personnalisé (un mot par ligne).

---

## Prérequis / Requirements

- Python 3.8+
- Brave Browser + ChromeDriver
- Bibliothèques : `selenium`, `tkinter`

Installez les dépendances / Install dependencies:
```bash
pip install -r requirements.txt
```

## Installation / Setup

1. Clonez le dépôt / Clone the repo:
   ```bash
   git clone https://github.com/yourusername/jklm-bot.git
   ```
2. Mettez à jour le chemin de ChromeDriver dans `bot_jklm.py`.
3. Vérifiez que Brave Browser est installé.
4. Préparez une liste de mots (ex. : `wordlist.txt`, un mot par ligne).
5. Lancez le bot / Run the bot:
   ```bash
   python bot_jklm.py
   ```

## Utilisation / Usage

1. Ouvrez l’interface / Open the GUI.
2. Entrez un pseudo (2-14 caractères) / Enter a username (2-14 characters).
3. Entrez un code lobby (4 lettres) / Enter a 4-letter lobby code.
4. Sélectionnez un fichier de mots (.txt) / Select a wordlist file (.txt).
5. Cliquez sur **Lancer** pour démarrer / Click **Start** to run.
6. Cliquez sur **Arrêter** pour arrêter / Click **Stop** to stop.

## Notes

- **FR** : Ce projet est juste pour s’amuser avec l’automatisation, pas pour tricher. Utilisez-le de manière responsable.  
- **EN** : This project is for fun with automation, not for cheating. Use it responsibly.
- Assurez-vous que les chemins pour ChromeDriver et Brave sont corrects / Make sure ChromeDriver and Brave paths are correct.

## Licence / License

Sous **licence MIT**. Voir [LICENSE](LICENSE) pour plus d’infos.  
Under **MIT License**. See [LICENSE](LICENSE) for details.

## Auteur / Author

**23R** 
