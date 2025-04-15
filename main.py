# main.py
import time
from lcddriver import lcd 
from gpiozero import Button, PWMOutputDevice
#from fingerprint import init_sensor, enroll_fingerprint, verify_fingerprint,addByAdmin
from lcd_display import display_message, scroll_text
from door_control import check_door_status, open_door
from speaker import play_sound
from config import BUTTON1_PIN, BUTTON2_PIN
from gpio_setup import setup_gpio
from lcd_display import clear
from ajouteverifadminforadd import init_sensor,enroll_fingerprint, verify_fingerprint,addByAdmin

#setup_gpio()
# Initialisation du PWM
speaker = PWMOutputDevice(4)  # Utilise gpiozero pour le contrôle du PWM

# Définition des boutons
button1 = Button(BUTTON1_PIN,pull_up=False)
button2 = Button(BUTTON2_PIN,pull_up=False)

# Variables pour gérer les menus
menu = 0

def menu_actions(menu):
    clear()
    if menu == 1:
        clear()
        scroll_text("Menu: Ajouter doigt", line=1)
        display_message("Appuyez sur B", line=2)
    elif menu == 2:
        clear()
        scroll_text("Menu: Ouverture", line=1)
        display_message("Appuyez sur B", line=2)
    elif menu == 3:
        clear()
        scroll_text("Menu: Supprimer", line=1)
        display_message("Appuyez sur B", line=2)


def handle_function(menu, sensor):
    if menu == 1:
        addByAdmin(sensor)
        display_message("Ajout en cours...", line=1)
        time.sleep(2)  # Simule l'ajout d'un doigt
    elif menu == 2:
        display_message("Ouverture...", line=1)
        result = verify_fingerprint(sensor)
        if result:
            match = result[0]
        if match == True:   
            open_door()
            #check_door_status(speaker)  # Vérifie l'état de la porte après ouverture/fermeture
            time.sleep(5)  # Délai avant l'affichage du message     
    elif menu == 3:
        display_message("Suppression...", line=1)
        time.sleep(2)  # Simule la suppression d'un utilisateur        
# Boucle principale
        
display_message(" Bienvenus chez",1)
display_message("    Jet1Oeil",2) 

while True:
    sensor = init_sensor()
    #print(button1)
    #print(button2)
    # Détection du changement d'état du bouton 2 (pour changer de menu)  
    if button2.is_pressed:
        print("je change")
        menu = menu + 1 if menu < 3 else 1  # Cycle entre les menus 1, 2 et 3
        menu_actions(menu)  # Afficher le menu correspondant
        time.sleep(0.2)  # Anti-rebond simple
        
    # Détection du changement d'état du bouton 1 (pour valider une action)
    if button1.is_pressed:
        print("je rentre")
        clear()
        handle_function(menu, sensor)  # Exécute la fonction du menu actuel
        menu_actions(menu)  # Retour au menu après l'action

    # Petite pause pour limiter la charge processeur
    time.sleep(0.1)
