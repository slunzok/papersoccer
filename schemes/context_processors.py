from .models import Notification, SchemeDirectory

def papersoccer_helper(request):
    if request.user.is_authenticated:
        new_notifications = Notification.objects.filter(receiver=request.user, created__gt=request.user.profile.notifications)
    else:
        new_notifications = ''

    defense_schemes = SchemeDirectory.objects.filter(parent_dir=None, scheme_access=1, scheme_type=1).order_by('name')
    attack_schemes = SchemeDirectory.objects.filter(parent_dir=None, scheme_access=1, scheme_type=2).order_by('name')
    other_schemes = SchemeDirectory.objects.filter(parent_dir=None, scheme_access=1, scheme_type=3).order_by('name')

    return {'new_notifications': new_notifications, 'defense_schemes': defense_schemes, 'attack_schemes': attack_schemes, 'other_schemes': other_schemes}
    
