import time
import mysql.connector
from pyfingerprint.pyfingerprint import PyFingerprint

# Configuration du capteur
PORT = "/dev/ttyAMA0"  # Adapter selon l'OS (Windows: COM3)
BAUD_RATE = 57600

# Configuration MySQL
MYSQL_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "Zx223-Zx81",  # Modifie par ton mot de passe MySQL
    "database": "projetbts"  # Modifie par le nom de ta base de données
}

# Connexion à la base MySQL
def connect_db():
    return mysql.connector.connect(**MYSQL_CONFIG)

# Enregistrer une empreinte dans la base MySQL
def enregistrer_empreinte(fingerprint_id, fingerprint_data, nom, prenom):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        query = "INSERT INTO fingerprints (fingerprint_id, fingerprint_data, nom, prenom) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (fingerprint_id, fingerprint_data, nom, prenom))
        conn.commit()
        conn.close()
        print(f"✅ Empreinte {fingerprint_id} enregistrée en base de données !")
    except mysql.connector.Error as e:
        print(f"🚨 Erreur MySQL: {e}")

# Comparer une empreinte avec celles de la base MySQL
def comparer_empreinte(f, new_characteristics):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, fingerprint_data, grade, nom, prenom FROM fingerprints")
    empreintes = cursor.fetchall()
    conn.close()

    for user_id, empreinte_enregistree, grade, nom, prenom in empreintes:
        # Charger l'empreinte depuis la base dans le buffer 2
        f.uploadCharacteristics(0x02, list(empreinte_enregistree))

        # Comparer avec l'empreinte actuelle (buffer 1)
        match_score = f.compareCharacteristics()
        if match_score > 50:  # Seuil ajustable
            return True, match_score, user_id, grade, nom, prenom

    return False, 0, None, None, None, None

# Initialisation du capteur
def init_sensor():
    try:
        f = PyFingerprint(PORT, BAUD_RATE, 0xFFFFFFFF, 0x00000000)
        
        if not f.verifyPassword():
            raise ValueError("Mot de passe du capteur incorrect !")
        
        return f
    except Exception as e:
        print(f"🚨 Erreur lors de l'initialisation du capteur: {e}")
        exit(1)

# Enregistrer une empreinte
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

# Vérifier une empreinte
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



# Main
if __name__ == '__main__':
    sensor = init_sensor()
    
    # Demander à l'utilisateur ce qu'il veut faire
    choix = input("Choix 1 pour enregistrer, 2 pour vérifier : ")
    
    if choix == '1':
        addByAdmin(sensor)
    elif choix == '2':
        verify_fingerprint(sensor)  
    else:
        print("Option invalide.")

