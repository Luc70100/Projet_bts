import mysql.connector
from config import MYSQL_CONFIG
from loguru import logger

def connect_db():
    return mysql.connector.connect(**MYSQL_CONFIG)

def logopen(id):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        debbuginfo(f"id qui essaye d'ouvrire la port : {id}")
        # Requête pour récupérer les informations de l'utilisateur
        query = "SELECT id, fingerprint_data, grade, nom, prenom FROM fingerprints WHERE id = %s"
        cursor.execute(query, (id,))
        res = cursor.fetchone()

        if res is None:
            debbugerror("pas de resulta pour cette id")
            return
        nom=res[3]
        prenom=res[4]
        query = "INSERT INTO ouvertures (id_empreinte,nom, prenom, open_at) VALUES (%s, %s, %s, NOW())"
        cursor.execute(query, (id,nom,prenom))
        conn.commit()
        conn.close()
        debbuginfo("enregistrement de l'ouverture effectuer")
    except mysql.connector.Error as e:
        debbugerror(f"🚨 Erreur MySQL: {e}")
        
def debbuginfo(n):
    logger.info(n)
def debbugwarning(n):
    logger.warning(n)
def debbugerror(n):
    logger.error(n) 
def debbugsuccess(n):
    logger.success(n) 

def logfile():
    logger.add("log/file_{time}.log", level="TRACE", rotation="100 MB")                                    