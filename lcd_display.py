# lcd_display.py

import lcddriver
import time
from config import LCD

# Initialisation de l'�cran LCD
lcd = lcddriver.lcd()
lcd.lcd_clear()
lcd.lcd_display_string("test",1)

def display_message(message, line=1):
    lcd.lcd_display_string(message[:16], line)  # Affiche au maximum 16 caract�res sur une ligne

def scroll_text(text, line=1):
    text = text.ljust(16)  # Ajoute des espaces pour une longueur minimale
    for offset in range(len(text) - 15):
        display_message(text[offset:offset + 16], line)
        time.sleep(0.3)  # Ajuster la vitesse du d�filement

def clear():
    lcd.lcd_clear()        
