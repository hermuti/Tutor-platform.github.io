from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import redirect

class StudentDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'student_dashboard/dashboard.html'  # Path to your template

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_student:
            messages.error(request, "You don't have permission to access this page.")
            return redirect('login')  # Redirect non-students to login
        return super().dispatch(request, *args, **kwargs)