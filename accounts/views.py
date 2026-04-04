from datetime import datetime
import logging

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import redirect, render
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import ensure_csrf_cookie

from .forms import RegisterForm
from .models import User

logger = logging.getLogger(__name__)


@never_cache
@ensure_csrf_cookie
def custom_login(request):
    if request.method == 'POST':
        identifier = request.POST.get('identifier', '').strip()
        password = request.POST.get('password', '')
        remember = request.POST.get('remember')
        next_url = request.POST.get('next') or request.GET.get('next')

        user = authenticate(request, username=identifier, password=password)
        if not user and identifier:
            candidates = User.objects.filter(
                Q(email__iexact=identifier)
                | Q(institute_id__iexact=identifier)
                | Q(username__iexact=identifier)
            )
            for candidate in candidates:
                authed = authenticate(request, username=candidate.username, password=password)
                if authed:
                    user = authed
                    break

        if user:
            login(request, user)
            if not remember:
                request.session.set_expiry(0)

            # Prefer a safe next URL if provided
            if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
                return redirect(next_url)

            if user.role == 'ADMIN':
                return redirect('dashboard:admin_dashboard')
            if user.role == 'TEACHER':
                return redirect('dashboard:teacher_dashboard')
            if user.role == 'STUDENT':
                return redirect('dashboard:student_dashboard')
            return redirect('dashboard:dashboard')

        # log failed attempt without sensitive data
        logger.debug('Failed login attempt for identifier=%s from %s', identifier, request.META.get('REMOTE_ADDR'))

        return render(
            request,
            'auth/login.html',
            {'error': 'Invalid Institute ID/Email or password.', 'identifier': identifier, 'next': next_url},
        )

    return render(request, 'auth/login.html', {'next': request.GET.get('next', '')})


@login_required
@never_cache
@ensure_csrf_cookie
def custom_register(request):
    if not (request.user.is_superuser or request.user.role == 'ADMIN'):
        messages.error(request, 'Only admin or superuser can create users.')
        return redirect('dashboard:dashboard')

    if request.method == 'POST':
        form = RegisterForm(request.POST, current_user=request.user)
        if form.is_valid():
            user = form.save()
            messages.success(
                request,
                (
                    f'User created successfully. Default password is DOB (DDMMYYYY): '
                    f'{user.default_password_from_dob() or "not available"}'
                ),
            )
            return redirect('accounts:register')
    else:
        form = RegisterForm(current_user=request.user)

    return render(request, 'auth/register.html', {'form': form})


def custom_logout(request):
    # Allow logout to be called even when not authenticated
    try:
        logout(request)
    except Exception:
        logger.exception('Error during logout')
    return redirect('accounts:login')


@never_cache
@ensure_csrf_cookie
def forgot_password(request):
    context = {}
    if request.method == 'POST':
        identifier = request.POST.get('identifier', '').strip()
        dob_str = request.POST.get('date_of_birth', '').strip()
        new_password = request.POST.get('new_password', '')
        confirm_password = request.POST.get('confirm_password', '')

        if new_password != confirm_password:
            context['error'] = 'Passwords do not match.'
            return render(request, 'auth/forgot_password.html', context)

        try:
            dob = datetime.strptime(dob_str, '%Y-%m-%d').date()
        except ValueError:
            context['error'] = 'Enter a valid date of birth.'
            return render(request, 'auth/forgot_password.html', context)

        user = User.objects.filter(Q(email__iexact=identifier) | Q(institute_id__iexact=identifier)).first()
        if not user or not user.date_of_birth or user.date_of_birth != dob:
            context['error'] = 'User details did not match.'
            return render(request, 'auth/forgot_password.html', context)

        user.set_password(new_password)
        user.save(update_fields=['password'])
        context['success_message'] = 'Password reset successful. You can login now.'

    return render(request, 'auth/forgot_password.html', context)
