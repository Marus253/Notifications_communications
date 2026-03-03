"""
Concepts POO avancés : Descripteurs, Métaclasse, Décorateur de classe
"""

import re
from datetime import datetime

# ================== DESCRIPTEURS ==================

class PriorityDescriptor:
    """
    Descripteur pour valider les priorités
    Valide que la priorité est: LOW, MEDIUM, HIGH ou URGENT
    """
    def __init__(self):
        self.data = {}
    
    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return self.data.get(id(obj), "MEDIUM")  # Valeur par défaut
    
    def __set__(self, obj, value):
        valid_priorities = ["LOW", "MEDIUM", "HIGH", "URGENT"]
        if value not in valid_priorities:
            raise ValueError(f"Priorité invalide: {value}. Doit être: {valid_priorities}")
        self.data[id(obj)] = value

class EmailDescriptor:
    """
    Descripteur pour valider les emails
    Utilise une regex simple
    """
    def __init__(self):
        self.data = {}
    
    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return self.data.get(id(obj), "")
    
    def __set__(self, obj, value):
        if value:  # Validation seulement si valeur non vide
            pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(pattern, value):
                raise ValueError(f"Email invalide: {value}")
        self.data[id(obj)] = value

# ================== MÉTACLASSE ==================

class NotificationMeta(type):
    """
    Métaclasse pour enregistrer automatiquement les classes de notification
    """
    _registry = {}  # Dictionnaire pour stocker les classes
    
    def __new__(cls, name, bases, attrs):
        # Crée la classe normalement
        new_class = super().__new__(cls, name, bases, attrs)
        
        # Ajoute un timestamp d'enregistrement
        new_class.registered_at = datetime.now()
        
        # Enregistre la classe (sauf les classes de base)
        if not name.startswith('Base'):
            cls._registry[name] = new_class
            print(f"[MÉTACLASSE] Classe '{name}' enregistrée à {new_class.registered_at}")
        
        return new_class
    
    @classmethod
    def get_registered_classes(cls):
        """Retourne toutes les classes enregistrées"""
        return cls._registry

# ================== DÉCORATEUR DE CLASSE ==================

def track_instances(cls):
    """
    Décorateur de classe pour tracker les instances créées
    """
    original_init = cls.__init__
    
    # Compteur d'instances
    cls._instances_count = 0
    cls._instances_list = []
    
    def new_init(self, *args, **kwargs):
        # Incrémente le compteur
        cls._instances_count += 1
        cls._instances_list.append(self)
        
        # Appelle l'init original
        original_init(self, *args, **kwargs)
        
        print(f"[DÉCORATEUR] Instance {cls._instances_count} de {cls.__name__} créée")
    
    # Remplace l'init
    cls.__init__ = new_init
    
    return cls

# ================== CLASSES DE DÉMONSTRATION ==================

class BaseNotification(metaclass=NotificationMeta):
    """Classe de base utilisant la métaclasse"""
    pass

@track_instances
class UserNotification(BaseNotification):
    """
    Notification utilisateur avec descripteurs
    """
    priority = PriorityDescriptor()
    email = EmailDescriptor()
    
    def __init__(self, message, priority="MEDIUM", email=""):
        self.message = message
        self.priority = priority  # Utilise le descripteur
        if email:
            self.email = email  # Utilise le descripteur
    
    def __str__(self):
        return f"{self.priority}: {self.message} (email: {self.email})"

# ================== TEST ==================

if __name__ == "__main__":
    print("=== TEST DES CONCEPTS AVANCÉS ===\n")
    
    # Test des descripteurs
    print("1. Test des descripteurs:")
    try:
        notif = UserNotification("Test notification", priority="HIGH", email="test@campus.edu")
        print(f"   ✅ Créée: {notif}")
        
        # Test validation
        notif.priority = "URGENT"
        print(f"   ✅ Priorité changée: {notif.priority}")
        
        # Test d'erreur (devrait échouer)
        print("\n   Test d'erreur (email invalide):")
        try:
            notif.email = "mauvais-email"
        except ValueError as e:
            print(f"   ❌ Erreur attendue: {e}")
            
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
    
    # Test de la métaclasse
    print("\n2. Test de la métaclasse:")
    registry = NotificationMeta.get_registered_classes()
    print(f"   Classes enregistrées: {list(registry.keys())}")
    
    # Test du décorateur de classe
    print("\n3. Test du décorateur de classe:")
    print(f"   Instances créées: {UserNotification._instances_count}")
    
    # Créer une autre instance pour tester
    notif2 = UserNotification("Deuxième test", priority="LOW")
    print(f"   Nouvelle instance: {notif2}")
    print(f"   Total instances: {UserNotification._instances_count}")