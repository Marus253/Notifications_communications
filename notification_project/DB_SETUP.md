# 🗄️ Configuration de la Base de Données - Système de Notification

## 📋 Fichiers créés

### 1. **models.py** - Modèles SQLAlchemy
Définit la structure de la base de données avec les tables :
- `users` : Utilisateurs du système
- `notifications` : Les alertes/notifications
- `user_notifications` : Liaison utilisateurs-notifications
- `notification_channels` : Canaux de communication (SMS, EMAIL, PUSH)
- `alert_logs` : Historique des actions

### 2. **init_db.py** - Script d'initialisation
Script pour créer et populer la base de données avec les données initiales.

### 3. **schema.sql** - Schéma SQL
Fichier SQL pur montrant la structure complète de la base de données.

### 4. **login.html** - Page de connexion
Interface de login stylisée avec Bootstrap 5.

### 5. **app.py** - Mise à jour
Intégration de SQLAlchemy, Flask-Login et routes d'authentification.

---

## 🚀 Installation et initialisation

### Étape 1 : Installer les dépendances
```bash
pip install -r requirements.txt
```

### Étape 2 : Initialiser la base de données
```bash
python init_db.py
```

Cela va :
- ✅ Créer toutes les tables
- ✅ Ajouter 3 utilisateurs de test
- ✅ Créer des canaux de notification
- ✅ Ajouter des données d'exemple

### Étape 3 : Lancer l'application
```bash
python app.py
```

---

## 🔐 Comptes de test par défaut

| Username | Mot de passe | Rôle | Email |
|----------|-------------|------|-------|
| `admin` | `admin123` | Admin | admin@upc.edu |
| `etudiant` | `etu123` | User | etudiant@upc.edu |
| `moderator` | `mod123` | Moderator | moderator@upc.edu |

### Accès à la connexion
- **URL** : `http://localhost:5000/login`
- **Page d'accueil** : `http://localhost:5000/`

---

## 📊 Structure de la base de données

### Table `users`
```sql
id (PK)
username (UNIQUE)
email (UNIQUE)
password_hash
full_name
role (admin | user | moderator)
phone
is_active
created_at
last_login
```

### Table `notifications`
```sql
id (PK)
title
message
alert_type (SECURITY | WEATHER | HEALTH | ACADEMIC)
priority (URGENT | HIGH | MEDIUM | LOW)
status (PENDING | SENT | FAILED)
created_by_id (FK users.id)
created_at
sent_at
icon
```

### Table `user_notifications` (Many-to-Many)
```sql
id (PK)
user_id (FK)
notification_id (FK)
read (Boolean)
read_at
received_at
```

### Table `notification_channels`
```sql
id (PK)
user_id (FK)
channel_type (SMS | EMAIL | PUSH)
channel_address
is_verified
is_active
created_at
```

### Table `alert_logs`
```sql
id (PK)
notification_id (FK)
action (created | sent | failed | read)
details
created_at
```

---

## 🎯 Cas d'usage

### Scénario 1 : Créer une notification
```python
from models import db, User, Notification, UserNotification

# Créer une notification
notif = Notification(
    title="Alerte Sécurité",
    message="Incident détecté",
    alert_type="SECURITY",
    priority="URGENT",
    created_by_id=1
)
db.session.add(notif)
db.session.commit()

# Assigner à un utilisateur
user_notif = UserNotification(
    user_id=2,
    notification_id=notif.id
)
db.session.add(user_notif)
db.session.commit()
```

### Scénario 2 : Récupérer les notifications non lues
```python
from models import User, UserNotification

user = User.query.get(2)
unread = user.received_notifications.filter_by(read=False).all()
print(f"{len(unread)} notifications non lues")
```

### Scénario 3 : Marquer comme lue
```python
user_notif = UserNotification.query.get(1)
user_notif.mark_as_read()
db.session.commit()
```

---

## 🛠️ Utilitaires

### Réinitialiser la base de données
```bash
# Supprimer la base actuelle
rm notifications.db

# Recréer et repeupler
python init_db.py
```

### Interroger la base de données directement
```bash
python
>>> from app import app, db
>>> from models import User, Notification
>>> with app.app_context():
>>>     users = User.query.all()
>>>     for user in users:
>>>         print(f"{user.username}: {user.email}")
```

---

## 🔄 Routes Flask

| Route | Méthode | Description |
|-------|---------|-------------|
| `/` | GET | Page d'accueil |
| `/login` | GET, POST | Connexion utilisateur |
| `/logout` | GET | Déconnexion |
| `/send` | GET, POST | Envoyer une notification |
| `/dashboard` | GET | Dashboard des statistiques |
| `/demo-poo` | GET | Démo des concepts POO |

---

## 📝 Notes importantes

1. **Base de données SQLite** : Utilisée pour la simplicité (fichier `notifications.db`)
2. **Hashage de mots de passe** : Utilise PBKDF2-SHA256 via Werkzeug
3. **Zones horaires** : Toutes les dates/heures sont en UTC
4. **Cascade delete** : Les relation parent-enfant sont cascadées
5. **Indexes** : Créés sur les colonnes fréquemment interrogées

---

## 🐛 Dépannage

### Erreur "database is locked"
```bash
rm notifications.db
python init_db.py
```

### Mots de passe oubliés
Les mots de passe de test sont hashés dans le code. Pour créer un nouvel utilisateur :
```python
from app import app, db
from models import User

with app.app_context():
    user = User(
        username="newuser",
        email="new@example.com",
        full_name="New User",
        role="user"
    )
    user.set_password("password123")
    db.session.add(user)
    db.session.commit()
```

---

## 📚 Références

- [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/)
- [Flask-Login](https://flask-login.readthedocs.io/)
- [SQLAlchemy ORM](https://docs.sqlalchemy.org/)
- [Werkzeug Security](https://werkzeug.palletsprojects.com/en/stable/security/)

---

**Version** : 1.0  
**Date** : <03-03-2026>  
**Auteur** : Système de Notification UPC
