# database.py

import mysql.connector
from config import MYSQL_CONFIG
import secrets
import string
import bcrypt
from log import debbuginfo,debbugerror

def connect_db():
    return mysql.connector.connect(**MYSQL_CONFIG)

# Enregistrer une empreinte dans la base MySQL
def enregistrer_empreinte(fingerprint_data, nom, prenom):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        query = "INSERT INTO fingerprints (fingerprint_data, nom, prenom) VALUES (%s, %s, %s)"
        cursor.execute(query, (fingerprint_data, nom, prenom))
        conn.commit()
        # Récupérer l'ID de l'empreinte insérée
        id = cursor.lastrowid
        conn.close()
        debbuginfo(f"✅ Empreinte enregistrée en base de données !")
        return id
    except mysql.connector.Error as e:
        debbugerror(f"🚨 Erreur MySQL: {e}")
        return None

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

def creationuser(id):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        password=''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(8))
        passwordhashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        # Insérer l'utilisateur dans la table utilisateurs avec l'ID de l'empreinte
        query = "INSERT INTO utilisateurs (fingerprint_id, username, password) VALUES (%s, %s, %s)"
        cursor.execute(query, (id, id, passwordhashed))
        conn.commit()
        debbuginfo(f"✅ Empreinte et utilisateur enregistrés en base de données !")
        return id,password
    except mysql.connector.Error as e:
            debbugerror(f"🚨 Erreur MySQL: {e}")
            return None,None
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

def supprimeruser(id):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        #on commence par lui suprimer son accede au site web
        query1 = "DELETE FROM utilisateurs WHERE fingerprint_id = %s"
        cursor.execute(query1, (id,))
        #ensuite on lui delete son accede au capteur d'empreinte 
        query = "DELETE FROM `fingerprints` WHERE id = %s"
        cursor.execute(query, (id,))
        conn.commit()
        debbuginfo(f"✅ Empreinte et utilisateur on ete supprimer de la base de données !")
        return True
    except mysql.connector.Error as e:
            debbugerror(f"🚨 Erreur MySQL: {e}")
            return None,None
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

def listeruser():
    try:
        conn = connect_db()
        cursor = conn.cursor()
        query = "SELECT prenom, id FROM `fingerprints`"
        cursor.execute(query)
        users = cursor.fetchall()
        conn.commit()
        return users
    except mysql.connector.Error as e:
            debbugerror(f"🚨 Erreur MySQL: {e}")
            return None,None
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()