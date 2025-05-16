# fingerprint.py

import time
from pyfingerprint.pyfingerprint import PyFingerprint
from db import enregistrer_empreinte, comparer_empreinte,listeruser,supprimeruser
from mail import port,smtp_server,login,password,sender_email,receiver_email,message,smtplib
from lcd_display import scroll_text,clear,display_message
from config import button1, button2
from log import debbuginfo, debbugwarning, debbugerror
tentative=0
def init_sensor():
    try:
        f = PyFingerprint("/dev/ttyAMA0", 57600, 0xFFFFFFFF, 0x00000000)
        if not f.verifyPassword():
            raise ValueError("Mot de passe du capteur incorrect !")
        return f
    except Exception as e:
        debbugerror(f"?? Erreur lors de l'initialisation du capteur: {e}")
        exit(1)

def enroll_fingerprint(f):
    debbuginfo("empreint en cour de capture")
    clear()
    display_message("Poser le doigt",1)
    while not f.readImage():
        pass
    debbuginfo("✅ Empreinte capturée !")
    
    f.convertImage(0x01)
    characteristics = f.downloadCharacteristics(0x01)
    fingerprint_data = bytearray(characteristics)
    nom = None
    prenom = None
    id=enregistrer_empreinte(fingerprint_data, nom, prenom)
    clear()
    display_message("Empreinte Prise",1)
    debbuginfo("✅ Empreinte enregistrée.")
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
        debbuginfo(f"✅✅ MATCH ! L'empreinte correspond à l'ID {user_id} nommer {nom} {prenom} qui a le grade {grade} (Score : {score})")
        scroll_text(f"Bonjour {nom},{prenom}",1)
        tentative=0       
        return match, score, user_id, grade, nom, prenom
    else:
        debbugwarning(f"❌ PAS DE MATCH ! (Score : {score})")
        tentative+=1
        restant = 10 - tentative 
        debbugwarning(f"empreinte non reconnue il reste plus que {restant} avant alerte")
        scroll_text("empreinte non reconnue!!",1)
        scroll_text(f"tentative restante {restant}",2)
        if tentative >= 10 :
            with smtplib.SMTP(smtp_server, port) as server:
                server.starttls()  # Sécuriser la connexion
                server.login(login, password)
                server.sendmail(sender_email, receiver_email, message.as_string())
            debbugwarning('Mail envoyer car brute force')
        return None,None,None,None,None,None


def addByAdmin(f):
    result = verify_fingerprint(f)
    if result:
        match, score, user_id, grade, nom, prenom = result
        if grade == 2 :
            debbuginfo("Ajoute de doigt en cour")
            id=enroll_fingerprint(f)
            return id
        else :
            debbugwarning("veuiller ressayer avec une personne administrateur")
            return None

def delByAdmin(f):
    result = verify_fingerprint(f)
    if result:
        match, score, user_id, grade, nom, prenom = result
        if grade == 2 :
            listuser = []
            n = 0
            users = listeruser()
            for i in range(len(users)):
                listuser.append(users[i][0])
            if listuser:
                clear()
                while not button1.is_pressed:
                    display_message(f"{listuser[n]}",1)
                    if button2.is_pressed:
                        if n <= len(listuser):
                            n += 1
                            clear()
                            time.sleep(1)
                        else:
                            debbuginfo("Fin de la liste des utilisateurs.")
                            break  
                debbugwarning(f"id de l'utilisateur suprimer {users[i]}")
                
                if supprimeruser(f"{users[i][1]}"):
                    return 
                else:
                    debbugerror("error de supression")                      
                return None
        else :
            debbugwarning("probleme de droit ")   
