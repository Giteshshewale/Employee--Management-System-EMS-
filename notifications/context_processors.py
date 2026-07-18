def unread_notifications(request):
    """Makes unread notification count/list available in every template."""
    if request.user.is_authenticated:
        qs = request.user.notifications.filter(is_read=False)
        return {
            'unread_notifications': qs[:5],
            'unread_notifications_count': qs.count(),
        }
    return {'unread_notifications': [], 'unread_notifications_count': 0}
