from django.shortcuts import redirect
from functools import wraps

def role_required(allowed_roles=[]):
    def decorator(view_func):
        @wraps(view_func)
        def wrap(request, *args, **kwargs):
            if request.user.is_authenticated:
                if request.user.role.upper() in allowed_roles:
                    return view_func(request, *args, **kwargs)
                else:
                    return redirect('accounts:login')  # Unauthorized role
            else:
                return redirect('accounts:login')  # Not logged in
        return wrap
    return decorator
