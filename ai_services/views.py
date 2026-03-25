from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import AIRecommendation


@login_required
def ai_insights(request):
    recommendations = AIRecommendation.objects.filter(user=request.user).order_by('-score')[:8]
    return render(request, 'ai/insights.html', {'recommendations': recommendations})
