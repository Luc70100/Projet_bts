from gpiozero import Button, PWMOutputDevice
import time

# Configuration du haut-parleur
speaker = PWMOutputDevice(4)  # Utilise gpiozero pour le contrôle du PWM

# Fréquences pour l'alarme (en Hz)
tone1 = 1000  # 1er ton
tone2 = 1500  # 2ème ton

# Durée de chaque ton (en secondes)
tone_duration = 0.1

# Combien de fois répéter l'alarme
repetitions = 10

for _ in range(repetitions):
    speaker.frequency = tone1
    speaker.value = 0.1

    time.sleep(tone_duration)
    
    speaker.frequency = tone2
    speaker.value = 0.1

    time.sleep(tone_duration)


# Arrêter le son
speaker.off()
