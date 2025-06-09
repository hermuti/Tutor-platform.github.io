from django.urls import path
from .views import StudentDashboardView

urlpatterns = [
    path('', StudentDashboardView.as_view(), name='student_dashboard'),
]