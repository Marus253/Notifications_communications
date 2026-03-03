"""
Mixins pour les différents canaux de communication
"""

class SMSMixin:
    """
    Mixin responsable de l'envoi de notifications par SMS
    """
    def send_sms(self, message):
        print(f"[SMS] Notification envoyée : {message}")


class EmailMixin:
    """
    Mixin responsable de l'envoi de notifications par Email
    """
    def send_email(self, message):
        print(f"[EMAIL] Notification envoyée : {message}")


class PushMixin:
    """
    Mixin responsable de l'envoi de notifications Push
    """
    def send_push(self, message):
        print(f"[PUSH] Notification envoyée : {message}")