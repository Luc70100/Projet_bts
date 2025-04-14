import smtplib
from email.mime.text import MIMEText

# Configuration
port = 587
smtp_server = "smtp.gmail.com"
login = "alerte@jet1oeil.com"  # Votre identifiant généré par Mailtrap
password = "dxiv gysb jbcr jhkn"  # Votre mot de passe généré par Mailtrap

sender_email = "alerte@jet1oeil.com"
receiver_email = "luc.bourguignon@jet1oeil.com"

# Contenu en texte brut
text = """\
Bonjour 
Il y a eu plus de 10 tentative d'ouverture non autoriser sur l'armoir de composant
"""

# Créer un objet MIMEText
message = MIMEText(text, "plain")
message["Subject"] = "Email en texte brut"
message["From"] = sender_email
message["To"] = receiver_email