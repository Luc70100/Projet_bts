from gpiozero import PWMOutputDevice
import time

# Configuration de la broche GPIO (ex: GPIO 17)
GPIO_PIN = 4

# Initialisation du GPIO avec modulation de fréquence
speaker = PWMOutputDevice(GPIO_PIN)

def set_frequency(frequency):
    """Définit la fréquence du signal PWM pour le haut-parleur."""
    if frequency > 0:
        speaker.frequency = frequency
        speaker.value = 0.5  # Définit un rapport cyclique de 50%
        print(f"Haut-parleur activé à {frequency} Hz")
    else:
        speaker.off()
        print("Haut-parleur désactivé")

try:
    while True:
        command = input("Entrez une fréquence en Hz (0 pour éteindre, 'exit' pour quitter) : ")
        if command == "exit":
            break
        try:
            freq = float(command)
            set_frequency(freq)
        except ValueError:
            print("Veuillez entrer un nombre valide.")
except KeyboardInterrupt:
    print("\nInterruption détectée. Arrêt du programme.")
finally:
    speaker.off()
    print("GPIO nettoyé.")
