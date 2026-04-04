from .utils import log_event, _safe_str


class PageViewTrackingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if request.method != 'GET':
            return response

        path = request.path or '/'
        if _is_excluded_path(path):
            return response

        content_type = response.get('Content-Type', '')
        if 'text/html' not in content_type:
            return response

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return response

        metadata = {
            'path': path[:255],
            'method': request.method,
            'referrer': _safe_str(request.META.get('HTTP_REFERER')),
            'user_agent': _safe_str(request.META.get('HTTP_USER_AGENT')),
            'host': _safe_str(request.get_host()),
        }
        log_event(request, 'page_view', metadata=metadata)
        return response


def _is_excluded_path(path):
    excluded_prefixes = (
        '/static/',
        '/media/',
        '/admin/',
        '/favicon.ico',
        '/robots.txt',
        '/sitemap.xml',
    )
    return any(path.startswith(prefix) for prefix in excluded_prefixes)
