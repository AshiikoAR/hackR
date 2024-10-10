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

# Route pour vérifier l"existence d"un email
@app.route("/check-email", methods=["POST"])
@jwt_required()  # Nécessite un token JWT valide
def check_email():
    email = request.json.get("email", None)
    apikey = "cb800f605f6c28261560328efd4c8d6366eeeaa6" # Clé API Hunter.io

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

if __name__ == "__main__":
    app.run(debug=True)