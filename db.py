# database.py

import mysql.connector
from config import MYSQL_CONFIG

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
