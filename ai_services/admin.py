from django.contrib import admin

from .models import AIChatSession, AIRecommendation, AIPerformanceInsight


admin.site.register(AIChatSession)
admin.site.register(AIRecommendation)
admin.site.register(AIPerformanceInsight)
