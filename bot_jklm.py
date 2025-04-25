# JKLM.fun Bot - Simplified Version
# Auteur/Author: 23R
# Créé/Created: April 2025
# Description (FR): Bot automatisé pour le jeu JKLM.fun, utilisant Selenium pour simuler la saisie de mots.
#                   Version simplifiée avec boutons "Lancer" et "Arrêter". 
# Description (EN): Automated bot for JKLM.fun game, using Selenium to simulate word input.
#                   Simplified version with "Start" and "Stop" buttons. 
# Dépendances/Requirements: Python 3.8+, selenium, tkinter, Brave Browser, ChromeDriver

import tkinter as tk
from tkinter import messagebox, filedialog
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import random
import threading
import traceback

# Variables globales pour l'état du bot / Global variables for bot state
form_data = {}
used_words = []
bot_thread = None
game_driver = None
bot_running = False
bot_launched = False


def lancer_bot(data, log_widget):
    """
    FR: Lance le bot pour automatiser la saisie de mots dans JKLM.fun.
        Lit une liste de mots, se connecte au lobby, et entre des mots selon la syllabe.
    EN: Starts the bot to automate word input in JKLM.fun.
        Reads a wordlist, joins the game lobby, and inputs words based on the syllable.

    Args:
        data (dict): Contient pseudo, code lobby, chemin de la liste de mots / Contains username, lobby code, wordlist path.
        log_widget (tk.Text): Affiche les logs du bot / Displays bot logs.
    """
    global game_driver, bot_running, bot_launched
    words_list = []
    common_misspelled_letters = 'abcdefgiorml'

    # FR: Charge et nettoie la liste de mots / EN: Loads and cleans the wordlist
    try:
        with open(data['wordlist_path'], 'r', encoding='utf-8') as file:
            words = file.readlines()
        for word in words:
            word = word.replace('Ã±', 'n').replace('ñ', 'n').strip()
            words_list.append(word)
        words_list.sort(key=len)
    except Exception as e:
        messagebox.showerror("Erreur/Error", f"Erreur lecture fichier/File read error: {e}")
        bot_running = False
        bot_launched = False
        return

    # FR: Configure Selenium avec Brave / EN: Set up Selenium with Brave
    try:
        driver_service = Service('C:/Users/mauri/Documents/chromedriver-win64/chromedriver.exe')
        chrome_options = Options()
        chrome_options.binary_location = "C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe"
        chrome_options.add_argument("--incognito")
        game_driver = webdriver.Chrome(service=driver_service, options=chrome_options)

        # FR: Ouvre le lobby / EN: Open the game lobby
        game_driver.get(f"https://jklm.fun/{data['lobby']}")
        time.sleep(3)

        # FR: Entre le pseudo / EN: Enter username
        input_elements = game_driver.find_elements(By.TAG_NAME, 'input')
        if len(input_elements) < 2:
            raise Exception("Champ pseudo introuvable/Username field not found")

        inputElement = input_elements[1]
        inputElement.clear()
        inputElement.send_keys(data['username'])
        inputElement.send_keys(Keys.ENTER)
        time.sleep(2)

        # FR: Passe à l'iframe du jeu / EN: Switch to game iframe
        try:
            iframe = game_driver.find_element(By.TAG_NAME, 'iframe')
            game_driver.switch_to.frame(iframe)
        except Exception:
            raise Exception("Iframe non trouvé/Iframe not found")

        time.sleep(3)

        # FR: Boucle principale du bot / EN: Main bot loop
        while bot_running:
            try:
                # FR: Attend le tour du joueur / EN: Wait for player's turn
                while not game_driver.find_element(By.CLASS_NAME, 'selfTurn').is_displayed():
                    if not bot_running:
                        break
                    time.sleep(0.2)
                if not bot_running:
                    break

                # FR: Récupère la syllabe / EN: Get the syllable
                try:
                    syl = game_driver.find_element(By.CLASS_NAME, 'syllable').text.lower()
                except Exception:
                    log_widget.insert(tk.END, "Syllabe non lue/Syllable not read\n")
                    log_widget.yview(tk.END)
                    time.sleep(0.5)
                    continue

                # FR: Cherche un mot avec la syllabe / EN: Find a word with the syllable
                x = random.randint(0, len(words_list) - len(words_list) // 4)
                word = None
                for i in range(x, len(words_list)):
                    if syl in words_list[i] and words_list[i] not in used_words:
                        word = words_list[i]
                        used_words.append(word)
                        log_widget.insert(tk.END, f"Mot/Word: {word}\n")
                        log_widget.yview(tk.END)
                        break

                if not word:
                    log_widget.insert(tk.END, f"Aucun mot pour/No word for: {syl}\n")
                    log_widget.yview(tk.END)
                    continue

                # FR: Simule la saisie / EN: Simulate typing
                try:
                    narrowedElement = game_driver.find_element(By.CLASS_NAME, 'selfTurn')
                    inputElement = narrowedElement.find_element(By.TAG_NAME, 'input')
                except Exception:
                    log_widget.insert(tk.END, "Champ saisie introuvable/Input field not found\n")
                    log_widget.yview(tk.END)
                    continue

                time.sleep(random.uniform(0.5, 2))

                # FR: Saisie avec erreurs aléatoires / EN: Type with random typos
                for i in range(len(word)):
                    if not bot_running:
                        break
                    inputElement.send_keys(word[i])
                    time.sleep(random.uniform(0.02, 0.2))
                    if random.randint(1, 70) == 2:
                        n_miss = random.randint(1, 2)
                        for _ in range(n_miss):
                            inputElement.send_keys(random.choice(common_misspelled_letters))
                            time.sleep(0.05)
                        for _ in range(n_miss):
                            inputElement.send_keys(Keys.BACKSPACE)
                            time.sleep(0.1)

                if bot_running:
                    inputElement.send_keys(Keys.ENTER)
                time.sleep(0.5)
            except Exception as e:
                log_widget.insert(tk.END, f"Erreur/Error: {e}\n{traceback.format_exc()}\n")
                log_widget.yview(tk.END)
                break

    except Exception as e:
        log_widget.insert(tk.END, f"Erreur lancement/Start error: {e}\n{traceback.format_exc()}\n")
        log_widget.yview(tk.END)
    finally:
        # FR: Ferme le navigateur / EN: Close the browser
        try:
            if game_driver:
                game_driver.quit()
        except Exception as e:
            log_widget.insert(tk.END, f"Erreur fermeture/Close error: {e}\n")
        bot_running = False
        bot_launched = False


def start_gui():
    """
    FR: Crée l'interface graphique Tkinter simplifiée.
    EN: Sets up the simplified Tkinter GUI.
    """

    def browse_file():
        """FR: Ouvre un sélecteur de fichier pour la liste de mots.
           EN: Opens a file dialog to select the wordlist."""
        file_path = filedialog.askopenfilename(filetypes=[("Fichiers texte/Text files", "*.txt")])
        wordlist_path_var.set(file_path)

    def start_bot():
        """
        FR: Lance le bot après validation des entrées.
        EN: Starts the bot after validating inputs.
        """
        global bot_thread, bot_running, bot_launched
        if bot_launched:
            messagebox.showinfo("Info", "Bot déjà lancé/Bot already running.")
            return

        username = username_entry.get()
        lobby = lobby_entry.get().upper()
        wordlist_path = wordlist_path_var.get()

        # FR: Validation des entrées / EN: Input validation
        if not (2 <= len(username) <= 14):
            messagebox.showerror("Erreur/Error", "Pseudo: 2-14 caractères/Username: 2-14 characters.")
            return
        if not (len(lobby) == 4 and lobby.isalpha()):
            messagebox.showerror("Erreur/Error", "Lobby: 4 lettres/Lobby: 4 letters.")
            return
        if not wordlist_path:
            messagebox.showerror("Erreur/Error", "Choisir fichier mots/Select wordlist file.")
            return

        data = {
            'username': username,
            'lobby': lobby,
            'wordlist_path': wordlist_path
        }

        bot_running = True
        bot_launched = True
        bot_thread = threading.Thread(target=lancer_bot, args=(data, log_widget))
        bot_thread.start()

    def stop_bot():
        """FR: Arrête le bot et réinitialise son état.
           EN: Stops the bot and resets its state."""
        global bot_running, bot_launched
        if bot_running:
            bot_running = False
            bot_launched = False
            messagebox.showinfo("Arrêt/Stop", "Bot arrêté/Bot stopped.")
        else:
            messagebox.showinfo("Arrêt/Stop", "Bot non actif/Bot not running.")

    # FR: Configure la fenêtre Tkinter / EN: Set up Tkinter window
    root = tk.Tk()
    root.title("JKLM.fun Bot - by 23R")

    # FR: Éléments de l'interface / EN: GUI elements
    tk.Label(root, text="Pseudo/Username:").grid(row=0, column=0, padx=10, pady=5, sticky='e')
    username_entry = tk.Entry(root)
    username_entry.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(root, text="Code lobby (4 lettres/letters):").grid(row=1, column=0, padx=10, pady=5, sticky='e')
    lobby_entry = tk.Entry(root)
    lobby_entry.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(root, text="Fichier mots/Wordlist:").grid(row=2, column=0, padx=10, pady=5, sticky='e')
    wordlist_path_var = tk.StringVar()
    tk.Entry(root, textvariable=wordlist_path_var, width=30).grid(row=2, column=1, padx=10, pady=5)
    tk.Button(root, text="Parcourir/Browse", command=browse_file).grid(row=2, column=2, padx=5, pady=5)

    tk.Button(root, text="Lancer/Start", bg="green", fg="white", command=start_bot).grid(row=3, column=1, pady=15)
    tk.Button(root, text="Arrêter/Stop", bg="red", fg="white", command=stop_bot).grid(row=4, column=1, pady=15)

    log_widget = tk.Text(root, height=8, width=60)
    log_widget.grid(row=5, column=0, columnspan=3, padx=10, pady=5)

    root.mainloop()


if __name__ == "__main__":
    start_gui()
