from django.urls import path

from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('admin/', views.admin_dashboard, name='admin_dashboard'),
    path('teacher/', views.teacher_dashboard, name='teacher_dashboard'),
    path('student/', views.student_dashboard, name='student_dashboard'),
    path('students/', views.students_page, name='students_page'),
    path('teachers/', views.teachers_page, name='teachers_page'),
    path('courses/', views.courses_page, name='courses_page'),
    path('attendance/', views.attendance_page, name='attendance_page'),
    path('assignments/', views.assignments_page, name='assignments_page'),
    path('assignments/submit/<int:assignment_id>/', views.assignment_submit, name='assignment_submit'),
    path('exams/', views.exams_page, name='exams_page'),
    path('fees/', views.fees_page, name='fees_page'),
    path('notices/', views.notices_page, name='notices_page'),
    path('notifications/', views.notifications_page, name='notifications_page'),
    path('messaging/', views.messaging_page, name='messaging_page'),
    path('reports/', views.reports_page, name='reports_page'),
    path('results/', views.results_page, name='results_page'),
    path('payments/', views.payments_page, name='payments_page'),
    path('settings/', views.settings_page, name='settings_page'),
    path('settings/profile/', views.settings_update_profile, name='settings_update_profile'),
    path('settings/password/', views.settings_change_password, name='settings_change_password'),
    path('settings/mfa/', views.settings_mfa, name='settings_mfa'),
    path('settings/data-download/', views.settings_data_download, name='settings_data_download'),
    path('settings/delete-account/', views.settings_delete_account, name='settings_delete_account'),
    path('settings/consent/', views.settings_consent, name='settings_consent'),
    path('settings/notifications/', views.settings_notifications, name='settings_notifications'),
    path('settings/language/', views.settings_language, name='settings_language'),
    path('settings/accessibility/', views.settings_accessibility, name='settings_accessibility'),
    path('data-hub/', views.data_hub, name='data_hub'),
    path('search/', views.search, name='search'),
    path('chatbot/ask/', views.chatbot_ask, name='chatbot_ask'),
]
