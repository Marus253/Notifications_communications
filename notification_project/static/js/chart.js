/**
 * Module de graphiques pour le dashboard
 */

class NotificationCharts {
    constructor() {
        this.charts = {};
    }
    
    /**
     * Initialise les graphiques
     */
    init() {
        this.initTypeChart();
        this.initPriorityChart();
        this.initTimelineChart();
    }
    
    /**
     * Graphique des types d'alertes
     */
    initTypeChart() {
        const ctx = document.getElementById('typeChart');
        if (!ctx) return;
        
        this.charts.type = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: ['Sécurité', 'Météo', 'Santé', 'Académique'],
                datasets: [{
                    data: [12, 19, 8, 15],
                    backgroundColor: [
                        '#e74c3c',
                        '#f39c12',
                        '#3498db',
                        '#27ae60'
                    ],
                    borderWidth: 2,
                    borderColor: '#fff'
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'bottom',
                    },
                    title: {
                        display: true,
                        text: 'Répartition par type'
                    }
                }
            }
        });
    }
    
    /**
     * Graphique des priorités
     */
    initPriorityChart() {
        const ctx = document.getElementById('priorityChart');
        if (!ctx) return;
        
        this.charts.priority = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: ['Urgent', 'Haute', 'Moyenne', 'Basse'],
                datasets: [{
                    label: 'Nombre de notifications',
                    data: [5, 12, 25, 8],
                    backgroundColor: [
                        '#e74c3c',
                        '#3498db',
                        '#f39c12',
                        '#27ae60'
                    ],
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            stepSize: 5
                        }
                    }
                },
                plugins: {
                    title: {
                        display: true,
                        text: 'Notifications par priorité'
                    }
                }
            }
        });
    }
    
    /**
     * Graphique timeline
     */
    initTimelineChart() {
        const ctx = document.getElementById('timelineChart');
        if (!ctx) return;
        
        const now = new Date();
        const labels = [];
        for (let i = 6; i >= 0; i--) {
            const date = new Date(now);
            date.setDate(date.getDate() - i);
            labels.push(date.toLocaleDateString('fr-FR', { weekday: 'short' }));
        }
        
        this.charts.timeline = new Chart(ctx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Notifications',
                    data: [4, 8, 6, 12, 9, 7, 5],
                    borderColor: '#3498db',
                    backgroundColor: 'rgba(52, 152, 219, 0.1)',
                    borderWidth: 2,
                    fill: true,
                    tension: 0.4
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    title: {
                        display: true,
                        text: 'Activité sur 7 jours'
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    }
    
    /**
     * Met à jour tous les graphiques
     */
    updateCharts(stats) {
        if (this.charts.type && stats.typeData) {
            this.charts.type.data.datasets[0].data = stats.typeData;
            this.charts.type.update();
        }
        
        if (this.charts.priority && stats.priorityData) {
            this.charts.priority.data.datasets[0].data = stats.priorityData;
            this.charts.priority.update();
        }
    }
}

// Initialisation automatique si Chart.js est chargé
document.addEventListener('DOMContentLoaded', function() {
    if (typeof Chart !== 'undefined') {
        const notificationCharts = new NotificationCharts();
        notificationCharts.init();
        window.notificationCharts = notificationCharts; // Pour accès global
    }
});