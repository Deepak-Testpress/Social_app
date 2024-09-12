import datetime
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from .models import Action


def create_action(user, verb, target=None):
    now = timezone.now()
    last_minute = now - datetime.timedelta(seconds=60)
    user_recent_actions = Action.objects.filter(
        user_id=user.id, verb=verb, created__gte=last_minute
    )

    if target:
        target_ct = ContentType.objects.get_for_model(target)
        similar_actions = user_recent_actions.filter(
            content_type=target_ct, target_id=target.id
        )

        if not similar_actions:
            action = Action(user=user, verb=verb, target=target)
            action.save()
            return True

    return False
