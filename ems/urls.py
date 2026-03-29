from django.contrib import admin
from django.urls import path, include
from dashboard.views import home, chatbot_ask
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('api/chatbot/', chatbot_ask, name='chatbot_api'),
    path('accounts/', include('accounts.urls')),
    path('', include('core.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('communications/', include('communications.urls')),
    path('billing/', include('billing.urls')),
    path('materials/', include('materials.urls')),
    path('ai/', include('ai_services.urls')),
    path('analytics/', include('analytics.urls')),
    path('students/', include('students.urls')),
    path('teachers/', include('teachers.urls')),
    path('attendance/', include('attendance.urls')),
    path('exams/', include('exams.urls')),
    path('fees/', include('fees.urls')),
    path('notices/', include('notices.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
