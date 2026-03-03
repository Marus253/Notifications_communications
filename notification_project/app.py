"""
Application Flask du système de notification
Utilise les classes core/ et SQLAlchemy pour la base de données
"""

from flask import Flask, render_template, request, jsonify, flash, redirect, url_for, session
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
import json
import os
from datetime import datetime

# Importe TES classes
from core.alert_types import SecurityAlert, WeatherAlert, HealthAlert, AcademicAlert
from core.notifiers import EmergencyNotifier
from core.advanced import NotificationMeta, UserNotification
from models import db, User, Notification, UserNotification as DBUserNotification, AlertLog, NotificationChannel

app = Flask(__name__)
app.secret_key = 'secret-key-123-notification'

# Configuration de la base de données
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "notifications.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialiser la base de données
db.init_app(app)

# Initialiser Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = "Veuillez vous connecter pour accéder à cette page."
login_manager.login_message_category = "warning"

# Faire User compatible avec Flask-Login
User.is_authenticated = property(lambda self: True)
User.is_anonymous = property(lambda self: False)
User.get_id = lambda self: str(self.id)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Données en mémoire (pour la compatibilité avec les anciennes routes)
notifications_history = []
users = {
    'admin': {'password': 'admin123', 'name': 'Administrateur'},
    'etudiant': {'password': 'etu123', 'name': 'Étudiant Test'}
}

def is_student_user():
    """Retourne True si l'utilisateur courant est un étudiant (Flask-Login ou session fallback)."""
    try:
        if current_user and getattr(current_user, 'is_authenticated', False):
            return getattr(current_user, 'role', None) == 'student'
    except Exception:
        pass
    # Fallback session username
    if session.get('username') == 'etudiant':
        return True
    return False

# Page d'accueil
@app.route('/')
def index():
    """Page d'accueil"""
    return render_template('index.html', 
                         notifications=notifications_history[-5:],  # 5 dernières
                         total=len(notifications_history))

# Page d'envoi
@app.route('/send', methods=['GET', 'POST'])
def send_notification():
    """Envoyer une notification"""
    # Vérifier l'authentification (Flask-Login ou session fallback)
    is_authenticated = (current_user and getattr(current_user, 'is_authenticated', False)) or session.get('username')
    if not is_authenticated:
        flash('Veuillez vous connecter pour envoyer une notification.', 'warning')
        return redirect(url_for('login'))
    
    if is_student_user():
        flash('Accès refusé : les étudiants ne peuvent pas envoyer de notifications.', 'warning')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        alert_type = request.form.get('alert_type')
        message = request.form.get('message')
        
        if not message:
            flash('Veuillez entrer un message', 'danger')
            return redirect('/send')
        
        print(f"\n{'='*50}")
        print(f"📨 NOUVELLE NOTIFICATION")
        print(f"Type: {alert_type}")
        print(f"Message: {message}")
        print('='*50)
        
        result = ""
        
        try:
            # Utilise TES classes
            if alert_type == 'SECURITY':
                alert = SecurityAlert(message)
                result = alert.send()
                priority = "URGENT"
                icon = "🚨"
                
            elif alert_type == 'WEATHER':
                alert = WeatherAlert(message)
                result = alert.send()
                priority = "MEDIUM"
                icon = "🌧️"
                
            elif alert_type == 'HEALTH':
                alert = HealthAlert(message)
                result = alert.send()
                priority = "HIGH"
                icon = "🏥"
                
            elif alert_type == 'ACADEMIC':
                alert = AcademicAlert(message)
                result = alert.send()
                priority = "LOW"
                icon = "📚"
                
            else:
                flash('Type d\'alerte invalide', 'danger')
                return redirect('/send')
            
            # Sauvegarde dans l'historique
            notifications_history.append({
                'type': alert_type,
                'message': message,
                'priority': priority,
                'icon': icon,
                'timestamp': datetime.now().strftime('%H:%M:%S'),
                'result': result
            })

            # --- Persist to DB: create Notification and link to all students ---
            try:
                notif_title = f"{alert_type} - {priority}"
                new_notif = Notification(
                    title=notif_title,
                    message=message,
                    alert_type=alert_type,
                    priority=priority,
                    status='SENT',
                    created_by_id=(current_user.id if (current_user and getattr(current_user, 'is_authenticated', False)) else None),
                )
                db.session.add(new_notif)
                db.session.commit()

                # Find all student users and create UserNotification entries
                students = User.query.filter_by(role='student').all()
                for stud in students:
                    user_notif = DBUserNotification(user_id=stud.id, notification_id=new_notif.id, read=False)
                    db.session.add(user_notif)
                db.session.commit()
            except Exception as e:
                # Log but don't break the flow
                print('Erreur lors de la sauvegarde en base:', e)
            
            flash(f'{icon} Notification envoyée avec succès!', 'success')
            
        except Exception as e:
            flash(f'Erreur: {str(e)}', 'danger')
            result = f"Erreur: {str(e)}"
        
        return render_template('send.html', result=result)
    
    return render_template('send.html')

# Dashboard
@app.route('/dashboard')
def dashboard():
    """Dashboard avec statistiques"""
    # Vérifier l'authentification (Flask-Login ou session fallback)
    is_authenticated = (current_user and getattr(current_user, 'is_authenticated', False)) or session.get('username')
    if not is_authenticated:
        flash('Veuillez vous connecter pour accéder au dashboard.', 'warning')
        return redirect(url_for('login'))
    
    if is_student_user():
        flash('Accès refusé : les étudiants n\'ont pas accès au dashboard.', 'warning')
        return redirect(url_for('index'))
    
    # Calcule les statistiques
    stats = {
        'total': len(notifications_history),
        'security': sum(1 for n in notifications_history if n['type'] == 'SECURITY'),
        'weather': sum(1 for n in notifications_history if n['type'] == 'WEATHER'),
        'health': sum(1 for n in notifications_history if n['type'] == 'HEALTH'),
        'academic': sum(1 for n in notifications_history if n['type'] == 'ACADEMIC'),
        'urgent': sum(1 for n in notifications_history if n['priority'] == 'URGENT'),
        'high': sum(1 for n in notifications_history if n['priority'] == 'HIGH'),
        'medium': sum(1 for n in notifications_history if n['priority'] == 'MEDIUM'),
        'low': sum(1 for n in notifications_history if n['priority'] == 'LOW'),
    }
    
    # Récupère le MRO pour la démo
    mro_list = []
    try:
        for i, cls in enumerate(EmergencyNotifier.__mro__):
            mro_list.append(str(cls))
    except:
        mro_list = ["MRO non disponible"]
    
    return render_template('dashboard.html', 
                         stats=stats,
                         mro=mro_list,
                         notifications=notifications_history[-10:])


# Boîte de réception personnelle
@app.route('/my-notifications')
def my_notifications():
    """Affiche les notifications reçues par l'utilisateur connecté."""
    # Si l'utilisateur est connecté via la base de données
    try:
        if current_user and getattr(current_user, 'is_authenticated', False):
            # Utiliser le modèle DBUserNotification (liaison user_notifications)
            user_notifs = DBUserNotification.query.filter_by(user_id=current_user.id).order_by(DBUserNotification.received_at.desc()).all()
            # Construire une liste affichable
            items = []
            for un in user_notifs:
                notif = un.notification
                items.append({
                    'type': notif.alert_type if notif else 'N/A',
                    'message': notif.message if notif else getattr(un, 'message', '—'),
                    'priority': notif.priority if notif else 'MEDIUM',
                    'timestamp': un.received_at.strftime('%Y-%m-%d %H:%M:%S') if un.received_at else '',
                    'read': un.read
                })
            return render_template('my_notifications.html', notifications=items)
    except Exception:
        # cas fallback + session
        pass

    # Fallback: si session 'etudiant' présent, afficher l'historique global (démo)
    if session.get('username') == 'etudiant':
        items = list(reversed(notifications_history))
        return render_template('my_notifications.html', notifications=items)

    # Sinon rediriger
    flash('Aucune boîte aux lettres disponible pour cet utilisateur.', 'warning')
    return redirect(url_for('index'))

# Page de démonstration POO
@app.route('/demo-poo')
def demo_poo():
    """Page de démonstration des concepts POO"""
    
    results = {}
    
    # 1. Test des mixins
    from core.mixins import SMSMixin, EmailMixin
    class TestMixin(SMSMixin, EmailMixin):
        pass
    test_mixin = TestMixin()
    results['mixins'] = " Mixins SMS et Email fonctionnels"
    
    # 2. Test du MRO
    from core.notifiers import EmergencyNotifier
    mro_info = EmergencyNotifier("Test").display_mro()
    results['mro'] = f" MRO avec {len(mro_info)} classes"
    
    # 3. Test des décorateurs
    from core.decorators import log_notification
    @log_notification
    def test_func():
        return "Décorateur fonctionnel"
    results['decorators'] = test_func()
    
    # 4. Test des descripteurs
    try:
        notif = UserNotification("Test", priority="HIGH", email="test@campus.edu")
        results['descripteurs'] = f" {notif}"
    except Exception as e:
        results['descripteurs'] = f" {e}"
    
    # 5. Test de la métaclasse
    from core.advanced import NotificationMeta
    registry = NotificationMeta.get_registered_classes()
    results['metaclasse'] = f" {len(registry)} classes enregistrées"
    
    # 6. Test des alertes
    security = SecurityAlert("Test sécurité")
    weather = WeatherAlert("Test météo")
    results['alertes'] = f" Alertes: {security.priority}, {weather.priority}"
    
    return render_template('demo_poo.html', results=results)

# API simple
@app.route('/api/send', methods=['POST'])
def api_send():
    """API pour envoyer des notifications (JSON)"""
    try:
        data = request.get_json()
        alert_type = data.get('type')
        message = data.get('message')
        
        if not alert_type or not message:
            return jsonify({'error': 'Type et message requis'}), 400
        
        # Utilise TES classes
        if alert_type == 'SECURITY':
            alert = SecurityAlert(message)
            result = alert.send()
        elif alert_type == 'WEATHER':
            alert = WeatherAlert(message)
            result = alert.send()
        else:
            return jsonify({'error': 'Type non supporté'}), 400
        
        return jsonify({
            'status': 'success',
            'result': result,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Page de connexion avec base de données
@app.route('/login', methods=['GET', 'POST'])
def login():
    """Page de connexion avec base de données"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        remember = request.form.get('remember', False)
        
        # Vérifier dans la BD d'abord
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password) and user.is_active:
            user.last_login = datetime.utcnow()
            db.session.commit()
            login_user(user, remember=bool(remember))
            flash(f'Bienvenue {user.full_name}! 🎉', 'success')
            return redirect(url_for('index'))
        
        # Fallback sur la mémoire pour compatibilité
        if username in users and users[username]['password'] == password:
            flash(f'Bienvenue {users[username]["name"]}! (mode compatibilité)', 'success')
            session['username'] = username
            session['user_name'] = users[username]['name']
            return redirect(url_for('index'))
        
        flash('Identifiants incorrects. Veuillez réessayer.', 'danger')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    """Déconnexion"""
    logout_user()
    session.clear()
    flash('Vous avez été déconnecté. À bientôt! 👋', 'info')
    return redirect(url_for('login'))

# Page 404
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    with app.app_context():
        # Créer les tables si elles n'existent pas
        db.create_all()
        print(" Lancement de l'application Flask...")
        print(" Configuration de la base de données :")
        print(f"   - Base de données : {app.config['SQLALCHEMY_DATABASE_URI']}")
        print(f"   - Tables créées ✓")
        print("\n Classes POO chargées:")
        print("   - SMSMixin, EmailMixin, PushMixin")
        print("   - SecurityAlert, WeatherAlert, HealthAlert, AcademicAlert")
        print("   - EmergencyNotifier (MRO)")
        print("   - Descripteurs et Métaclasse")
        print("\n 🔐 Routes de connexion :")
        print(f"   - http://localhost:5000/login")
        print(f"   - http://localhost:5000/logout")
        print("\n Serveur démarré sur http://localhost:5000")
    
    app.run(debug=True, port=5000)