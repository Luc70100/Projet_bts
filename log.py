import mysql.connector
from config import MYSQL_CONFIG

def connect_db():
    return mysql.connector.connect(**MYSQL_CONFIG)

def logopen(id):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        print(f"{id}")
        # Requête pour récupérer les informations de l'utilisateur
        query = "SELECT id, fingerprint_data, grade, nom, prenom FROM fingerprints WHERE id = %s"
        cursor.execute(query, (id,))
        res = cursor.fetchone()

        if res is None:
            print(f"Pas de résultat pour l'ID {id}")
            return

        print(f"Résultat de la requête SELECT : {res}")
        if res is None:
            print("pas de resulta pour cette id")
            return
        nom=res[3]
        print(f"{nom},")
        prenom=res[4]
        print(f"{prenom},")
        print(f"{id},")
        query = "INSERT INTO ouvertures (id_empreinte,nom, prenom, open_at) VALUES (%s, %s, %s, NOW())"
        cursor.execute(query, (id,nom,prenom))
        conn.commit()
        conn.close()
        print("enregistrement de l'ouverture effectuer")
    except mysql.connector.Error as e:
        print(f"🚨 Erreur MySQL: {e}")
        
    