# gpio_setup.py

from gpiozero import Button, PWMOutputDevice
from config import BUTTON1_PIN, BUTTON2_PIN, DOOR_CONTACT_PIN, RELAY_PIN, SPEAKER_PIN

def setup_gpio():
    
    # Définition du contacteur de porte (si nécessaire, vous pouvez ajouter une logique ici pour l'utiliser)
    door_contact = Button(DOOR_CONTACT_PIN)  # Si c'est un simple bouton
    # Pour un capteur de porte qui envoie un signal de type HIGH/LOW en continu, utilisez Button ou DigitalInputDevice.

    # Définition du relais pour ouvrir/fermer la porte
    relay = PWMOutputDevice(RELAY_PIN)  # Utilise un PWMOutputDevice si besoin de contrôle en PWM, sinon DigitalOutputDevice si c'est juste ON/OFF.
    relay.off()  # Commence avec le relais éteint (OFF)

    # Définition du haut-parleur pour générer un son (PWM)
    speaker = PWMOutputDevice(SPEAKER_PIN)
    speaker.off()  # Commence avec le haut-parleur éteint

    return door_contact, relay, speaker  # Retourne les objets pour un usage ultérieur
