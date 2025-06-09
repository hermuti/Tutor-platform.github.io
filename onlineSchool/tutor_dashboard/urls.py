from django.urls import path
from .views import TutorDashboardView

urlpatterns = [
    path('', TutorDashboardView.as_view(), name='tutor_dashboard'),
]