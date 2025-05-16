# config.py
from gpiozero import Button, PWMOutputDevice
# Configuration du capteur
PORT = "/dev/ttyAMA0"
BAUD_RATE = 57600

# Configuration MySQL
MYSQL_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "Zx223-Zx81",
    "database": "projetbts"
}

# Configuration des GPIO
BUTTON1_PIN = 27  # Bouton pour valider
BUTTON2_PIN = 22   # Bouton pour changer de menu
DOOR_CONTACT_PIN = 25  # Contacteur de porte
RELAY_PIN = 23  # Relais pour commander la porte
SPEAKER_PIN = 4  # Broche o� le haut-parleur est connect�

# Configuration de l'�cran LCD (si tu veux personnaliser plus tard)
LCD = None  # Ce sera configur� dans lcd_display.py

# Initialisation du PWM
speaker = PWMOutputDevice(4)  # Utilise gpiozero pour le contrôle du PWM

# Définition des boutons
button1 = Button(BUTTON1_PIN, pull_up=False)
button2 = Button(BUTTON2_PIN, pull_up=False)