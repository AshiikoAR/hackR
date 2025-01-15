# API HackR - Alexandre RAGUIN

## Table des matières
- [Installation de l'API HackR](#installation-de-lapi-hackr)
- [I - Authentification](#i---authentification)
    - [1. Obtenir un Token JWT](#1-obtenir-un-token-jwt)
    - [2. Accès Sécurisé](#2-accès-sécurisé)
- [II - Vérification d'existence d'adresse mail](#ii---vérification-dexistence-dadresse-mail)
    - [1. Code de vérification de l'adresse mail](#1-code-de-vérification-de-l-adresse-mail)
    - [2. Erreurs et Gestion des Réponses n°1](#2-erreurs-et-gestion-des-réponses-n1)
- [III - Liste des mots de passe courants](#iii---liste-des-mots-de-passe-courants)
    - [1. Code de recherche de mot de passe](#1-code-de-recherche-de-mot-de-passe)
    - [2. Erreurs et Gestion des Réponses n°2](#2-erreurs-et-gestion-des-réponses-n2)
- [IV - Spammer un email](#iv---spammer-un-email)
    - [1. Code pour spammer un email](#1-code-pour-spammer-un-email)
    - [2. Erreurs et Gestion des Réponses n°3](#2-erreurs-et-gestion-des-réponses-n3)
- [V - Récupérer les sous-domaines d'un domaine](#v---récupérer-les-sous-domaines-dun-domaine)
    - [1. Code pour récupérer les sous-domaines](#1-code-pour-récupérer-les-sous-domaines)
    - [2. Erreurs et Gestion des Réponses n°4](#2-erreurs-et-gestion-des-réponses-n4)
- [VI - Générer une page de phishing](#vi---générer-une-page-de-phishing)
    - [1. Code pour générer une page de phishing](#1-code-pour-générer-une-page-de-phishing)
    - [2. Erreurs et Gestion des Réponses n°5](#2-erreurs-et-gestion-des-réponses-n5)
- [VII - Générer une identité fictive](#vii---générer-une-identité-fictive)
    - [1. Code pour générer une identité fictive](#1-code-pour-générer-une-identité-fictive)
    - [2. Erreurs et Gestion des Réponses n°6](#2-erreurs-et-gestion-des-réponses-n6)
- [VIII - Lancer une attaque DDoS](#viii---lancer-une-attaque-ddos)
    - [1. Code pour lancer une attaque DDoS](#1-code-pour-lancer-une-attaque-ddos)
    - [2. Erreurs et Gestion des Réponses n°7](#2-erreurs-et-gestion-des-réponses-n7)
- [IX - Générer un mot de passe sécurisé](#ix---générer-un-mot-de-passe-sécurisé)
    - [1. Code pour générer un mot de passe sécurisé](#1-code-pour-générer-un-mot-de-passe-sécurisé)
    - [2. Erreurs et Gestion des Réponses n°8](#2-erreurs-et-gestion-des-réponses-n8)
- [X - Crawler des informations sur une personne](#x---crawler-des-informations-sur-une-personne)
    - [1. Code pour crawler des informations sur une personne](#1-code-pour-crawler-des-informations-sur-une-personne)
    - [2. Erreurs et Gestion des Réponses n°9](#2-erreurs-et-gestion-des-réponses-n9)
- [XI - Obtenir une image aléatoire](#xi---obtenir-une-image-aléatoire)
    - [1. Code pour obtenir une image aléatoire](#1-code-pour-obtenir-une-image-aléatoire)
    - [2. Erreurs et Gestion des Réponses n°10](#2-erreurs-et-gestion-des-réponses-n10)

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

> L’API sera maintenant disponible à l’adresse https://127.0.0.1:5000.

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
- URL : http://127.0.0.1:5000/login
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
- URL : http://127.0.0.1:5000/check-email
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
> **email** - Adresse mail vérifiée.
> **existence** - Statut de l'adresse mail (ex. : “deliverable”, “undeliverable”, “risky”).
> **score** - Score de fiabilité de l'adresse mail (0 à 100).

### 2. Erreurs et Gestion des Réponses n°1

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

### 1. Code de recherche de mot de passe
Cette fonctionnalité permet de vérifier si le mot de passe fait partie de la liste des 10k passwords les plus communs (à partir du fichier "**10k-most-common.txt**").
-  Route : POST /check-password
- Description : Vérification de l’existence d’une adresse email.
- URL : http://127.0.0.1:5000/check-password
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
> **msg** - Renvoie si le mot de passe à été trouvé (ou non = sécurisé) dans la liste des mots de passe courants.

### 2. Erreurs et Gestion des Réponses n°2

> Si le fichier ".txt" contenant les mots de passe est absent du dossier du projet :
- Réponse (JSON) :
```json
{
  "msg": "Fichier des mots de passe courants introuvable"
}
```

> Si l'utilisateur a oublié de renseigner un mdp :
- Réponse (JSON) :
```json
{
  "msg": "Mot de passe manquant"
}
```

## IV - Spammer un email

### 1. Code pour spammer un email
Cette fonctionnalité permet d'envoyer un grand nombre d'emails à une adresse spécifique.
-  Route : POST /send-spam
- Description : Envoi de spams à une adresse email.
- URL : http://127.0.0.1:5000/send-spam
- Méthode : POST
- Headers : /
- Authorization: Bearer <votre_token_jwt>
- Body (JSON) :
```json
{
  "email": "victim@example.com",
  "subject": "This is a spam message",
  "content": "Spam content",
  "num_emails": 100
}
```
- Réponse (JSON) :
```json
{
  "msg": "100 emails envoyés avec succès à victim@example.com."
}
```
> **email** - Adresse email de la victime.
> **subject** - Sujet du message de spam.
> **content** - Contenu du message de spam.
> **num_emails** - Nombre d'emails à envoyer.

### 2. Erreurs et Gestion des Réponses n°3

> Si l’adresse email est manquante dans le corps de la requête :
- Réponse (JSON) :
```json
{
  "msg": "Email, subject, et contenu sont requis"
}
```

> Si le message est manquant dans le corps de la requête :
- Réponse (JSON) :
```json
{
  "msg": "Email, subject, et contenu doivent être des chaînes de caractères"
}
```

> Si le nombre d'emails à envoyer est manquant dans le corps de la requête :
- Réponse (JSON) :
```json
{
  "msg": "Nombre d'emails manquant"
}
```

## V - Récupérer les sous-domaines d'un domaine

### 1. Code pour récupérer les sous-domaines
Cette fonctionnalité permet de récupérer les sous-domaines d'un domaine spécifique.
-  Route : POST /get-domains
- Description : Récupération des sous-domaines d'un domaine.
- URL : http://127.0.0.1:5000/get-domains
- Méthode : POST
- Headers : /
- Authorization: Bearer <votre_token_jwt>
- Body (JSON) :
```json
{
  "domain": "example.com"
}
```
- Réponse (JSON) :
```json
{
  "domain": "example.com",
  "subdomains": ["sub1.example.com", "sub2.example.com"]
}
```
> **domain** - Domaine pour lequel récupérer les sous-domaines.
> **subdomains** - Liste des sous-domaines récupérés.

### 2. Erreurs et Gestion des Réponses n°4

> Si le domaine est manquante dans le corps de la requête :
- Réponse (JSON) :
```json
{
  "msg": "Nom de domaine manquant"
}
```

> Si une erreur se produit lors de la récupération des sous-domaines :
- Réponse (JSON) :
```json
{
  "msg": "Erreur lors de la récupération des sous-domaines"
}
```

## VI - Générer une page de phishing

### 1. Code pour générer une page de phishing
Cette fonctionnalité permet de générer une page de phishing pour une cible spécifique.
-  Route : POST /create-phishing-page
- Description : Génération d'une page de phishing.
- URL : http://127.0.0.1:5000/create-phishing-page
- Méthode : POST
- Headers : /
- Authorization: Bearer <votre_token_jwt>
- Body (JSON) :
```json
{
  "target": "example_target"
}
```
- Réponse (JSON) :
```json
{
  "phishing_page": "<html><body><h1>Bienvenue example_target</h1><p>Veuillez entrer vos informations de connexion.</p></body></html>"
}
```
> **target** - Cible pour laquelle générer la page de phishing.

### 2. Erreurs et Gestion des Réponses n°5

> Si la cible est manquante dans le corps de la requête :
- Réponse (JSON) :
```json
{
  "msg": "Cible manquante"
}
```

## VII - Générer une identité fictive

### 1. Code pour générer une identité fictive
Cette fonctionnalité permet de générer une identité fictive.
-  Route : GET /generate-identity
- Description : Génération d'une identité fictive.
- URL : http://127.0.0.1:5000/generate-identity
- Méthode : GET
- Headers : /
- Authorization: Bearer <votre_token_jwt>
- Réponse (JSON) :
```json
{
  "name": "John Doe",
  "address": "123 Main St, Springfield, USA",
  "email": "john.doe@example.com",
  "job": "Software Engineer"
}
```
> **name** - Nom fictif généré.
> **address** - Adresse fictive générée.
> **email** - Email fictif généré.
> **job** - Profession fictive générée.

### 2. Erreurs et Gestion des Réponses n°6

> Si une erreur se produit lors de la génération de l'identité :
- Réponse (JSON) :
```json
{
  "msg": "Erreur lors de la génération de l'identité"
}
```

## VIII - Lancer une attaque DDoS

### 1. Code pour lancer une attaque DDoS
Cette fonctionnalité permet de lancer une attaque DDoS sur une URL cible.
-  Route : POST /ddos
- Description : Lancer une attaque DDoS.
- URL : http://127.0.0.1:5000/ddos
- Méthode : POST
- Headers : /
- Authorization: Bearer <votre_token_jwt>
- Body (JSON) :
```json
{
  "target_url": "http://example.com",
  "num_requests": 100
}
```
- Réponse (JSON) :
```json
{
  "msg": "100 requêtes envoyées à http://example.com."
}
```
> **target_url** - URL cible de l'attaque DDoS.
> **num_requests** - Nombre de requêtes à envoyer.

### 2. Erreurs et Gestion des Réponses n°7

> Si l'URL cible est manquante dans le corps de la requête :
- Réponse (JSON) :
```json
{
  "msg": "URL cible manquante"
}
```

> Si le nombre de requêtes est manquant ou invalide dans le corps de la requête :
- Réponse (JSON) :
```json
{
  "msg": "Number of requests must be an integer"
}
```

## IX - Générer un mot de passe sécurisé

### 1. Code pour générer un mot de passe sécurisé
Cette fonctionnalité permet de générer un mot de passe sécurisé.
-  Route : GET /generate-password
- Description : Génération d'un mot de passe sécurisé.
- URL : http://127.0.0.1:5000/generate-password
- Méthode : GET
- Headers : /
- Authorization: Bearer <votre_token_jwt>
- Réponse (JSON) :
```json
{
  "password": "A1b2C3d4E5!"
}
```
> **password** - Mot de passe sécurisé généré.

### 2. Erreurs et Gestion des Réponses n°8

> Si une erreur se produit lors de la génération du mot de passe :
- Réponse (JSON) :
```json
{
  "msg": "Erreur lors de la génération du mot de passe"
}
```

## X - Crawler des informations sur une personne

### 1. Code pour crawler des informations sur une personne
Cette fonctionnalité permet de crawler des informations sur une personne en utilisant son prénom et son nom.
-  Route : POST /crawl-info
- Description : Crawler des informations sur une personne.
- URL : http://127.0.0.1:5000/crawl-info
- Méthode : POST
- Headers : /
- Authorization: Bearer <votre_token_jwt>
- Body (JSON) :
```json
{
  "first_name": "John",
  "last_name": "Doe"
}
```
- Réponse (JSON) :
```json
{
  "first_name": "John",
  "last_name": "Doe",
  "info": "Informations fictives pour John Doe"
}
```
> **first_name** - Prénom de la personne.
> **last_name** - Nom de la personne.
> **info** - Informations fictives récupérées.

### 2. Erreurs et Gestion des Réponses n°9

> Si le prénom ou le nom est manquant dans le corps de la requête :
- Réponse (JSON) :
```json
{
  "msg": "Prénom manquant"
}
```

## XI - Obtenir une image aléatoire

### 1. Code pour obtenir une image aléatoire
Cette fonctionnalité permet d'obtenir une image aléatoire.
-  Route : GET /random-image
- Description : Obtenir une image aléatoire.
- URL : http://127.0.0.1:5000/random-image
- Méthode : GET
- Headers : /
- Authorization: Bearer <votre_token_jwt>
- Réponse : Image aléatoire.

### 2. Erreurs et Gestion des Réponses n°10

> Si une erreur se produit lors de la récupération de l'image :
- Réponse (JSON) :
```json
{
  "msg": "Erreur lors de la récupération de l'image"
}
```