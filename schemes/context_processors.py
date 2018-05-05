from .models import Notification

def papersoccer_helper(request):
    if request.user.is_authenticated:
        new_notifications = Notification.objects.filter(receiver=request.user, created__gt=request.user.profile.notifications)
    else:
        new_notifications = ''

    return {'new_notifications': new_notifications}
    
