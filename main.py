import time
from lcddriver import lcd
from lcd_display import display_message, scroll_text, clear
from door_control import check_door_status, open_door
from speaker import play_sound
from config import BUTTON1_PIN, BUTTON2_PIN, speaker, button1, button2
from gpio_setup import setup_gpio
from fingerprint import init_sensor, enroll_fingerprint, verify_fingerprint, addByAdmin,delByAdmin
from db import creationuser
from log import logopen, logfile
import requests

logfile()

# Variables pour gérer les menus
menu = 0
last_action_time = time.time()  # Temps de la dernière action

def menu_actions(menu):
    clear()
    if menu == 1:
        scroll_text("Menu: Ajouter doigt", line=1)
        display_message("Appuyez sur B", line=2)
    elif menu == 2:
        scroll_text("Menu: Ouverture", line=1)
        display_message("Appuyez sur B", line=2)
    elif menu == 3:
        scroll_text("Menu: Supprimer", line=1)
        display_message("Appuyez sur B", line=2)

def handle_function(menu, sensor):
    global last_action_time  # Utiliser la variable globale
    if menu == 1:
        id = addByAdmin(sensor)
        if id is not None:
            clear()
            scroll_text("Creation de l'utilisateur...", line=1)
            time.sleep(2)  # Simule l'ajout d'un doigt
            user, password = creationuser(id)
            clear()
            while not button1.is_pressed and not button2.is_pressed:
                display_message(f"id:{user}", 1)
                display_message(f"mdp:{password}", 2)
                last_action_time = time.time()  # Mettre à jour le temps de la dernière action
        else:
            display_message("Error", line=1)
    elif menu == 2:
        display_message("Ouverture...", line=1)
        result = verify_fingerprint(sensor)
        if result:
            match = result[0]
        if match:
            requests.get("http://admin:Zx23-Zx81@localhost:25000/service/program/trigger?id=1") #requette pour cree le signet
            open_door()
            clear()
            display_message("Porte Ouvert",1)
            logopen(result[2])
            time.sleep(30) #on attend que la personne se serve avant de check la fermeture 
            check_door_status(speaker)  # Vérifie l'état de la porte après ouverture/fermeture
            time.sleep(5)  # Délai avant l'affichage du message
            last_action_time = time.time()  # Mettre à jour le temps de la dernière action
    elif menu == 3:
        display_message("Suppression...", line=1)
        delByAdmin(sensor)
        time.sleep(2)  # Simule la suppression d'un utilisateur
        last_action_time = time.time()  # Mettre à jour le temps de la dernière action

# Boucle principale
display_message(" Bienvenus chez", 1)
display_message("    Jet1Oeil", 2)

while True:
    sensor = init_sensor()

    # Détection du changement d'état du bouton 2 (pour changer de menu)
    if button2.is_pressed:
        menu = menu + 1 if menu < 3 else 1  # Cycle entre les menus 1, 2 et 3
        menu_actions(menu)  # Afficher le menu correspondant
        last_action_time = time.time()  # Mettre à jour le temps de la dernière action
        time.sleep(0.2)  # Anti-rebond simple

    # Détection du changement d'état du bouton 1 (pour valider une action)
    if button1.is_pressed:
        clear()
        handle_function(menu, sensor)  # Exécute la fonction du menu actuel
        menu_actions(menu)  # Retour au menu après l'action
        last_action_time = time.time()  # Mettre à jour le temps de la dernière action

    # Vérifier si 3 minutes se sont écoulées sans action
    if time.time() - last_action_time > 180:  # 180 secondes = 3 minutes
        clear()
        display_message(" Bienvenus chez", 1)
        display_message("    Jet1Oeil", 2)
        last_action_time = time.time()  # Mettre à jour le temps de la dernière action

    # Petite pause pour limiter la charge processeur
    time.sleep(0.1)
