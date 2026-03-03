import time
import functools
from typing import Callable, Any

def log_notification(func: Callable) -> Callable:
    """
    Décorateur pour logger l'exécution d'une fonction de notification.
    Affiche le nom de la fonction, les arguments et le résultat.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        print(f"[LOG] Notification: {func.__name__}")
        print(f"[LOG]   Args: {args}")
        print(f"[LOG]   Kwargs: {kwargs}")
        try:
            result = func(*args, **kwargs)
            print(f"[LOG]   Résultat: {result}")
            return result
        except Exception as e:
            print(f"[LOG]   Erreur: {e}")
            raise
    return wrapper

def priority(level: str):
    """
    Décorateur pour ajouter un niveau de priorité à une notification.
    Le niveau est stocké dans un attribut de la fonction.
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            print(f"[PRIORITY] Niveau: {level}")
            return func(*args, **kwargs)
        wrapper.priority_level = level  
        return wrapper
    return decorator

def retry_on_failure(max_retries: int = 3, delay: float = 1.0):
    """
    Décorateur pour réessayer une fonction en cas d'échec.
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            for attempt in range(1, max_retries + 1):
                try:
                    print(f"[RETRY] Tentative {attempt}/{max_retries}")
                    return func(*args, **kwargs)
                except Exception as e:
                    print(f"[RETRY] Échec: {e}")
                    if attempt < max_retries:
                        time.sleep(delay)
            raise Exception(f"Échec après {max_retries} tentatives")
        return wrapper
    return decorator