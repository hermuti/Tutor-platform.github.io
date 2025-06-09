from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import redirect

class TutorDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'tutor_dashboard/dashboard.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_tutor:
            messages.error(request, "Tutor access required")
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)