```markdown
# 🚨 Système de Notification Intelligent — UPC

**Projet M1 — POO Avancée**

---

## Description

Système de notification modulable destiné à l'UPC pour gérer et diffuser des alertes (sécurité, santé, météo, académique) via plusieurs canaux (email, SMS, push). Le projet met l'accent sur la conception orientée objet : mixins, décorateurs, gestion des priorités et extensibilité.

## Contenu du dépôt
- `app.py` : point d'entrée minimal pour lancer l'application.
- `core/` : logique principale (notifiers, alertes, décorateurs, mixins).
- `templates/`, `static/` : interface web minimale pour envoi/démonstration.
- `requirements.txt` : dépendances Python.

## Installation rapide
1. Créez et activez un environnement virtuel (Windows PowerShell) :

```powershell
python -m venv env
env\Scripts\Activate.ps1
```

2. Installez les dépendances :

```powershell
pip install -r requirements.txt
```

## Lancer l'application
1. Démarrer l'application (exemple) :

```powershell
python app.py
```

2. Ouvrir dans un navigateur : `http://127.0.0.1:5000` (si Flask est utilisé).

## Utilisation (exemples)
- Envoyer une alerte depuis l'interface web `Send`.
- Exemple de script (approche programmatique) :

```python
from core.notifiers import NotificationManager
manager = NotificationManager()
manager.send_alert(type='securite', message='Test intrusion', priority='urgent')
```

## Configuration
- Préférences et paramètres (fichiers ou variables d'environnement) peuvent être définis dans `core/` ou via le fichier `config` si présent.

## Structure de développement
- `core/notifiers.py` : gestion des canaux et stratégies de secours.
- `core/alert_types.py` : définitions des types d'alertes et priorités.
- `core/decorators.py` : décorateurs utilitaires pour logs/retentatives.
- `core/mixins.py` : comportements réutilisables.

## Tests & validation
- Pas de suite de tests automatisés incluse par défaut. Pour tester manuellement : lancer `app.py` et envoyer des alertes via l'interface.

## Contribuer
1. Forker le dépôt.
2. Créer une branche feature/bugfix.
3. Ouvrir une Pull Request avec description des changements.

## Contact
- Auteur / Équipe : voir l'en-tête du projet ou contacter le responsable pédagogique.

---

Merci d'utiliser ce projet — dites-moi si vous souhaitez que j'ajoute :
- une documentation d'API détaillée
- des exemples d'intégration SMS/Email (faux providers pour tests)
- une suite de tests automatisés
```
Frontend:      HTML5, CSS3, JavaScript (Bootstrap 5.1)
Backend:       Python 3.9+, Flask 2.3
Base de données: SQLite (dev) / PostgreSQL (prod)
API:           RESTful avec JSON
Concepts POO:  Mixins, Héritage multiple, Décorateurs, Descripteurs, Métaclasses
```

### Diagramme d'Architecture Détaillé
```
┌─────────────────────────────────────────────────────────────────┐
│                    COUCHE PRÉSENTATION (Frontend)               │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐  │
│  │   Templates     │  │   CSS/JS        │  │   Bootstrap     │  │
│  │   HTML          │  │   Personnalisés │  │   Components    │  │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘  │
└───────────────────────────────┬─────────────────────────────────┘
                                │
┌───────────────────────────────▼─────────────────────────────────┐
│                    COUCHE APPLICATION (Flask) App.py                  │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐            │
│  │   Routes    │  │   Views      │  │   Models    │            │
│  │   (URLs)    │  │   (Logique)  │  │   (Données) │            │
│  └─────────────┘  └─────────────┘  └─────────────┘            │
└───────────────────────────────┬─────────────────────────────────┘
                                │
┌───────────────────────────────▼─────────────────────────────────┐
│                    COUCHE DOMAINE (POO Avancée)                 │
│  ┌─────────────────────────────────────────────────────────┐  │
│  │                    PACKAGE CORE                         │  │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌────────┐  │  │
│  │  │  Mixins  │  │Décorateurs│  │ Héritage │  │Alertes │  │  │
│  │  └──────────┘  └──────────┘  └──────────┘  └────────┘  │  │
│  │  ┌──────────┐  ┌──────────┐                            │  │
│  │  │Descript. │  │Métaclasse│                            │  │
│  │  └──────────┘  └──────────┘                            │  │
│  └─────────────────────────────────────────────────────────┘  │
└───────────────────────────────────────────────────────────────┘
```

---

## 📁 Structure des Fichiers

### Arborescence Complète
```
notification_flask/
├── 📄 README.md                      # Ce fichier
├── 📄 app.py                         # Application Flask principale
├── 📄 requirements.txt               # Dépendances Python
├── 📄 config.py                      # Configuration Flask
├── 📄 .env.example                   Variables d'environnement
│
├── 📁 core/                          # CŒUR POO DU PROJET
│   ├── 📄 __init__.py                # Package Python
│   ├── 📄 mixins.py                  # SMSMixin, EmailMixin, PushMixin
│   ├── 📄 decorators.py              # log_notification, priority, retry_on_failure
│   ├── 📄 notifiers.py               # EmergencyNotifier (MRO)
│   ├── 📄 alert_types.py             # 4 types d'alerte
│   └── 📄 advanced.py                # Descripteurs, Métaclasse
│
├── 📁 static/                        # FICHIERS STATIQUES
│   ├── 📁 css/
│   │   ├── 📄 style.css             # Styles principaux
│   │   └── 📄 dashboard.css         # Styles dashboard
│   │
│   └── 📁 js/
│       ├── 📄 main.js               # JavaScript principal
│       └── 📄 charts.js             # Graphiques (optionnel)
│
├── 📁 templates/                     # TEMPLATES HTML
│   ├── 📄 base.html                 # Template de base
│   ├── 📄 index.html                # Page d'accueil
│   ├── 📄 send.html                 # Envoyer notification
│   ├── 📄 dashboard.html            # Dashboard
│   ├── 📄 demo_poo.html             # Démonstration POO
│   ├── 📄 login.html                # Connexion
│   └── 📄 404.html                  # Page 404
│
└── 📁 tests/                         # TESTS
    ├── 📄 test_mixins.py
    ├── 📄 test_decorators.py
    ├── 📄 test_mro.py
    └── 📄 test_integration.py
```

---

## 🚀 Guide d'Installation

### Prérequis
- Python 3.9 ou supérieur
- pip (gestionnaire de paquets Python)
- Navigateur web moderne

### Installation Étape par Étape

#### Étape 1 : Cloner ou Créer le Projet
```bash
# Créer un nouveau dossier
mkdir notification_flask
cd notification_flask

# Créer l'environnement virtuel
python -m venv venv

# Activer l'environnement
# Sur Windows :
venv\Scripts\activate
# Sur Mac/Linux :
source venv/bin/activate
```

#### Étape 2 : Installer les Dépendances
```bash
# Installer Flask
pip install Flask

# Ou installer toutes les dépendances depuis requirements.txt
pip install -r requirements.txt
```

#### Étape 3 : Configuration
```bash
# Copier le fichier d'environnement
cp .env.example .env

# Éditer .env avec vos configurations
# SECRET_KEY=votre_clé_secrète
# DATABASE_URL=sqlite:///notifications.db
```

#### Étape 4 : Lancer l'Application
```bash
# Développement
python app.py

# Production (avec Gunicorn)
gunicorn app:app
```

L'application sera disponible à : **http://localhost:5000**

---

## 📖 Guide d'Utilisation

### 1. 🏠 Page d'Accueil
**URL :** `/`  
**Description :** Présentation du projet avec :
- Vue d'ensemble des fonctionnalités
- Dernières notifications
- Accès rapide aux principales actions
- Explication des concepts POO

### 2. 📤 Envoyer une Notification
**URL :** `/send`  
**Étapes :**
1. Sélectionner le type d'alerte
2. Rédiger le message
3. Cliquer sur "Envoyer"
4. Observer les logs dans la console

**Types d'alerte disponibles :**
- 🚨 **Sécurité** (URGENT) → SMS + Email + Push
- 🌧️ **Météo** (MOYENNE) → Email
- 🏥 **Santé** (HAUTE) → SMS + Email
- 📚 **Académique** (BASSE) → Email

### 3. 📊 Dashboard
**URL :** `/dashboard`  
**Fonctionnalités :**
- Statistiques en temps réel
- Graphiques des types d'alerte
- Historique complet
- Taux de confirmation
- MRO (Method Resolution Order)

### 4. 🧪 Démonstration POO
**URL :** `/demo-poo`  
**Concepts démontrés :**
- Mixins en action
- Héritage multiple
- Décorateurs avec *args/**kwargs
- Descripteurs de validation
- Métaclasses

### 5. 🔐 Connexion
**URL :** `/login`  
**Comptes de test :**
- Utilisateur : `admin` / Mot de passe : `admin123`
- Utilisateur : `etudiant` / Mot de passe : `etu123`

---

## 🧠 Concepts POO Expliqués

### 1. Les Mixins (core/mixins.py)
**Définition :** Classes conçues pour être combinées avec d'autres classes, pas utilisées seules.

**Code exemple :**
```python
class SMSMixin:
    """Ajoute la fonctionnalité d'envoi SMS"""
    def send_sms(self, message):
        print(f"[SMS] {message}")

# Utilisation :
class SecurityAlert(SMSMixin, EmailMixin, PushMixin):
    """Combine 3 fonctionnalités"""
    pass
```

**Pourquoi utiliser des Mixins ?**
- Évite l'héritage profond
- Facilite la réutilisation du code
- Permet la composition flexible

### 2. Héritage Multiple & MRO (core/notifiers.py)
**Définition :** Une classe peut hériter de plusieurs parents. Le MRO détermine l'ordre de recherche des méthodes.

**Code exemple :**
```python
class EmergencyNotifier(SecurityMixin, WeatherMixin, HealthMixin, AcademicMixin):
    """Hérite de 4 classes différentes"""
    pass

# Afficher le MRO
print(EmergencyNotifier.__mro__)
# (<class '__main__.EmergencyNotifier'>, 
#  <class '__main__.SecurityMixin'>, 
#  <class '__main__.WeatherMixin'>, 
#  <class '__main__.HealthMixin'>, 
#  <class '__main__.AcademicMixin'>, 
#  <class 'object'>)
```

**Comment Python résout les méthodes ?**
1. Cherche dans la classe elle-même
2. Cherche dans la première classe parent
3. Cherche dans les classes suivantes selon le MRO
4. Cherche dans la classe `object` (racine)

### 3. Décorateurs avec *args/**kwargs (core/decorators.py)
**Définition :** Fonctions qui modifient le comportement d'autres fonctions.

**Code exemple :**
```python
def log_notification(func):
    """Décorateur qui log les appels de fonction"""
    def wrapper(*args, **kwargs):
        print(f"[LOG] Appel de {func.__name__}")
        return func(*args, **kwargs)  # *args et **kwargs acceptent n'importe quels arguments
    return wrapper

@log_notification
@priority("URGENT")
def send_alert(message):
    print(f"🚨 {message}")
```

**Pourquoi *args et **kwargs ?**
- `*args` : accepte un nombre variable d'arguments positionnels
- `**kwargs` : accepte un nombre variable d'arguments nommés
- Permet aux décorateurs de fonctionner avec n'importe quelle fonction

### 4. Descripteurs (core/advanced.py)
**Définition :** Objets qui contrôlent l'accès aux attributs.

**Code exemple :**
```python
class PriorityDescriptor:
    """Valide que la priorité est valide"""
    def __set__(self, obj, value):
        valid = ["LOW", "MEDIUM", "HIGH", "URGENT"]
        if value not in valid:
            raise ValueError(f"Priorité invalide: {value}")
        # Stocke la valeur
```

**Utilisation :**
```python
class Notification:
    priority = PriorityDescriptor()  # Validation automatique !
    
notif = Notification()
notif.priority = "URGENT"  # OK
notif.priority = "INVALIDE"  # ❌ Lève ValueError
```

### 5. Métaclasses (core/advanced.py)
**Définition :** Classes qui créent des classes.

**Code exemple :**
```python
class NotificationMeta(type):
    """Métaclasse qui enregistre automatiquement les classes"""
    registry = {}
    
    def __new__(cls, name, bases, attrs):
        # Crée la classe
        new_class = super().__new__(cls, name, bases, attrs)
        
        # Enregistre automatiquement
        cls.registry[name] = new_class
        
        return new_class

class BaseNotification(metaclass=NotificationMeta):
    """Utilise la métaclasse"""
    pass
```

**Quand utiliser une métaclasse ?**
- Pour enregistrer automatiquement des classes
- Pour ajouter des méthodes à toutes les classes
- Pour générer du code automatiquement

---

## 🔧 Pour les Développeurs

### Structure du Code Flask

#### `app.py` - Le Cerveau de l'Application
```python
# 1. Importation des modules
from flask import Flask, render_template, request

# 2. Création de l'application
app = Flask(__name__)

# 3. Définition des routes
@app.route('/')
def index():
    """Affiche la page d'accueil"""
    return render_template('index.html')

# 4. Lancement du serveur
if __name__ == '__main__':
    app.run(debug=True)
```

#### Comment Ajouter une Nouvelle Route
```python
@app.route('/nouvelle-page')
def nouvelle_page():
    # Logique métier ici
    donnees = {"titre": "Nouvelle Page", "message": "Bienvenue!"}
    return render_template('nouvelle_page.html', **donnees)
```

#### Comment Utiliser les Classes POO dans Flask
```python
from core.alert_types import SecurityAlert

@app.route('/send-security', methods=['POST'])
def send_security():
    message = request.form.get('message')
    
    # Utilisation des classes POO
    alert = SecurityAlert(message)
    result = alert.send()  # Utilise mixins + décorateurs
    
    return jsonify({"status": "success", "result": result})
```

### Extensions Flask Utiles

| Extension | Utilité | Installation |
|-----------|---------|--------------|
| Flask-SQLAlchemy | ORM pour base de données | `pip install flask-sqlalchemy` |
| Flask-Login | Gestion d'authentification | `pip install flask-login` |
| Flask-WTF | Formulaires web | `pip install flask-wtf` |
| Flask-Mail | Envoi d'emails | `pip install flask-mail` |

### Bonnes Pratiques de Code

#### 1. Organisation des Imports
```python
# 1. Imports standards Python
import os
import json
from datetime import datetime

# 2. Imports tiers
from flask import Flask, render_template
import sqlalchemy as sa

# 3. Imports locaux
from core.mixins import SMSMixin
from models import Notification
```

#### 2. Documentation des Fonctions
```python
def envoyer_notification(message, type_alerte):
    """
    Envoie une notification via les canaux appropriés.
    
    Parameters:
    -----------
    message : str
        Le message à envoyer
    type_alerte : str
        Type d'alerte ('SECURITY', 'WEATHER', etc.)
    
    Returns:
    --------
    dict
        Résultat de l'envoi avec statut et détails
    
    Raises:
    -------
    ValueError
        Si le type d'alerte est invalide
    """
    # Implémentation...
```

#### 3. Gestion des Erreurs
```python
try:
    alert = SecurityAlert(message)
    result = alert.send()
except ValueError as e:
    # Erreur de validation
    return jsonify({"error": str(e)}), 400
except Exception as e:
    # Erreur inattendue
    app.logger.error(f"Erreur: {str(e)}")
    return jsonify({"error": "Erreur interne"}), 500
```

---

## 🧪 Tests et Démonstration

### Tests Automatisés
```bash
# Exécuter tous les tests
python -m pytest tests/

# Tests spécifiques
python -m pytest tests/test_mixins.py
python -m pytest tests/test_mro.py -v  # Mode verbeux
```

### Scénarios de Démo

#### Scénario 1 : Alerte de Sécurité
1. Aller sur `/send`
2. Sélectionner "Sécurité"
3. Entrer : "Intrusion détectée au bâtiment A"
4. Cliquer sur "Envoyer"
5. Observer dans la console :
   ```
   [LOG] Appel de send
   [PRIORITY] Niveau: URGENT
   [SMS] [URGENT] Intrusion détectée...
   [EMAIL] Alerte Sécurité: Intrusion...
   [PUSH] 🚨 Intrusion détectée...
   ```

#### Scénario 2 : Démonstration MRO
1. Aller sur `/demo-poo`
2. Cliquer sur "Tester le MRO"
3. Observer l'affichage :
   ```
   0. <class 'core.notifiers.EmergencyNotifier'>
   1. <class 'core.notifiers.SecurityEmergencyMixin'>
   2. <class 'core.notifiers.WeatherEmergencyMixin'>
   3. <class 'core.notifiers.HealthEmergencyMixin'>
   4. <class 'core.notifiers.AcademicEmergencyMixin'>
   5. <class 'object'>
   ```

### API de Test
```bash
# Tester l'API
curl -X POST http://localhost:5000/api/send \
  -H "Content-Type: application/json" \
  -d '{"type": "SECURITY", "message": "Test API"}'

# Réponse :
{
  "status": "success",
  "result": "Alerte sécurité envoyée sur 3 canaux",
  "timestamp": "2024-01-15T10:30:00"
}
```

---

## 📊 Évaluation

### Grille d'Évaluation - Partie 1 (POO)

| Critère | Poids | Description |
|---------|-------|-------------|
| Qualité de la conception OOP | 30% | Architecture propre, bonnes pratiques |
| Utilisation des mixins et héritage multiple | 25% | MRO compris et appliqué |
| Implémentation des décorateurs avec *args/**kwargs | 20% | Décorateurs flexibles et réutilisables |
| Présentation et démonstration | 15% | Clarté, professionnalisme |
| Collaboration et discussion technique | 10% | Travail d'équipe, justifications |

### Grille d'Évaluation - Partie 2 (Application Web)

| Critère | Poids | Description |
|---------|-------|-------------|
| Décorateurs de classes | 15% | Implémentation correcte |
| Descripteurs | 15% | Validation automatique des données |
| Métaclasses | 15% | Génération de code automatique |
| Qualité de l'application web | 20% | Interface, fonctionnalités, UX |
| Présentation & analyse technique | 15% | Explication des choix techniques |
| Démo & Q/R | 10% | Démonstration fluide, réponses claires |
| Documentation | 10% | Complète et professionnelle |

---

## 📚 Références

### Documentation Officielle
- [Python Documentation](https://docs.python.org/3/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Bootstrap 5 Documentation](https://getbootstrap.com/docs/5.1/)

### Ressources POO Avancée
- [Python Mixins Explained](https://realpython.com/python-mixin/)
- [Understanding Python MRO](https://www.python.org/download/releases/2.3/mro/)
- [Python Decorators Guide](https://realpython.com/primer-on-python-decorators/)
- [Descriptors HowTo Guide](https://docs.python.org/3/howto/descriptor.html)
- [Metaclasses in Python](https://realpython.com/python-metaclasses/)

### Projets Similaires
- [Django Notifications](https://github.com/django-notifications/django-notifications)
- [Flask-User](https://github.com/lingthio/Flask-User)
- [Python-Pushover](https://github.com/scolby33/pushover)

### Outils de Développement
- [Postman](https://www.postman.com/) - Test d'APIs
- [DB Browser for SQLite](https://sqlitebrowser.org/) - Visualisation de bases de données
- [VS Code](https://code.visualstudio.com/) - Éditeur de code
- [Git](https://git-scm.com/) - Contrôle de version

---

## 🤝 Contribution

### Pour Contribuer au Projet
1. Fork le projet
2. Créer une branche (`git checkout -b feature/ma-fonctionnalite`)
3. Commit les changements (`git commit -m 'Ajout de ma fonctionnalité'`)
4. Push vers la branche (`git push origin feature/ma-fonctionnalite`)
5. Ouvrir une Pull Request

### Normes de Code
- Suivre [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- Commenter le code en français
- Ajouter des docstrings complètes
- Écrire des tests unitaires

---

## 📞 Support

### En Cas de Problème
1. **Vérifier les logs** : `python app.py` affiche les erreurs
2. **Vérifier les imports** : Tous les modules sont-ils installés ?
3. **Consulter la documentation** : Les concepts sont expliqués ci-dessus
4. **Demander de l'aide** : Créer une issue sur GitHub

### Pour les Étudiants
Ce projet est conçu pour être **éducatif**. Chaque fichier contient des commentaires explicatifs. Prenez le temps de :
1. Lire les commentaires dans le code
2. Exécuter les tests pour comprendre
3. Modifier le code pour expérimenter
4. Consulter les ressources de référence

---

## 🎓 Conclusion

Ce projet démontre comment les concepts avancés de POO peuvent être appliqués à un problème réel. Il combine :

1. **Théorie POO** : Mixins, héritage multiple, décorateurs, descripteurs, métaclasses
2. **Pratique Web** : Application Flask complète avec interface utilisateur
3. **Bonnes pratiques** : Code organisé, documentation, tests

**Compétences développées :**
- Architecture logicielle
- Programmation orientée objet avancée
- Développement web avec Flask
- Collaboration en équipe
- Présentation technique

**Pour aller plus loin :**
- Ajouter une base de données réelle (PostgreSQL)
- Implémenter l'envoi réel de SMS/Email
- Ajouter une interface d'administration
- Déployer sur un serveur (Heroku, AWS)

---

*Projet réalisé dans le cadre du cours de POO Avancée - M1 Génie Logiciel - UPC*  
*© 2026 - Tous droits réservés*
```
