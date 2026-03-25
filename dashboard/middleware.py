from django.contrib.auth import get_user_model
from django.db import IntegrityError

from .models import ActivityLog


class ActivityLogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if request.user.is_authenticated and not request.path.startswith('/static/'):
            user = self._safe_user(request)
            try:
                ActivityLog.objects.create(
                    user=user,
                    action='Page access',
                    path=request.path[:255],
                    method=request.method,
                    ip_address=self._get_client_ip(request),
                )
            except IntegrityError:
                # Prevent request failure if user/session FK is stale.
                ActivityLog.objects.create(
                    user=None,
                    action='Page access',
                    path=request.path[:255],
                    method=request.method,
                    ip_address=self._get_client_ip(request),
                )

        return response

    @staticmethod
    def _get_client_ip(request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0].strip()
        return request.META.get('REMOTE_ADDR')

    @staticmethod
    def _safe_user(request):
        if not request.user.is_authenticated:
            return None
        User = get_user_model()
        if User.objects.filter(pk=request.user.pk).exists():
            return request.user
        return None
