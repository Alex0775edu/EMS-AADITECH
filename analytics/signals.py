from django.contrib.auth.signals import user_logged_in, user_login_failed
from django.dispatch import receiver

from .utils import log_event, _safe_str


@receiver(user_logged_in)
def handle_user_logged_in(sender, request, user, **kwargs):
    if not request:
        return
    metadata = {
        'path': request.path[:255],
        'user_agent': _safe_str(request.META.get('HTTP_USER_AGENT')),
    }
    log_event(request, 'login', metadata=metadata, user=user)


@receiver(user_login_failed)
def handle_user_login_failed(sender, credentials, request, **kwargs):
    if not request:
        return
    identifier = credentials.get('username') or credentials.get('email') or credentials.get('identifier') or ''
    metadata = {
        'path': request.path[:255],
        'identifier': _safe_str(identifier, 120),
        'user_agent': _safe_str(request.META.get('HTTP_USER_AGENT')),
    }
    log_event(request, 'login_failed', metadata=metadata, user=None)
