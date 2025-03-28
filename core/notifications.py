from django.core.mail import send_mail
from django.conf import settings

class NotificationService:
    @staticmethod
    def send_due_payment_reminder(member):
        send_mail(
            'Payment Due Reminder',
            f'Dear {member.name}, your payment of ${member.due_amount} is due.',
            settings.DEFAULT_FROM_EMAIL,
            [member.email],
            fail_silently=False,
        )

    @staticmethod
    def send_session_reminder(booking):
        # Send session reminders
        pass