"""
Script pour initialiser la base de données
Utilisation: python init_db.py
"""

import os
import sys
from app import app, db
from models import User, Notification, UserNotification, AlertLog, NotificationChannel
from datetime import datetime, timedelta

def init_database():
    """Initialiser la base de données avec les tables et données"""
    
    print("🗄️  Initialisation de la base de données...")
    
    # Créer toutes les tables
    with app.app_context():
        print("📝 Création des tables...")
        db.create_all()
        print("✅ Tables créées avec succès!")
        
        # Vérifier si les utilisateurs existent déjà
        admin_exists = User.query.filter_by(username='admin').first()
        
        if admin_exists:
            print("⚠️  Les utilisateurs existent déjà, passage de l'insertion des données...")
            return
        
        # Créer les utilisateurs par défaut
        print("\n👥 Création des utilisateurs par défaut...")
        
        admin = User(
            username='admin',
            email='admin@upc.edu',
            full_name='Administrateur',
            role='admin',
            phone='+33612345678',
            is_active=True
        )
        admin.set_password('admin123')
        
        etudiant = User(
            username='etudiant',
            email='etudiant@upc.edu',
            full_name='Étudiant Test',
            role='user',
            phone='+33687654321',
            is_active=True
        )
        etudiant.set_password('etu123')
        
        moderator = User(
            username='moderator',
            email='moderator@upc.edu',
            full_name='Modérateur',
            role='moderator',
            phone='+33698765432',
            is_active=True
        )
        moderator.set_password('mod123')
        
        db.session.add(admin)
        db.session.add(etudiant)
        db.session.add(moderator)
        db.session.commit()
        
        print(f"✅ Utilisateurs créés :")
        print(f"   - admin (admin123)")
        print(f"   - etudiant (etu123)")
        print(f"   - moderator (mod123)")
        
        # Créer les canaux de notification pour les utilisateurs
        print("\n📢 Création des canaux de notification...")
        
        channels = [
            NotificationChannel(user_id=admin.id, channel_type='EMAIL', channel_address='admin@upc.edu', is_verified=True, is_active=True),
            NotificationChannel(user_id=admin.id, channel_type='SMS', channel_address='+33612345678', is_verified=True, is_active=True),
            NotificationChannel(user_id=etudiant.id, channel_type='EMAIL', channel_address='etudiant@upc.edu', is_verified=True, is_active=True),
            NotificationChannel(user_id=etudiant.id, channel_type='PUSH', channel_address='push_token_etudiant', is_verified=True, is_active=True),
            NotificationChannel(user_id=moderator.id, channel_type='EMAIL', channel_address='moderator@upc.edu', is_verified=True, is_active=True),
        ]
        
        for channel in channels:
            db.session.add(channel)
        
        db.session.commit()
        print(f"✅ {len(channels)} canaux de notification créés")
        
        # Créer quelques notifications d'exemple
        print("\n🔔 Création des notifications d'exemple...")
        
        notifications_data = [
            {
                'title': 'Alerte Sécurité - Campus',
                'message': 'Un incident de sécurité a été détecté sur le campus. Veuillez rester vigilant.',
                'alert_type': 'SECURITY',
                'priority': 'URGENT',
                'icon': '🚨'
            },
            {
                'title': 'Alerte Météorologique',
                'message': 'Un orage est prévu sur la région. Recommandation de rester en intérieur.',
                'alert_type': 'WEATHER',
                'priority': 'HIGH',
                'icon': '🌧️'
            },
            {
                'title': 'Alerte Santé - Vaccination',
                'message': 'Rappel : les vaccins sont obligatoires pour accéder campus.',
                'alert_type': 'HEALTH',
                'priority': 'MEDIUM',
                'icon': '🏥'
            },
            {
                'title': 'Alerte Académique - Examens',
                'message': 'Les examens de fin semestre commencent le 15 mars.',
                'alert_type': 'ACADEMIC',
                'priority': 'LOW',
                'icon': '📚'
            }
        ]
        
        for notif_data in notifications_data:
            notification = Notification(
                title=notif_data['title'],
                message=notif_data['message'],
                alert_type=notif_data['alert_type'],
                priority=notif_data['priority'],
                icon=notif_data['icon'],
                created_by_id=admin.id,
                status='SENT',
                sent_at=datetime.utcnow() - timedelta(days=2)
            )
            db.session.add(notification)
            db.session.flush()
            
            # Ajouter pour tous les utilisateurs
            for user in [admin, etudiant, moderator]:
                user_notif = UserNotification(
                    user_id=user.id,
                    notification_id=notification.id,
                    read=(user.id == admin.id)  # Admin a lu tous les messages
                )
                db.session.add(user_notif)
        
        db.session.commit()
        print(f"✅ {len(notifications_data)} notifications d'exemple créées")
        
        # Créer des logs d'alerte
        print("\n📊 Création des logs d'alerte...")
        
        alert_logs = [
            AlertLog(notification_id=1, action='created', details='Notification créée par admin'),
            AlertLog(notification_id=1, action='sent', details='Notification envoyée à 3 utilisateurs'),
            AlertLog(notification_id=2, action='created', details='Alerte météo créée'),
            AlertLog(notification_id=2, action='sent', details='Envoyée via EMAIL et PUSH'),
        ]
        
        for log in alert_logs:
            db.session.add(log)
        
        db.session.commit()
        print(f"✅ {len(alert_logs)} logs d'alerte créés")
        
        print("\n" + "="*50)
        print("✨ Base de données initialisée avec succès!")
        print("="*50)
        
        print("\n📋 Résumé :")
        print(f"   - {User.query.count()} utilisateurs")
        print(f"   - {Notification.query.count()} notifications")
        print(f"   - {NotificationChannel.query.count()} canaux")
        print(f"   - {AlertLog.query.count()} logs d'alerte")
        
        print("\n🔑 Comptes de connexion :")
        print("   URL: http://localhost:5000/login")
        print("   - admin / admin123")
        print("   - etudiant / etu123")
        print("   - moderator / mod123")


if __name__ == '__main__':
    init_database()
