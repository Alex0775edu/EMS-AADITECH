from django.conf import settings
from django.core.cache import cache
from django.http import JsonResponse
from django.middleware.csrf import get_token


class EnsureCsrfCookieMiddleware:
    """Ensure a CSRF cookie is present for browsers and JS fetch calls.

    Some clients (SPA or AJAX) rely on a cookie or meta tag being present
    before making unsafe requests. This middleware calls Django's
    `get_token` to generate a token and sets the CSRF cookie on the
    response for safe (GET/HEAD/OPTIONS) requests if missing.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Ensure a token exists on the request (may create one)
        try:
            token = get_token(request)
        except Exception:
            token = None

        response = self.get_response(request)

        # Only set cookie for idempotent requests where it helps clients
        if request.method in ('GET', 'HEAD', 'OPTIONS') and token:
            cookie_name = getattr(settings, 'CSRF_COOKIE_NAME', 'csrftoken')
            if cookie_name not in request.COOKIES and cookie_name not in response.cookies:
                response.set_cookie(
                    cookie_name,
                    token,
                    max_age=getattr(settings, 'CSRF_COOKIE_AGE', None),
                    domain=getattr(settings, 'CSRF_COOKIE_DOMAIN', None),
                    secure=getattr(settings, 'CSRF_COOKIE_SECURE', False),
                    httponly=getattr(settings, 'CSRF_COOKIE_HTTPONLY', False),
                    samesite=getattr(settings, 'CSRF_COOKIE_SAMESITE', 'Lax'),
                )

        return response


class RateLimitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.window = getattr(settings, 'RATE_LIMIT_WINDOW', 60)
        self.limit = getattr(settings, 'RATE_LIMIT_REQUESTS', 120)

    def __call__(self, request):
        ip = self._get_ip(request)
        key = f"rl:{ip}:{request.path}"
        count = cache.get(key, 0)
        if count >= self.limit:
            return JsonResponse({'detail': 'Too many requests. Please slow down.'}, status=429)
        cache.set(key, count + 1, timeout=self.window)
        return self.get_response(request)

    @staticmethod
    def _get_ip(request):
        forwarded = request.META.get('HTTP_X_FORWARDED_FOR')
        if forwarded:
            return forwarded.split(',')[0].strip()
        return request.META.get('REMOTE_ADDR', 'unknown')
