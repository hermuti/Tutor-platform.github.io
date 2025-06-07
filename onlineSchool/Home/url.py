from django.urls import path
from .views import TeacherList, TeacherDetail, TeacherStats

urlpatterns = [
    path('teachers/', TeacherList.as_view(), name='teacher-list'),
    path('teachers/<int:pk>/', TeacherDetail.as_view(), name='teacher-detail'),
    path('teachers/stats/', TeacherStats.as_view(), name='teacher-stats'),
]