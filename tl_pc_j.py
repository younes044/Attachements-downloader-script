# important: Lire 'lisez_moi_dabord.txt' avant d'executer ce script
# Lien de vidéo de mon test de script: https://youtu.be/Ma0cPBWyFHo

import os, email, imaplib

print(' ')

user = input('Tappez votre @ email:    ')
password = input('Tappez votre mot de passe:    ')

# Mettez le imap host de votre email provider
host = 'imap.mail.ru'

#Chemin de dossier de téléchargements
dir = '/home/kali/Téléchargements'

print("""
Attendez svp...
""")

# extrait le cors de l'email
def get_body(msg):
    if msg.is_multipart():
        return get_body(msg.get_payload(0))
    else:
        return msg.get_payload(None,True)
    
# Pour télécharger les pièces jointes
def telecharger(msg):
    for part in msg.walk():
        if part.get_content_maintype()=='multipart':
            continue
        if part.get('Content-Disposition') is None:
            continue
        fileName = part.get_filename()

        if bool(fileName):
            filePath = os.path.join(dir, fileName)
            with open(filePath,'wb') as f:
                f.write(part.get_payload(decode=True))
                


def get_emails(result_bytes):
    msgs = []
    for n in result_bytes[0].split():
        typ, data = con.fetch(n, '(RFC822)')
        msgs.append(data)
    return msgs

con = imaplib.IMAP4_SSL(host)
con.login(user, password)
con.select('inbox')

_, data = con.fetch('*','(RFC822)')
dt = email.message_from_bytes(data[0][1])
telecharger(dt)

print('Le téléchargement est terminé avec succès !')
