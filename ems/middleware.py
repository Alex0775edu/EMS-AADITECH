from django.conf import settings
from django.core.cache import cache
from django.http import JsonResponse


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
