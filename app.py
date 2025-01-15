from flask import Flask, request, jsonify, send_from_directory
from flask_jwt_extended import (JWTManager, create_access_token, jwt_required, get_jwt_identity)
from flask_swagger_ui import get_swaggerui_blueprint
from flask_cors import CORS
import requests
import json
import os
from functools import wraps
from faker import Faker
import random

app = Flask(__name__)
CORS(app)

# Configuration du secret pour JWT
app.config["JWT_SECRET_KEY"] = "lorem_ipsum_dolor_sit_amet"
jwt = JWTManager(app)

# Configuration pour la documentation Swagger
SWAGGER_URL = '/docs'
API_URL = '/swagger.json'
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "HackR API Documentation"
    }
)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

# Servir le fichier swagger.json
@app.route("/swagger.json")
def serve_swagger_json():
    return send_from_directory(os.getcwd(), "swagger.json")

# Logs des actions utilisateurs (stockés en mémoire ou dans un fichier)
LOG_FILE = 'logs.json'

# Types d'utilisateurs avec rôles (admin ou user)
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

# Vérification du rôle de l'utilisateur
def admin_required(f):
    @wraps(f)  # Utilisation de functools.wraps pour éviter les conflits
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
    if not isinstance(email, str):
        return jsonify({"msg": "Email must be a string"}), 422

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

    # Chargement de la liste des mots de passe courants depuis un fichier texte
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

# Route pour récupérer les domaines et sous-domaines d'un domaine donné
@app.route("/get-domains", methods=["POST"])
@jwt_required()
def get_domains():
    domain = request.json.get("domain", None)
    username = get_jwt_identity()["username"]

    if not domain:
        return jsonify({"msg": "Nom de domaine manquant"}), 400

    # Utilisation de l'API SecurityTrails (ou autre service de renseignement de domaines)
    api_key = "HywSt8KrfSkeufDTYXg80MWOeulw4mYU"  # Remplacez par votre clé API SecurityTrails
    headers = {
        "APIKEY": api_key
    }
    response = requests.get(f"https://api.securitytrails.com/v1/domain/{domain}/subdomains", headers=headers)

    if response.status_code == 200:
        data = response.json()
        subdomains = data.get("subdomains", [])
        domains_with_subdomains = [f"{sub}.{domain}" for sub in subdomains]
        log_action(username, "get-domains", f"Domain: {domain}")
        return jsonify({"domain": domain, "subdomains": domains_with_subdomains})
    else:
        return jsonify({"msg": "Erreur lors de la récupération des sous-domaines"}), response.status_code

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

# Route pour obtenir les logs des dernières actions d'un utilisateur spécifique
@app.route("/logs/user/<username>", methods=["GET"])
@jwt_required()
@admin_required
def view_user_logs(username):
    try:
        with open(LOG_FILE, 'r') as file:
            logs = json.load(file)
        user_logs = [log for log in logs if log["user"] == username]
        return jsonify(user_logs)
    except FileNotFoundError:
        return jsonify({"msg": "Aucun log trouvé"}), 404

# Route pour obtenir les logs des dernières actions d'une fonctionnalité spécifique
@app.route("/logs/action/<action>", methods=["GET"])
@jwt_required()
@admin_required
def view_action_logs(action):
    try:
        with open(LOG_FILE, 'r') as file:
            logs = json.load(file)
        action_logs = [log for log in logs if log["action"] == action]
        return jsonify(action_logs)
    except FileNotFoundError:
        return jsonify({"msg": "Aucun log trouvé"}), 404

fake = Faker()

# Route pour générer une page de phishing (exemple simple)
@app.route("/create-phishing-page", methods=["POST"])
@jwt_required()
@admin_required
def create_phishing_page():
    target = request.json.get("target", None)
    username = get_jwt_identity()["username"]

    if not target:
        return jsonify({"msg": "Cible manquante"}), 400

    phishing_page = f"<html><body><h1>Bienvenue {target}</h1><p>Veuillez entrer vos informations de connexion.</p></body></html>"
    log_action(username, "create-phishing-page", f"target: {target}")
    return jsonify({"phishing_page": phishing_page})

# Route pour lancer une attaque DDoS (exemple simple)
@app.route("/ddos", methods=["POST"])
@jwt_required()
@admin_required
def ddos():
    target_url = request.json.get("target_url", None)
    num_requests = request.json.get("num_requests", 100)
    username = get_jwt_identity()["username"]

    if not target_url:
        return jsonify({"msg": "URL cible manquante"}), 400

    for _ in range(num_requests):
        try:
            requests.get(target_url)
        except requests.RequestException:
            pass

    log_action(username, "ddos", f"target_url: {target_url}, num_requests: {num_requests}")
    return jsonify({"msg": f"{num_requests} requêtes envoyées à {target_url}."})

# Route pour changer une image de manière aléatoire
@app.route("/random-image", methods=["GET"])
@jwt_required()
def random_image():
    username = get_jwt_identity()["username"]
    response = requests.get("https://picsum.photos/200")
    log_action(username, "random-image")
    return send_from_directory(os.getcwd(), response.url.split("/")[-1])

# Route pour générer une identité fictive
@app.route("/generate-identity", methods=["GET"])
@jwt_required()
def generate_identity():
    username = get_jwt_identity()["username"]
    identity = {
        "name": fake.name(),
        "address": fake.address(),
        "email": fake.email(),
        "job": fake.job()
    }
    log_action(username, "generate-identity")
    return jsonify(identity)

# Route pour crawler des informations sur une personne
@app.route("/crawl-info", methods=["POST"])
@jwt_required()
def crawl_info():
    first_name = request.json.get("first_name", None)
    last_name = request.json.get("last_name", None)
    username = get_jwt_identity()["username"]

    if not first_name or not last_name:
        return jsonify({"msg": "Prénom et nom manquants"}), 400

    # Exemple simple de recherche d'informations (à remplacer par une vraie API)
    info = {
        "first_name": first_name,
        "last_name": last_name,
        "info": f"Informations fictives pour {first_name} {last_name}"
    }
    log_action(username, "crawl-info", f"first_name: {first_name}, last_name: {last_name}")
    return jsonify(info)

# Route pour générer un mot de passe sécurisé
@app.route("/generate-password", methods=["GET"])
@jwt_required()
def generate_password():
    username = get_jwt_identity()["username"]
    password = fake.password(length=12, special_chars=True, digits=True, upper_case=True, lower_case=True)
    log_action(username, "generate-password")
    return jsonify({"password": password})

# Swagger documentation
swagger_template = {
    "swagger": "2.0",
    "info": {
        "title": "HackR API",
        "description": "API pour diverses opérations de sécurité",
        "version": "1.0.0"
    },
    "host": "localhost:5000",
    "basePath": "/",
    "schemes": ["http"],
    "paths": {
        "/login": {
            "post": {
                "summary": "Authentification utilisateur",
                "description": "Obtenir un token JWT",
                "parameters": [
                    {
                        "name": "body",
                        "in": "body",
                        "required": True,
                        "schema": {
                            "type": "object",
                            "properties": {
                                "username": {"type": "string"},
                                "password": {"type": "string"}
                            }
                        }
                    }
                ],
                "responses": {
                    "200": {"description": "Token JWT généré"},
                    "401": {"description": "Identifiants incorrects"}
                }
            }
        },
        # ...ajouter les autres routes ici...
    }
}

@app.route("/swagger-docs.json")
def swagger_json():
    return jsonify(swagger_template)

if __name__ == "__main__":
    app.run(debug=True)