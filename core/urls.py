from django.urls import path
from . import views

urlpatterns = [
    path("api/chatbot/", views.chatbot, name="chatbot"),
    path("newsletter/", views.newsletter_subscribe, name="newsletter"),
    path("help-center/", views.help_center, name="help_center"),
    path("documentation/", views.documentation, name="documentation"),
    path("api-status/", views.api_status, name="api_status"),
    path("security/", views.security_page, name="security"),
    path("support/", views.support_page, name="support"),
    path("about/", views.about_page, name="about"),
    path("careers/", views.careers_page, name="careers"),
    path("partners/", views.partners_page, name="partners"),
    path("privacy/", views.privacy_page, name="privacy"),
    path("terms/", views.terms_page, name="terms"),
]
