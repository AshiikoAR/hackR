from flask import Flask, request, jsonify
from flask_jwt_extended import (JWTManager, create_access_token, jwt_required)
import requests

app = Flask(__name__)

# Configuration du secret pour JWT
app.config["JWT_SECRET_KEY"] = "lorem_ipsum_dolor_sit_amet"
jwt = JWTManager(app)

# Exemple d'utilisateur
USERS = {
    "admin": "password"
}

# Route d'authentification pour obtenir un token JWT
@app.route("/login", methods=["POST"])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    
    if USERS.get(username) == password:
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token)
    else:
        return jsonify({"msg": "Identifiants incorrects"}), 401

# Route pour vérifier l'existence d'un email
@app.route("/check-email", methods=["POST"])
@jwt_required()  # Nécessite un token JWT valide
def check_email():
    email = request.json.get("email", None)
    apikey = "cb800f605f6c28261560328efd4c8d6366eeeaa6"  # Clé API Hunter.io

    if not email:
        return jsonify({"msg": "Adresse email manquante"}), 400

    # Utilisation de l'API Hunter.io 
    response = requests.get(f"https://api.hunter.io/v2/email-verifier?email={email}&api_key={apikey}")
    
    if response.status_code == 200:
        data = response.json()
        return jsonify({
            "email": email,
            "existence": data.get("data").get("result"),
            "score": data.get("data").get("score")
        })
    else:
        return jsonify({"msg": "Erreur lors de la vérification"}), 500

# Route pour spammer un email
@app.route("/send-spam", methods=["POST"])
@jwt_required()  # Nécessite un token JWT valide
def send_spam():
    email = request.json.get("email", None)
    subject = request.json.get("subject", "Spam Subject")
    content = request.json.get("content", "This is a spam email.")
    num_emails = request.json.get("num_emails", 1)

    if not email or not content or not subject:
        return jsonify({"msg": "Email, subject, et contenu sont requis"}), 400

    # Configuration API MailJet
    mailjet_api_key = "3938d9cf27060e30280cc13183e64d98"
    mailjet_secret_key = "7f7917bfa6ed133d9585811e9a6d9801"
    mail_envoi = "alexandre.raguin49@gmail.com"

    # Headers et payload pour l'API MailJet
    headers = {
        'Content-Type': 'application/json'
    }

    payload = {
        'Messages': [{
            "From": {
                "Email": mail_envoi,  # Variable utilisée correctement
                "Name": "TEST Test"
            },
            "To": [{
                "Email": email,
                "Name": "Cible"
            }],
            "Subject": subject,
            "TextPart": content,
        }]
    }

    # Envoi des emails en boucle (selon le nombre demandé)
    for i in range(num_emails):
        response = requests.post(
            "https://api.mailjet.com/v3.1/send",
            auth=(mailjet_api_key, mailjet_secret_key),
            json=payload,
            headers=headers
        )

        if response.status_code != 200:
            return jsonify({"msg": f"Erreur lors de l'envoi de l'email {i+1}"}), response.status_code

    return jsonify({"msg": f"{num_emails} emails envoyés avec succès à {email}."})

# Route pour vérifier si un mot de passe est courant
@app.route("/check-password", methods=["POST"])
@jwt_required()  # Nécessite un token JWT valide
def check_password():
    password = request.json.get("password", None)

    if not password:
        return jsonify({"msg": "Mot de passe manquant"}), 400

    # Charger la liste des mots de passe courants depuis le fichier texte
    common_passwords_file = "10k-most-common.txt"
    
    try:
        with open(common_passwords_file, "r") as file:
            common_passwords = file.read().splitlines()
    except FileNotFoundError:
        return jsonify({"msg": "Fichier des mots de passe courants introuvable"}), 500

    # Vérifier si le mot de passe est dans la liste
    if password in common_passwords:
        return jsonify({"msg": "Le mot de passe est dans la liste des mots de passe les plus courants."}), 200
    else:
        return jsonify({"msg": "Le mot de passe est sécurisé (non trouvé dans la liste des mots de passe courants)."}), 200

if __name__ == "__main__":
    app.run(debug=True)