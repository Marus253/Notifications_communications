// ===== VARIABLES GLOBALES =====
const API_BASE_URL = window.location.origin;

// ===== FONCTIONS UTILITAIRES =====

/**
 * Affiche une notification temporaire
 */
function showNotification(message, type = 'info') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-custom alert-dismissible fade show`;
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    const container = document.querySelector('.container') || document.body;
    container.insertBefore(alertDiv, container.firstChild);
    
    // Auto-dismiss after 5 seconds
    setTimeout(() => {
        if (alertDiv.parentElement) {
            const bsAlert = new bootstrap.Alert(alertDiv);
            bsAlert.close();
        }
    }, 5000);
}

/**
 * Formate une date
 */
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleString('fr-FR', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

/**
 * Met en majuscule la première lettre
 */
function capitalize(text) {
    return text.charAt(0).toUpperCase() + text.slice(1).toLowerCase();
}

// ===== GESTION DES FORMULAIRES =====

/**
 * Valide un formulaire d'envoi de notification
 */
function validateNotificationForm() {
    const message = document.getElementById('message');
    const alertType = document.getElementById('alert_type');
    
    if (!message.value.trim()) {
        showNotification('Veuillez entrer un message', 'danger');
        message.focus();
        return false;
    }
    
    if (!alertType.value) {
        showNotification('Veuillez sélectionner un type d\'alerte', 'danger');
        return false;
    }
    
    return true;
}

/**
 * Met à jour l'interface en fonction du type d'alerte sélectionné
 */
function updateAlertTypeUI() {
    const alertType = document.getElementById('alert_type');
    const priorityBadge = document.getElementById('priority-badge');
    const channelsInfo = document.getElementById('channels-info');
    
    if (!alertType || !priorityBadge || !channelsInfo) return;
    
    const type = alertType.value;
    const config = {
        SECURITY: {
            priority: 'URGENT',
            color: 'danger',
            channels: 'SMS, Email, Push',
            icon: '🚨'
        },
        WEATHER: {
            priority: 'MOYENNE',
            color: 'warning',
            channels: 'Email',
            icon: '🌧️'
        },
        HEALTH: {
            priority: 'HAUTE',
            color: 'info',
            channels: 'SMS, Email',
            icon: '🏥'
        },
        ACADEMIC: {
            priority: 'BASSE',
            color: 'success',
            channels: 'Email',
            icon: '📚'
        }
    };
    
    const conf = config[type] || config.SECURITY;
    
    priorityBadge.innerHTML = `
        <span class="badge bg-${conf.color}">
            ${conf.icon} Priorité: ${conf.priority}
        </span>
    `;
    
    channelsInfo.innerHTML = `
        <div class="alert alert-${conf.color}">
            <strong>Canaux utilisés :</strong> ${conf.channels}
        </div>
    `;
}

// ===== REQUÊTES API =====

/**
 * Envoie une notification via l'API
 */
async function sendNotificationAPI(alertType, message) {
    try {
        const response = await fetch(`${API_BASE_URL}/api/send`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                type: alertType,
                message: message
            })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            showNotification(`Notification envoyée: ${data.result}`, 'success');
            return data;
        } else {
            showNotification(`Erreur: ${data.error}`, 'danger');
            return null;
        }
    } catch (error) {
        showNotification(`Erreur réseau: ${error.message}`, 'danger');
        return null;
    }
}

/**
 * Récupère les statistiques
 */
async function fetchStats() {
    try {
        const response = await fetch(`${API_BASE_URL}/api/stats`);
        return await response.json();
    } catch (error) {
        console.error('Erreur lors de la récupération des stats:', error);
        return null;
    }
}

// ===== ANIMATIONS ET EFFETS =====

/**
 * Anime les statistiques au chargement
 */
function animateStats() {
    const statCards = document.querySelectorAll('.stat-card');
    statCards.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        
        setTimeout(() => {
            card.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, index * 100);
    });
}

/**
 * Ajoute un effet de pulse aux notifications importantes
 */
function addPulseToUrgentNotifications() {
    const urgentNotifications = document.querySelectorAll('.notification-security');
    urgentNotifications.forEach(notification => {
        notification.classList.add('pulse');
    });
}

// ===== INITIALISATION =====

/**
 * Initialise l'application
 */
function initApp() {
    console.log('🚀 Application initialisée');
    
    // Mise à jour de l'UI du formulaire
    const alertTypeSelect = document.getElementById('alert_type');
    if (alertTypeSelect) {
        alertTypeSelect.addEventListener('change', updateAlertTypeUI);
        updateAlertTypeUI(); // Initial call
    }
    
    // Animation des statistiques
    if (document.querySelector('.stat-card')) {
        animateStats();
    }
    
    // Effet pulse sur les notifications urgentes
    addPulseToUrgentNotifications();
    
    // Gestion du formulaire d'envoi
    const sendForm = document.getElementById('send-form');
    if (sendForm) {
        sendForm.addEventListener('submit', function(e) {
            if (!validateNotificationForm()) {
                e.preventDefault();
                return false;
            }
            
            // Ajout d'un effet de chargement
            const submitBtn = this.querySelector('button[type="submit"]');
            const originalText = submitBtn.innerHTML;
            submitBtn.innerHTML = '<span class="loading-spinner"></span> Envoi en cours...';
            submitBtn.disabled = true;
            
            // Réinitialisation après 2 secondes (simulation)
            setTimeout(() => {
                submitBtn.innerHTML = originalText;
                submitBtn.disabled = false;
            }, 2000);
        });
    }
    
    // Auto-refresh du dashboard toutes les 30 secondes
    if (window.location.pathname.includes('/dashboard')) {
        setInterval(() => {
            console.log('🔄 Actualisation automatique du dashboard');
            // Ici tu pourrais recharger les données
        }, 30000);
    }
}

// ===== ÉVÉNEMENTS =====

// Initialisation quand le DOM est chargé
document.addEventListener('DOMContentLoaded', initApp);

// Gestion des tooltips Bootstrap
document.addEventListener('DOMContentLoaded', function() {
    const tooltips = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    tooltips.forEach(tooltip => new bootstrap.Tooltip(tooltip));
});

// Gestion des popovers Bootstrap
document.addEventListener('DOMContentLoaded', function() {
    const popovers = document.querySelectorAll('[data-bs-toggle="popover"]');
    popovers.forEach(popover => new bootstrap.Popover(popover));
});