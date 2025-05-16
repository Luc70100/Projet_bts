from db import enregistrer_empreinte, comparer_empreinte, listeruser
from config import BUTTON1_PIN, BUTTON2_PIN
from gpiozero import Button
import time

button1 = Button(BUTTON1_PIN, pull_up=False)
button2 = Button(BUTTON2_PIN, pull_up=False)

listuser = []
n = 0
users = listeruser()

for i in range(len(users)):
    if users[i][0]:
        listuser.append(users[i][0])
print(listuser)

while not button2.is_pressed:
    if button1.is_pressed:
        if n < len(listuser):
            print("Utilisateur sélectionné :", listuser[n])
            n += 1
            time.sleep(1)
        else:
            print("Fin de la liste des utilisateurs.")
            break

# S’assurer que n est valide avant l’affichage
if n < len(users):
    print(users[n][1])
else:
    print("Index hors limites, aucun utilisateur sélectionné.")
