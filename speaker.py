# utils.py
from config import SPEAKER_PIN

def play_sound(pwm):
    pwm.start(50)  # D�marre le son � 50% de la largeur d'impulsion
