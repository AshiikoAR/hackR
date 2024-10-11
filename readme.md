# API HackR - Alexandre RAGUIN

## Table des matières
- [Installation de l'API HackR](#installation-de-lapi-hackr)
- [I - Authentification](#i---authentification)
    - [1. Obtenir un Token JWT](#1-obtenir-un-token-jwt)
    - [2. Accès Sécurisé](#2-accès-sécurisé)
- [II - Vérification d'existence d'adresse mail](#ii---vérification-dexistence-dadresse-mail)
    - [1. Code de vérification de l'adresse mail](#1-code-de-vérification-de-l-adresse-mail)
    - [2. Erreurs et Gestion des Réponses](#2-erreurs-et-gestion-des-réponses)
- [III - Liste des mots de passe courants](#iii---liste-des-mots-de-passe-courants)

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

## I - Authentification 

### 1. Obtenir un Token JWT

Avant d’utiliser l’API, vous devez vous authentifier pour recevoir un token JWT, qui vous permettra d’accéder aux fonctionnalités sécurisées.
- Route : POST /login
- Description : Authentification avec un nom d’utilisateur et un mot de passe pour obtenir un token JWT.
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

### 2. Accès Sécurisé

Toutes les routes de l’API (sauf /login) sont protégées par JWT. Vous devez inclure votre token JWT dans les headers de chaque requête sous la forme suivante :
- Headers :
```bash
Authorization: Bearer <votre_token_jwt>
```

---

## II - Vérification d'existence d'adresse mail

### 1. Code de vérification de l'adresse mail
Cette fonctionnalité vérifie si une adresse email existe réellement en se basant sur des services externes comme Hunter.io. Elle renvoie également un score de fiabilité de l’adresse.
-  Route : POST /check-email
- Description : Vérification de l’existence d’une adresse email.
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
> email : Adresse mail vérifiée.
> existence : Statut de l'adresse mail (ex. : “deliverable”, “undeliverable”, “risky”).
> score : Score de fiabilité de l'adresse mail (0 à 100).

### 2. Erreurs et Gestion des Réponses

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

## III - Liste des mots de passe courants

### Code de recherche de mot de passe
Cette fonctionnalité permet de vérifier si le mot de passe fait partie de la liste des 10k passwords les plus communs (à partir du fichier "**10k-most-common.txt**").
-  Route : POST /check-password
- Description : Vérification de l’existence d’une adresse email.
- URL : http://localhost:5000/check-password
- Méthode : POST
- Headers : /
- Authorization: Bearer <votre_token_jwt>
- Body (JSON) :
```json
{
  "password": "123456"
}
```
- Réponse (JSON) :
```json
{
  "msg": "Le mot de passe est dans la liste des mots de passe les plus courants."
}
```
**OU**
```json
{
  "msg": "Le mot de passe est sécurisé (non trouvé dans la liste des mots de passe courants)."
}
```
> msg : Renvoie si le mot de passe à été trouvé (ou non = sécurisé) dans la liste des mots de passe courants.

### 2. Erreurs et Gestion des Réponses

> Si le fichier ".txt" contenant les mots de passe est absent du dossier du projet :
- Réponse (JSON) :
```json
{
  "msg": "Fichier des mots de passe courants introuvable"
}
```

> Si ul'utilisateur a oublié de renseigner un mdp :
- Réponse (JSON) :
```json
{
  "msg": "Mot de passe manquant"
}
```