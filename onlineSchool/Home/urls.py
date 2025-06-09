from django.urls import path,include
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
    path('student/', include('student_dashboard.urls')),
    path('tutor/', include('tutor_dashboard.urls')),
    #path('admin/', include('admin_dashboard.urls')),
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
