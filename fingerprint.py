# fingerprint.py

import time
from pyfingerprint.pyfingerprint import PyFingerprint
from db import enregistrer_empreinte, comparer_empreinte

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
    while not f.readImage():
        pass

    print("✅ Empreinte capturée !")
    f.convertImage(0x01)
    characteristics = f.downloadCharacteristics(0x01)
    fingerprint_data = bytearray(characteristics)

    fingerprint_id = input("Entrez un ID unique pour l'empreinte : ")
    nom = input("Veuillez entrer le nom : ")
    prenom = input("Veuillez entrer le prénom : ")

    enregistrer_empreinte(fingerprint_id, fingerprint_data, nom, prenom)
    print("✅ Empreinte enregistrée.")

def verify_fingerprint(f):
    print("\n🔄 Retire ton doigt puis repose-le pour la vérification...")
    time.sleep(2)

    print("\n👉 Place ton doigt pour vérification...")
    while not f.readImage():
        pass

    print("✅ Nouvelle empreinte capturée !")
    f.convertImage(0x01)
    new_characteristics = f.downloadCharacteristics(0x01)

    # Comparaison avec la base de données
    match, score, user_id, grade, nom, prenom = comparer_empreinte(f, bytearray(new_characteristics))

    if match:
        print(f"✅✅ MATCH ! L'empreinte correspond à l'ID {user_id} nommer {nom} {prenom} qui a le grade {grade} (Score : {score})")
        return match, score, user_id, grade, nom, prenom
    else:
        print(f"❌ PAS DE MATCH ! (Score : {score})")
        return None,None,None,None,None,None


def addByAdmin(f):
    result = verify_fingerprint(f)
    if result:
        match, score, user_id, grade, nom, prenom = result
        if grade == 2 :
            print("presenter le doigt")
            time.sleep(10)
            enroll_fingerprint(f)
        else :
            print("veuiller ressayer avec une personne administrateur")
