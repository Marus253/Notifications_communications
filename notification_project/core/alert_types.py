"""
Classes d'alerte qui utilisent TES mixins SMS/Email/Push
"""

from core.mixins import SMSMixin, EmailMixin, PushMixin
from core.decorators import log_notification, priority
from core.notifiers import (
    SecurityEmergencyMixin, 
    WeatherEmergencyMixin,
    HealthEmergencyMixin, 
    AcademicEmergencyMixin
)

class BaseAlert:
    """Classe de base pour toutes les alertes"""
    def __init__(self, message):
        self.message = message
        self.sent = False
    
    def get_formatted_message(self):
        return f"[{self.__class__.__name__}] {self.message}"

# ========== ALERTE SÉCURITÉ ==========
class SecurityAlert(
    BaseAlert,
    SecurityEmergencyMixin,
    SMSMixin, EmailMixin, PushMixin  # TES mixins
):
    """
    Alerte de sécurité - Priorité URGENT
    Utilise tous les canaux (SMS, Email, Push)
    """
    def __init__(self, message):
        super().__init__(message)
        self.priority = "URGENT"
    
    @log_notification
    @priority("URGENT")
    def send(self):
        """Envoie l'alerte sur tous les canaux"""
        msg = self.get_formatted_message()
        print(f"🚨 Envoi alerte SÉCURITÉ ({self.priority}): {self.message}")
        
        # Utilise TES mixins
        self.send_sms(f"[URGENT] {self.message}")
        self.send_email(f"Alerte Sécurité: {self.message}")
        self.send_push(f"🚨 {self.message}")
        
        self.sent = True
        return f"Alerte sécurité envoyée sur 3 canaux"

# ========== ALERTE MÉTÉO ==========
class WeatherAlert(
    BaseAlert,
    WeatherEmergencyMixin,
    EmailMixin  # Seulement Email
):
    """
    Alerte météo - Priorité MOYENNE
    Utilise seulement Email
    """
    def __init__(self, message):
        super().__init__(message)
        self.priority = "MEDIUM"
    
    @log_notification
    @priority("MEDIUM")
    def send(self):
        """Envoie l'alerte par email seulement"""
        msg = self.get_formatted_message()
        print(f"🌧️ Envoi alerte MÉTÉO ({self.priority}): {self.message}")
        
        # Utilise TES mixins
        self.send_email(f"Alerte Météo: {self.message}")
        
        self.sent = True
        return f"Alerte météo envoyée par email"

# ========== ALERTE SANTÉ ==========
class HealthAlert(
    BaseAlert,
    HealthEmergencyMixin,
    SMSMixin, EmailMixin  # SMS et Email
):
    """
    Alerte santé - Priorité HAUTE
    Utilise SMS et Email
    """
    def __init__(self, message):
        super().__init__(message)
        self.priority = "HIGH"
    
    @log_notification
    @priority("HIGH")
    def send(self):
        """Envoie l'alerte par SMS et Email"""
        msg = self.get_formatted_message()
        print(f"🏥 Envoi alerte SANTÉ ({self.priority}): {self.message}")
        
        # Utilise TES mixins
        self.send_sms(f"[SANTÉ] {self.message}")
        self.send_email(f"Alerte Santé: {self.message}")
        
        self.sent = True
        return f"Alerte santé envoyée par SMS et email"

# ========== ALERTE ACADÉMIQUE ==========
class AcademicAlert(
    BaseAlert,
    AcademicEmergencyMixin,
    EmailMixin  # Seulement Email
):
    """
    Alerte académique - Priorité BASSE
    Utilise seulement Email
    """
    def __init__(self, message):
        super().__init__(message)
        self.priority = "LOW"
    
    @log_notification
    @priority("LOW")
    def send(self):
        """Envoie l'alerte par email seulement"""
        msg = self.get_formatted_message()
        print(f"📚 Envoi alerte ACADÉMIQUE ({self.priority}): {self.message}")
        
        # Utilise TES mixins
        self.send_email(f"Info Académique: {self.message}")
        
        self.sent = True
        return f"Alerte académique envoyée par email"

# ========== TEST ==========
if __name__ == "__main__":
    print("=== TEST DES ALERTES ===")
    
    # Test alerte sécurité
    print("\n1. Test Alerte Sécurité:")
    security = SecurityAlert("Intrusion bâtiment A")
    print(f"   Priorité: {security.priority}")
    print(f"   MRO: {SecurityAlert.__mro__}")
    security.send()
    
    # Test alerte météo
    print("\n2. Test Alerte Météo:")
    weather = WeatherAlert("Pluies intenses prévues")
    print(f"   Priorité: {weather.priority}")
    weather.send()
    
    # Test alerte santé
    print("\n3. Test Alerte Santé:")
    health = HealthAlert("Cas COVID détecté")
    print(f"   Priorité: {health.priority}")
    health.send()
    
    # Test alerte académique
    print("\n4. Test Alerte Académique:")
    academic = AcademicAlert("Réunion reportée")
    print(f"   Priorité: {academic.priority}")
    academic.send()