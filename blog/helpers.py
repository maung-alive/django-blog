from dashboard.models import Action
from django.contrib.auth.models import User

def save_action(msg: str, type: str, user: User):
    Action.objects.create(
        msg=msg,
        type=type,
        user=user
    )