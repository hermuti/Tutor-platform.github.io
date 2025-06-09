from django.urls import path
from .views import *
# (
#     register_view,
#     CustomLoginView,
#     CustomLogoutView,
#     StudentDashboardView,
#     TutorDashboardView,
#     AdminDashboardView
# )

urlpatterns = [
    # Authentication
    path('accounts/register/', register_view, name='register'),
    path('accounts/login/', CustomLoginView.as_view(), name='login'),
    path('accounts/logout/', CustomLogoutView.as_view(), name='logout'),
    
    # Dashboards
    path('dashboard/student/', StudentDashboardView.as_view(), name='student_dashboard'),
    path('dashboard/tutor/', TutorDashboardView.as_view(), name='tutor_dashboard'),
    path('dashboard/admin/', AdminDashboardView.as_view(), name='admin_dashboard'),
]

# login dashboard view
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

class StudentDashboardView(TemplateView):
    template_name = 'dashboard/student_dashboard.html'
    
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_student:
            messages.error(request, "You don't have student access")
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)

class TutorDashboardView(TemplateView):
    template_name = 'dashboard/tutor_dashboard.html'
    
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_tutor:
            messages.error(request, "You don't have tutor access")
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)

class AdminDashboardView(TemplateView):
    template_name = 'dashboard/admin_dashboard.html'
    
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_admin:
            messages.error(request, "You don't have admin access")
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)
