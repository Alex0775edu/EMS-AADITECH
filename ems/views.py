from django.shortcuts import render
from django.http import HttpResponseForbidden
import logging

logger = logging.getLogger(__name__)


def csrf_failure(request, reason=""):
    """Custom CSRF failure view that logs helpful debugging information.

    This view is configured as `CSRF_FAILURE_VIEW` in settings during
    CSRF debugging. It returns a minimal 403 page while emitting request
    metadata to the configured logger so administrators can diagnose
    why a POST was rejected.
    """
    try:
        logger.warning('CSRF verification failed. reason=%s path=%s', reason, request.path)
        # Log some useful request metadata (avoid logging sensitive body in prod)
        logger.debug('CSRF request META: %s', {k: request.META.get(k) for k in ['HTTP_HOST','HTTP_ORIGIN','HTTP_REFERER','REMOTE_ADDR']})
    except Exception:
        logger.exception('Error logging CSRF failure')

    # Render a user-friendly 403 page if available
    try:
        return render(request, '403_csrf.html', status=403, context={'reason': reason})
    except Exception:
        return HttpResponseForbidden('CSRF verification failed.')
