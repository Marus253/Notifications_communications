"""
Classes de base pour les différents types d'urgence
"""

class SecurityEmergencyMixin:
    def notify_security(self, message):
        return f"[SÉCURITÉ] Alerte critique : {message}"


class WeatherEmergencyMixin:
    def notify_weather(self, message):
        return f"[MÉTÉO] Alerte météo : {message}"


class HealthEmergencyMixin:
    def notify_health(self, message):
        return f"[SANTÉ] Urgence sanitaire : {message}"


class AcademicEmergencyMixin:
    def notify_academic(self, message):
        return f"[ACADÉMIQUE] Information urgente : {message}"


# Exemple de classe avec héritage multiple
class EmergencyNotifier(
    SecurityEmergencyMixin,
    WeatherEmergencyMixin,
    HealthEmergencyMixin,
    AcademicEmergencyMixin
):
    """
    Classe démonstrative de l'héritage multiple
    """
    def __init__(self, name="Notifieur"):
        self.name = name
    
    def display_mro(self):
        """Affiche le MRO (Method Resolution Order)"""
        print(f"\n=== MRO de {self.__class__.__name__} ===")
        for i, cls in enumerate(self.__class__.__mro__):
            print(f"{i}. {cls}")
        return self.__class__.__mro__
    
    def test_all(self, message):
        """Teste toutes les méthodes héritées"""
        print(f"\n=== Test des mixins pour: {message} ===")
        print(self.notify_security(message))
        print(self.notify_weather(message))
        print(self.notify_health(message))
        print(self.notify_academic(message))


# Pour tester directement
if __name__ == "__main__":
    notifier = EmergencyNotifier("Testeur")
    notifier.display_mro()
    notifier.test_all("Incident sur le campus")