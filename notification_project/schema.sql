-- Schema de la base de données du système de notification UPC
-- Database: notifications.db (SQLite)
-- Created: 2026-03-03

-- ==================================================
-- TABLE: users
-- Description: Stocke les informations des utilisateurs
-- ==================================================
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(80) NOT NULL UNIQUE,
    email VARCHAR(120) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(120),
    role VARCHAR(20) DEFAULT 'user',  -- admin, user, moderator
    phone VARCHAR(20),
    is_active BOOLEAN DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    last_login DATETIME,
    INDEX idx_username (username),
    INDEX idx_created_at (created_at)
);

-- ==================================================
-- TABLE: notifications
-- Description: Stocke les notifications/alertes
-- ==================================================
CREATE TABLE IF NOT EXISTS notifications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(200) NOT NULL,
    message TEXT NOT NULL,
    alert_type VARCHAR(50) NOT NULL,  -- SECURITY, WEATHER, HEALTH, ACADEMIC
    priority VARCHAR(20) DEFAULT 'MEDIUM',  -- URGENT, HIGH, MEDIUM, LOW
    status VARCHAR(20) DEFAULT 'PENDING',  -- PENDING, SENT, FAILED
    created_by_id INTEGER NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    sent_at DATETIME,
    icon VARCHAR(50),
    FOREIGN KEY (created_by_id) REFERENCES users(id),
    INDEX idx_alert_type (alert_type),
    INDEX idx_priority (priority),
    INDEX idx_created_at (created_at)
);

-- ==================================================
-- TABLE: user_notifications
-- Description: Liaison entre utilisateurs et notifications (many-to-many)
-- ==================================================
CREATE TABLE IF NOT EXISTS user_notifications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    notification_id INTEGER NOT NULL,
    read BOOLEAN DEFAULT 0,
    read_at DATETIME,
    received_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (notification_id) REFERENCES notifications(id),
    UNIQUE (user_id, notification_id),
    INDEX idx_user_id (user_id),
    INDEX idx_notification_id (notification_id)
);

-- ==================================================
-- TABLE: notification_channels
-- Description: Canaux de notification pour chaque utilisateur
-- ==================================================
CREATE TABLE IF NOT EXISTS notification_channels (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    channel_type VARCHAR(50) NOT NULL,  -- SMS, EMAIL, PUSH
    channel_address VARCHAR(200) NOT NULL,
    is_verified BOOLEAN DEFAULT 0,
    is_active BOOLEAN DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- ==================================================
-- TABLE: alert_logs
-- Description: Historique/logs des actions sur les alertes
-- ==================================================
CREATE TABLE IF NOT EXISTS alert_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    notification_id INTEGER,
    action VARCHAR(50) NOT NULL,  -- created, sent, failed, read
    details TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (notification_id) REFERENCES notifications(id),
    INDEX idx_action (action),
    INDEX idx_created_at (created_at)
);

-- ==================================================
-- INDEXES supplémentaires pour optimisation
-- ==================================================
CREATE INDEX IF NOT EXISTS idx_user_notifications_read ON user_notifications(read);
CREATE INDEX IF NOT EXISTS idx_notifications_status ON notifications(status);
CREATE INDEX IF NOT EXISTS idx_channels_active ON notification_channels(is_active);

-- ==================================================
-- DONNÉES D'EXEMPLE
-- ==================================================

-- Utilisateurs par défaut
INSERT OR IGNORE INTO users (id, username, email, password_hash, full_name, role, phone, is_active)
VALUES 
    (1, 'admin', 'admin@upc.edu', 'pbkdf2:sha256:600000$example$hash', 'Administrateur', 'admin', '+33612345678', 1),
    (2, 'etudiant', 'etudiant@upc.edu', 'pbkdf2:sha256:600000$example$hash', 'Étudiant Test', 'user', '+33687654321', 1),
    (3, 'moderator', 'moderator@upc.edu', 'pbkdf2:sha256:600000$example$hash', 'Modérateur', 'moderator', '+33698765432', 1);

-- Canaux de notification
INSERT OR IGNORE INTO notification_channels (id, user_id, channel_type, channel_address, is_verified, is_active)
VALUES
    (1, 1, 'EMAIL', 'admin@upc.edu', 1, 1),
    (2, 1, 'SMS', '+33612345678', 1, 1),
    (3, 2, 'EMAIL', 'etudiant@upc.edu', 1, 1),
    (4, 2, 'PUSH', 'push_token_etudiant', 1, 1),
    (5, 3, 'EMAIL', 'moderator@upc.edu', 1, 1);

-- ==================================================
-- VUES UTILES (SQL)
-- ==================================================

-- Vue : Notifications non lues par utilisateur
CREATE VIEW IF NOT EXISTS vw_unread_notifications AS
SELECT 
    u.id as user_id,
    u.username,
    COUNT(DISTINCT un.id) as unread_count
FROM users u
LEFT JOIN user_notifications un ON u.id = un.user_id AND un.read = 0
GROUP BY u.id;

-- Vue : Statistiques des alertes
CREATE VIEW IF NOT EXISTS vw_alert_statistics AS
SELECT 
    alert_type,
    priority,
    status,
    COUNT(*) as count,
    AVG(JULIANDAY(sent_at) - JULIANDAY(created_at)) as avg_response_time_days
FROM notifications
WHERE created_at >= DATE('now', '-30 days')
GROUP BY alert_type, priority, status;

-- Vue : Activité des utilisateurs
CREATE VIEW IF NOT EXISTS vw_user_activity AS
SELECT 
    u.id,
    u.username,
    u.full_name,
    COUNT(DISTINCT n.id) as notifications_sent,
    COUNT(DISTINCT CASE WHEN un.read = 1 THEN un.id END) as notifications_read,
    u.last_login
FROM users u
LEFT JOIN notifications n ON u.id = n.created_by_id
LEFT JOIN user_notifications un ON u.id = un.user_id
GROUP BY u.id;

-- ==================================================
-- NOTES IMPORTANTES
-- ==================================================
/*
1. Les mots de passe sont hashés avec Werkzeug.security (PBKDF2-SHA256)
2. Les dates/heures sont en UTC (datetime.utcnow())
3. Chaque notification peut être envoyée à plusieurs utilisateurs via user_notifications
4. Les canaux de notification permettent multi-canal (SMS, EMAIL, PUSH)
5. Les alert_logs trackent toutes les actions pour l'audit

Comptes par défaut :
- admin / admin123
- etudiant / etu123
- moderator / mod123
*/
