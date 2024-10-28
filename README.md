# Squelette de projet Flask

## Installation

1. Cloner le dépôt

`git@github.com:DominicTremblay/Flask-Boilerplate.git`

2. Créer un fichier `.env` à la racine du projet

```
SECRET_KEY='votre_clé_secrète'
DATABASE_URL=sqlite:///films.db
FLASK_ENV=development
FLASK_DEBUG=1
```

3. Créer un environnement virtuel

`python -m venv venv`

4. Activer l'environnement virtuel

- Windows: `venv\Scripts\activate`
- MacOS/Linux: `source venv/bin/activate`

5. Installer les dépendances

`pip install -r requirements.txt`

6. Créer la base de données

`flask db upgrade`

7. Entrer les données de test

`flask seed run`

8. Démarrer le serveur

`flask run`

9. Ouvrir un navigateur et aller à l'adresse `http://localhost:5000`





