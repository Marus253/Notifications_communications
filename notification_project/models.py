"""
Modèles SQLAlchemy pour la base de données d'alerte
"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    """Modèle pour les utilisateurs"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(120))
    role = db.Column(db.String(20), default='user')  # admin, user, moderator
    phone = db.Column(db.String(20))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    last_login = db.Column(db.DateTime)
    
    # Relations
    notifications = db.relationship('Notification', backref='creator', lazy='dynamic', foreign_keys='Notification.created_by_id')
    received_notifications = db.relationship('UserNotification', backref='user', lazy='dynamic')
    
    def set_password(self, password):
        """Définir le mot de passe hashé"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Vérifier le mot de passe"""
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username}>'


class Notification(db.Model):
    """Modèle pour les notifications"""
    __tablename__ = 'notifications'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    alert_type = db.Column(db.String(50), nullable=False)  # SECURITY, WEATHER, HEALTH, ACADEMIC
    priority = db.Column(db.String(20), default='MEDIUM')  # URGENT, HIGH, MEDIUM, LOW
    status = db.Column(db.String(20), default='PENDING')  # PENDING, SENT, FAILED
    created_by_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    sent_at = db.Column(db.DateTime)
    icon = db.Column(db.String(50))
    
    # Relations
    recipients = db.relationship('UserNotification', backref='notification', lazy='dynamic', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Notification {self.title}>'


class UserNotification(db.Model):
    """Modèle de liaison entre utilisateurs et notifications"""
    __tablename__ = 'user_notifications'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    notification_id = db.Column(db.Integer, db.ForeignKey('notifications.id'), nullable=False, index=True)
    read = db.Column(db.Boolean, default=False)
    read_at = db.Column(db.DateTime)
    received_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def mark_as_read(self):
        """Marquer la notification comme lue"""
        self.read = True
        self.read_at = datetime.utcnow()
    
    def __repr__(self):
        return f'<UserNotification user_id={self.user_id} notification_id={self.notification_id}>'


class AlertLog(db.Model):
    """Modèle pour l'historique des alertes"""
    __tablename__ = 'alert_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    notification_id = db.Column(db.Integer, db.ForeignKey('notifications.id'))
    action = db.Column(db.String(50), nullable=False)  # created, sent, failed, read
    details = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    def __repr__(self):
        return f'<AlertLog {self.action}>'


class NotificationChannel(db.Model):
    """Modèle pour les canaux de notification"""
    __tablename__ = 'notification_channels'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    channel_type = db.Column(db.String(50), nullable=False)  # SMS, EMAIL, PUSH
    channel_address = db.Column(db.String(200), nullable=False)
    is_verified = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<NotificationChannel {self.channel_type}>'
