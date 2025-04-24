# door_control.py

import time
from gpiozero import Button, PWMOutputDevice
# Nous utilisons les objets fournis par gpiozero
from config import DOOR_CONTACT_PIN, RELAY_PIN, SPEAKER_PIN

def check_door_status(speaker):
    # Vérification du contacteur de porte
    # Fréquences pour l'alarme (en Hz)
    tone1 = 1000  # 1er ton
    tone2 = 1500  # 2ème ton
    # Durée de chaque ton (en secondes)
    tone_duration = 0.2
    door_contact = Button(DOOR_CONTACT_PIN)  # Utilisation de Button pour le contacteur
    
    if door_contact.is_pressed:  # La porte est ouverte
        time.sleep(300)
        while door_contact.is_pressed:  # Tant que la porte est ouverte
            speaker.frequency = tone1
            speaker.value = 0.1
            time.sleep(tone_duration)
            speaker.frequency = tone2
            speaker.value = 0.1
            print("porte ouvert")
        speaker.off()  # Arrêter le son quand la porte est fermée
    else:  # La porte est fermée
        speaker.off()  # Arrêter le PWM si la porte est fermée

def open_door():
    relay = PWMOutputDevice(RELAY_PIN)  # Utilisation de PWMOutputDevice pour le relais
    relay.on()  # Ouvrir la porte
    time.sleep(5)  # Simulation de l'ouverture
    relay.off()  # Fermer la porte après l'ouverture
