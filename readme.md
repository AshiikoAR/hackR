# API HackR - Alexandre RAGUIN

## Table des matières
- [Installation de l'API HackR](#installation-de-lapi-hackr)
- [I - Vérification d'existence d'adresse mail](#i---vérification-dexistence-dadresse-mail)

---

## Installation de l'API HackR

Prérequis
- **Python 3.x** et versions ultérieurs.
- Outils comme **pip** et **virtualenv** (gestion des environnements virtuels).

Étapes d’installation
1. Cloner le dépôt :
```bash
git clone <URL_DU_REPO>
cd <nom_du_dossier>
```

2. Installer les dépendances :
```bash
python3 -m venv env
source env/bin/activate  # Sur Windows: env\Scripts\activate
pip install -r requirements.txt
```
3. Lancer l’application :
```bash
python app.py
```

> L’API sera maintenant disponible à l’adresse https://localhost:5000.

**Technologies utilisées**
- **Flask** : Framework web léger pour Python.
- **Flask-JWT-Extended** : Gestion de l’authentification via JWT.
- **Requests** : Bibliothèque pour faire des requêtes HTTP (utilisée pour vérifier les emails via des API externes).
- **Hunter.io** : Service externe pour la vérification d’emails.

> **Tester l'API avec Postman**
>
> Vous pouvez tester toutes les routes avec Postman, un exemple ci-dessous :
> - Effectuer une requête POST sur /login pour obtenir un token JWT.
> - Utiliser le token dans les headers sous Authorization: Bearer <votre_token> pour accéder aux autres routes.

---

## I - Vérification d'existence d'adresse mail

### 1 - Authentification - Obtenir un Token JWT

Avant d’utiliser l’API, vous devez vous authentifier pour recevoir un token JWT, qui vous permettra d’accéder aux fonctionnalités sécurisées.
- Route : POST /login
- Description : Authentification avec un nom d’utilisateur et un mot de passe pour obtenir un token JWT.
- Exemple de requête :
- URL : http://localhost:5000/login
- Méthode : POST
- Body (JSON) :
```json
{
  "username": "admin",
  "password": "password"
}
```
- Réponse (JSON) :
```json
{
  "access_token": "<votre_token_jwt>"
}
```
> **Conseil d'utilisation** - Conservez ce token pour l’utiliser dans les headers de toutes vos futures requêtes.

### 2. Vérification de l’Existence d’une Adresse mail

Cette fonctionnalité vérifie si une adresse email existe réellement en se basant sur des services externes comme Hunter.io. Elle renvoie également un score de fiabilité de l’adresse.
-  Route : POST /check-email
- Description : Vérification de l’existence d’une adresse email.
- Exemple de requête :
- URL : http://localhost:5000/check-email
- Méthode : POST
- Headers : /
- Authorization: Bearer <votre_token_jwt>
- Body (JSON) :
```json
{
  "email": "test@example.com"
}
```
- Réponse (JSON) :
```json
{
  "email": "test@example.com",
  "existence": "deliverable",
  "score": 92
}
```
- email : Adresse mail vérifiée.
- existence : Statut de l'adresse mail (ex. : “deliverable”, “undeliverable”, “risky”).
- score : Score de fiabilité de l'adresse mail (0 à 100).

### 3. JWT et Accès Sécurisé

Toutes les routes de l’API (sauf /login) sont protégées par JWT. Vous devez inclure votre token JWT dans les headers de chaque requête sous la forme suivante :
- Headers :
```bash
Authorization: Bearer <votre_token_jwt>
```

### 4. Erreur et Gestion des Réponses

> Si l’adresse email est manquante dans le corps de la requête :
- Réponse (JSON) :
```json
{
  "msg": "Adresse email manquante"
}
```

> Si une erreur se produit lors de la vérification avec le service externe :
- Réponse (JSON) :
```json
{
  "msg": "Erreur lors de la vérification"
}
```