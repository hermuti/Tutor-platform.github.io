
    # Password Management
    # path('password-reset/', views.CustomPasswordResetView.as_view(), name='password_reset'),

# from django.urls import path
# from . import views
# from .views import CustomLogoutView
# urlpatterns = [
#     path('login/', views.RoleBasedLoginView.as_view(), name='login'),
#     path('logout/', views.CustomLogoutView.as_view(), name='logout'),
#     path('register/student/', views.StudentRegisterView.as_view(), name='student_register'),
#     path('register/tutor/', views.TutorRegisterView.as_view(), name='tutor_register'),
#     path('logout/', CustomLogoutView.as_view(), name='logout'),

# ]

# from django.urls import path
# from . import views

# urlpatterns = [
#     path('login/', views.login_view, name='login'),
#     path('logout/', views.logout_view, name='logout'),
#     path('register/', views.register_view, name='register'),
#     path('student_dashboard/', views.student_dashboard, name='student_dashboard'),
#     path('tutor_dashboard/', views.tutor_dashboard, name='tutor_dashboard'),
#     path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
# ]
from django.urls import path
from .views import *
#(
#     CustomLoginView, CustomLogoutView,
#     StudentRegisterView, TutorRegisterView,
#     StudentDashboardView, TutorDashboardView, AdminDashboardView,
#     register_view, login_view, logout_view
# )

urlpatterns = [
    # Class-based views
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('register/student/', StudentRegisterView.as_view(), name='student_register'),
    path('register/tutor/', TutorRegisterView.as_view(), name='tutor_register'),
    path('student/dashboard/', StudentDashboardView.as_view(), name='student_dashboard'),
    path('tutor/dashboard/', TutorDashboardView.as_view(), name='tutor_dashboard'),
    path('admin/dashboard/', AdminDashboardView.as_view(), name='admin_dashboard'),
    
    # Function-based views (alternative)
    path('simple/register/', register_view, name='register'),
    path('simple/login/', login_view, name='simple_login'),
    path('simple/logout/', logout_view, name='simple_logout'),
]