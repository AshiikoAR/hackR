from flask import Flask, request, jsonify, send_from_directory
from flask_jwt_extended import (JWTManager, create_access_token, jwt_required, get_jwt_identity)
from flask_swagger_ui import get_swaggerui_blueprint
import requests
import json
import os
from functools import wraps

app = Flask(__name__)

# Configuration du secret pour JWT
app.config["JWT_SECRET_KEY"] = "lorem_ipsum_dolor_sit_amet"
jwt = JWTManager(app)

# Route pour la documentation Swagger
SWAGGER_URL = '/docs'  # URL pour accéder à la documentation
API_URL = '/swagger.json'  # Lien vers le fichier swagger.json

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={  # Configuration Swagger UI
        'app_name': "HackR API Documentation"
    }
)

app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

# Servir le fichier swagger.json
@app.route("/swagger.json")
def swagger_json():
    return send_from_directory(os.getcwd(), "swagger.json")

# Logs des actions utilisateurs (stockés en mémoire ou dans un fichier)
LOG_FILE = 'logs.json'

# Exemple d'utilisateur avec rôles (admin ou user)
USERS = {
    "admin": {"password": "password", "role": "admin"},
    "user": {"password": "password", "role": "user"}
}

# Fonction pour ajouter des logs
def log_action(user, action, details=""):
    log_entry = {"user": user, "action": action, "details": details}
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'w') as file:
            json.dump([log_entry], file)
    else:
        with open(LOG_FILE, 'r+') as file:
            logs = json.load(file)
            logs.append(log_entry)
            file.seek(0)
            json.dump(logs, file, indent=4)

# Route d'authentification pour obtenir un token JWT
@app.route("/login", methods=["POST"])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    
    user = USERS.get(username)
    if user and user["password"] == password:
        access_token = create_access_token(identity={"username": username, "role": user["role"]})
        log_action(username, "login")
        return jsonify(access_token=access_token)
    else:
        return jsonify({"msg": "Identifiants incorrects"}), 401

# Vérification du rôle de l'utilisateur
def admin_required(f):
    def wrapper(*args, **kwargs):
        identity = get_jwt_identity()
        if identity["role"] != "admin":
            return jsonify({"msg": "Accès refusé, droits insuffisants"}), 403
        return f(*args, **kwargs)
    return wrapper

# Route pour vérifier l'existence d'un email
@app.route("/check-email", methods=["POST"])
@jwt_required()  # Nécessite un token JWT valide
def check_email():
    email = request.json.get("email", None)
    apikey = "cb800f605f6c28261560328efd4c8d6366eeeaa6"  # Clé API Hunter.io
    username = get_jwt_identity()["username"]

    if not email:
        return jsonify({"msg": "Adresse email manquante"}), 400

    # Utilisation de l'API Hunter.io 
    response = requests.get(f"https://api.hunter.io/v2/email-verifier?email={email}&api_key={apikey}")
    
    if response.status_code == 200:
        data = response.json()
        log_action(username, "check-email", f"email: {email}")
        return jsonify({
            "email": email,
            "existence": data.get("data").get("result"),
            "score": data.get("data").get("score")
        })
    else:
        return jsonify({"msg": "Erreur lors de la vérification"}), 500

# Route pour spammer un email (admin uniquement)
@app.route("/send-spam", methods=["POST"])
@jwt_required()  # Nécessite un token JWT valide
@admin_required  # Réservé aux administrateurs
def send_spam():
    email = request.json.get("email", None)
    subject = request.json.get("subject", "Spam Subject")
    content = request.json.get("content", "This is a spam email.")
    num_emails = request.json.get("num_emails", 1)
    username = get_jwt_identity()["username"]

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
                "Email": mail_envoi,
                "Name": "SpamBot"
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

    log_action(username, "send-spam", f"{num_emails} emails envoyés à {email}")
    return jsonify({"msg": f"{num_emails} emails envoyés avec succès à {email}."})

# Route pour vérifier si un mot de passe est courant
@app.route("/check-password", methods=["POST"])
@jwt_required()  # Nécessite un token JWT valide
def check_password():
    password = request.json.get("password", None)
    username = get_jwt_identity()["username"]

    if not password:
        return jsonify({"msg": "Mot de passe manquant"}), 400

    # Charger la liste des mots de passe courants depuis le fichier texte
    common_passwords_file = "10k-most-common.txt"
    
    try:
        with open(common_passwords_file, "r") as file:
            common_passwords = file.read().splitlines()
    except FileNotFoundError:
        return jsonify({"msg": "Fichier des mots de passe courants introuvable"}), 500

    if password in common_passwords:
        log_action(username, "check-password", "Mot de passe courant")
        return jsonify({"msg": "Le mot de passe est dans la liste des mots de passe les plus courants."}), 200
    else:
        log_action(username, "check-password", "Mot de passe sécurisé")
        return jsonify({"msg": "Le mot de passe est sécurisé (non trouvé dans la liste des mots de passe courants)."}), 200

# Vérification du rôle de l'utilisateur
def admin_required(f):
    @wraps(f)  # Utilisation de functools.wraps pour éviter les conflits
    def wrapper(*args, **kwargs):
        identity = get_jwt_identity()
        if identity["role"] != "admin":
            return jsonify({"msg": "Accès refusé, droits insuffisants"}), 403
        return f(*args, **kwargs)
    return wrapper

# Route pour voir les logs (réservée aux admins)
@app.route("/logs", methods=["GET"])
@jwt_required()  # Nécessite un token JWT valide
@admin_required  # Réservé aux administrateurs
def view_logs():
    try:
        with open(LOG_FILE, 'r') as file:
            logs = json.load(file)
        return jsonify(logs)
    except FileNotFoundError:
        return jsonify({"msg": "Aucun log trouvé"}), 404

if __name__ == "__main__":
    app.run(debug=True)