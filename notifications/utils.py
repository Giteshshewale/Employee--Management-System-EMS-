from .models import Notification


def create_notification(user, message):
    """Create a notification for a user. Safely no-ops if user is None."""
    if user is None:
        return None
    return Notification.objects.create(user=user, message=message)
