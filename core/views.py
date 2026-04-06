import json
import urllib.request
import urllib.error
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.shortcuts import render
from django.db import IntegrityError
from students.models import Student
from teachers.models import Teacher
from .models import Institution, NewsletterSubscription


SYSTEM_PROMPT = (
    "You are AaDiTeCh, a WhatsApp-style student support assistant for an Education "
    "Management System. Help with attendance, exams, fees, notices, documents, "
    "classes, dashboards, and login/account guidance. Keep answers concise, "
    "ask clarifying questions when needed, and use the user's language (Hindi or "
    "English). Do not claim to access databases, take actions, or verify identities. "
    "If a request needs staff approval or sensitive data, advise contacting the "
    "school admin or support desk."
)

PLATFORM_FEATURE_APPS = [
    "accounts",
    "attendance",
    "billing",
    "classes",
    "communications",
    "core",
    "dashboard",
    "documents",
    "exams",
    "fees",
    "institutions",
    "materials",
    "notices",
    "notifications",
    "reports",
    "students",
    "teachers",
]


def _sanitize_history(raw_history):
    if not isinstance(raw_history, list):
        return []
    cleaned = []
    for item in raw_history[-6:]:
        if not isinstance(item, dict):
            continue
        role = item.get("role")
        content = item.get("content")
        if role in {"user", "assistant"} and isinstance(content, str) and content.strip():
            cleaned.append({"role": role, "content": content.strip()})
    return cleaned


@require_POST
def chatbot(request):
    if not settings.OPENAI_API_KEY:
        return JsonResponse(
            {"error": "OPENAI_API_KEY not configured on server."},
            status=500,
        )

    try:
        payload = json.loads(request.body.decode("utf-8"))
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON body."}, status=400)

    message = payload.get("message", "")
    if not isinstance(message, str) or not message.strip():
        return JsonResponse({"error": "Message is required."}, status=400)

    history = _sanitize_history(payload.get("history", []))

    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    messages.extend(history)
    messages.append({"role": "user", "content": message.strip()})

    request_body = json.dumps(
        {
            "model": settings.OPENAI_MODEL,
            "messages": messages,
            "temperature": 0.3,
            "max_tokens": 350,
        }
    ).encode("utf-8")

    url = f"{settings.OPENAI_API_BASE.rstrip('/')}/chat/completions"
    req = urllib.request.Request(
        url,
        data=request_body,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {settings.OPENAI_API_KEY}",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            raw = resp.read().decode("utf-8")
            data = json.loads(raw)
    except urllib.error.HTTPError as exc:
        return JsonResponse(
            {"error": "AI service error.", "details": exc.read().decode("utf-8")},
            status=502,
        )
    except Exception:
        return JsonResponse({"error": "AI service unavailable."}, status=502)

    reply = ""
    try:
        reply = data["choices"][0]["message"]["content"].strip()
    except Exception:
        reply = ""

    if not reply:
        return JsonResponse({"error": "Empty response from AI."}, status=502)

    return JsonResponse({"reply": reply})


def help_center(request):
    return render(request, "pages/help_center.html")


def documentation(request):
    return render(request, "pages/documentation.html")


def api_status(request):
    return render(request, "pages/api_status.html")


def security_page(request):
    return render(request, "pages/security.html")


def support_page(request):
    return render(request, "pages/support.html")


def about_page(request):
    context = {
        "institutes_supported": Institution.objects.count(),
        "total_students": Student.objects.count(),
        "total_teachers": Teacher.objects.count(),
        "platform_module_count": len(PLATFORM_FEATURE_APPS),
    }
    return render(request, "pages/about.html", context)


def careers_page(request):
    return render(request, "pages/careers.html")


def partners_page(request):
    return render(request, "pages/partners.html")


def privacy_page(request):
    return render(request, "pages/privacy.html")


def terms_page(request):
    return render(request, "pages/terms.html")


@require_POST
def newsletter_subscribe(request):
    email = request.POST.get("email", "").strip().lower()
    if not email or "@" not in email:
        return JsonResponse({"error": "Please enter a valid email."}, status=400)

    try:
        NewsletterSubscription.objects.create(email=email)
    except IntegrityError:
        return JsonResponse({"message": "You are already subscribed."})

    return JsonResponse({"message": "Subscription successful."})
