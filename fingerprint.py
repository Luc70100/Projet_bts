# fingerprint.py

import time
from pyfingerprint.pyfingerprint import PyFingerprint
from db import enregistrer_empreinte, comparer_empreinte
from mail import port,smtp_server,login,password,sender_email,receiver_email,message,smtplib
from lcd_display import scroll_text,clear,display_message
tentative=0
def init_sensor():
    try:
        f = PyFingerprint("/dev/ttyAMA0", 57600, 0xFFFFFFFF, 0x00000000)
        if not f.verifyPassword():
            raise ValueError("Mot de passe du capteur incorrect !")
        return f
    except Exception as e:
        print(f"?? Erreur lors de l'initialisation du capteur: {e}")
        exit(1)

def enroll_fingerprint(f):
    print("👉 Place ton doigt sur le capteur pour l'enregistrer...")
    display_message("Poser le doigt",1)
    while not f.readImage():
        pass
    print("✅ Empreinte capturée !")
    
    f.convertImage(0x01)
    characteristics = f.downloadCharacteristics(0x01)
    fingerprint_data = bytearray(characteristics)
    nom = None
    prenom = None
    id=enregistrer_empreinte(fingerprint_data, nom, prenom)
    clear()
    display_message("Empreinte Prise",1)
    print("✅ Empreinte enregistrée.")
    return id

def verify_fingerprint(f):
    global tentative
    time.sleep(2)
    clear()
    scroll_text("Place ton doigt",1)
    while not f.readImage():
        pass
    clear()
    f.convertImage(0x01)
    new_characteristics = f.downloadCharacteristics(0x01)

    # Comparaison avec la base de données
    match, score, user_id, grade, nom, prenom = comparer_empreinte(f, bytearray(new_characteristics))

    if match:
        print(f"✅✅ MATCH ! L'empreinte correspond à l'ID {user_id} nommer {nom} {prenom} qui a le grade {grade} (Score : {score})")
        scroll_text(f"Bonjour {nom},{prenom}",1)
        tentative=0       
        return match, score, user_id, grade, nom, prenom
    else:
        print(f"❌ PAS DE MATCH ! (Score : {score})")
        tentative+=1
        restant = 10 - tentative 
        print(f"empreinte non reconnue il reste plus que {restant} avant alerte")
        

        scroll_text("empreinte non reconnue!!",1)
        scroll_text(f"tentative restante {restant}",2)
        if tentative >= 10 :
            with smtplib.SMTP(smtp_server, port) as server:
                server.starttls()  # Sécuriser la connexion
                server.login(login, password)
                server.sendmail(sender_email, receiver_email, message.as_string())
            print('Envoyé')
        return None,None,None,None,None,None


def addByAdmin(f):
    result = verify_fingerprint(f)
    if result:
        match, score, user_id, grade, nom, prenom = result
        if grade == 2 :
            print("presenter le doigt")
            id=enroll_fingerprint(f)
            return id
        else :
            print("veuiller ressayer avec une personne administrateur")
            return None
