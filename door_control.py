# door_control.py

import time
from gpiozero import Button, PWMOutputDevice
# Nous utilisons les objets fournis par gpiozero
from config import DOOR_CONTACT_PIN, RELAY_PIN, SPEAKER_PIN

def check_door_status(speaker):
    # Vérification du contacteur de porte
    door_contact = Button(DOOR_CONTACT_PIN)  # Utilisation de Button pour le contacteur
    if door_contact.is_pressed:  # La porte est ouverte
        print("Ferme la Porte")
        print("Ferme la Porte")
        speaker.frequency = 250  # Démarre le son à 50% de la largeur d'impulsion
        speaker.value = 0.1
        while door_contact.is_pressed:  # Tant que la porte est ouverte
            time.sleep(0.1)  # Petite pause pour éviter de surcharger le CPU

        speaker.off()  # Arrêter le son quand la porte est fermée
        print("A Bientot")
        print("A Bientot")

    else:  # La porte est fermée
        print("A Bientot")
        print("A Bientot")
        speaker.off()  # Arrêter le PWM si la porte est fermée

def open_door():
    relay = PWMOutputDevice(RELAY_PIN)  # Utilisation de PWMOutputDevice pour le relais
    relay.on()  # Ouvrir la porte
    time.sleep(5)  # Simulation de l'ouverture
    relay.off()  # Fermer la porte après l'ouverture
