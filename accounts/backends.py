from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q


class IdentifierBackend(ModelBackend):
    """Authenticate using username, email, or institute ID."""

    def authenticate(self, request, username=None, password=None, **kwargs):
        identifier = (username or kwargs.get('identifier') or kwargs.get('email') or '').strip()
        if not identifier or password is None:
            return None

        UserModel = get_user_model()
        candidates = UserModel._default_manager.filter(
            Q(username__iexact=identifier)
            | Q(email__iexact=identifier)
            | Q(institute_id__iexact=identifier)
        )

        for user in candidates:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
        return None
