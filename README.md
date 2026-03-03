# Notifications_communications

Un système intelligent de notifications et de communications basé sur Flask.

## Description

Ce projet est une application web complète de gestion des notifications utilisant:
- **Backend**: Flask avec SQLAlchemy ORM
- **Base de données**: SQLite
- **Frontend**: HTML, CSS, JavaScript avec Chart.js
- **Authentication**: Flask-Login

## Fonctionnalités

- 🔐 Système d'authentification utilisateur
- 📊 Dashboard interactif avec graphiques
- 🔔 Gestion des notifications intelligentes
- 📧 Système d'alertes configurables
- 🎨 Interface utilisateur responsive

## Structure du projet

```
notification_project/
├── app.py                 # Application principale Flask
├── models.py              # Modèles de données SQLAlchemy
├── init_db.py             # Initialisation de la base de données
├── requirements.txt       # Dépendances Python
├── core/                  # Modules de base
│   ├── notifiers.py      # Système de notifications
│   ├── alert_types.py    # Types d'alertes
│   ├── advanced.py       # Fonctionnalités avancées
│   ├── decorators.py     # Décorateurs personnalisés
│   └── mixins.py         # Mixins pour modèles
├── templates/            # Templates HTML
│   ├── base.html
│   ├── dashboard.html
│   ├── login.html
│   └── send.html
└── static/               # Ressources statiques
    ├── css/              # Feuilles de style
    └── js/               # Scripts JavaScript
```

## Installation

1. Cloner le repository:
```bash
git clone https://github.com/Marus253/notification_project.git
cd notification_project
```

2. Créer un environnement virtuel:
```bash
python -m venv env
source env/bin/activate  # Linux/Mac
env\Scripts\activate     # Windows
```

3. Installer les dépendances:
```bash
pip install -r requirements.txt
```

4. Initialiser la base de données:
```bash
python init_db.py
```

## Utilisation

Lancer l'application:
```bash
python app.py
```

L'application sera accessible à `http://localhost:5000`

## Configuration

Voir [DB_SETUP.md](notification_project/DB_SETUP.md) pour plus de détails sur la configuration de la base de données.

## Auteur

Marus253

## Licence

MIT
