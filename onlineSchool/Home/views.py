from django.views.generic import TemplateView, CreateView
from django.contrib.auth.views import LoginView, LogoutView
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import StudentRegisterForm, TutorRegisterForm
from Home.forms import EmailAuthenticationForm  
from django.contrib.auth import get_user_model
from .models import User, StudentProfile, TutorProfile  # Updated imports

User = get_user_model()

# ====================== Authentication Views ======================

from django.urls import reverse_lazy

class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    authentication_form = EmailAuthenticationForm
    redirect_authenticated_user = True
    
    # Add this to completely override default behavior
    def get_success_url(self):
        role = self.request.POST.get('role')
        return self._get_redirect_url(role)
    
    def _get_redirect_url(self, role):
        if role == 'student':
            return reverse_lazy('student_dashboard')
        elif role == 'tutor':
            return reverse_lazy('tutor_dashboard')
        elif role == 'admin':
            return reverse_lazy('admin_dashboard')
        return reverse_lazy('home')  # Fallback URL
    
    def form_valid(self, form):
        role = self.request.POST.get('role')
        user = form.get_user()
        
        if not role:
            messages.error(self.request, "Please select a role")
            return self.form_invalid(form)
            
        login(self.request, user)
        return super().form_valid(form)  # Will use get_success_url
class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('home')
    
    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        messages.success(request, "You have been successfully logged out.")
        return response

# ====================== Registration Views ======================
def register_view(request):
    if request.method == 'POST':
        # Get form data
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        role = request.POST.get('role')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')

        # Validate required fields
        if not all([username, email, password1, password2, role, first_name, last_name]):
            messages.error(request, "All fields are required.")
            return render(request, 'accounts/register.html', {
                'username': username,
                'email': email,
                'first_name': first_name,
                'last_name': last_name,
                'role': role
            })

        if password1 != password2:
            messages.error(request, "Passwords don't match.")
            return render(request, 'accounts/register.html', {
                'username': username,
                'email': email,
                'first_name': first_name,
                'last_name': last_name,
                'role': role
            })

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return render(request, 'accounts/register.html', {
                'email': email,
                'first_name': first_name,
                'last_name': last_name,
                'role': role
            })

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return render(request, 'accounts/register.html', {
                'username': username,
                'first_name': first_name,
                'last_name': last_name,
                'role': role
            })

        try:
            # Create user with all required fields
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password1,
                first_name=first_name,
                last_name=last_name,
                role=role
            )
            
            # Set role flags and create profile
            if role == 'student':
                user.is_student = True
                StudentProfile.objects.create(user=user)
            elif role == 'tutor':
                user.is_tutor = True
                TutorProfile.objects.create(user=user)
            elif role == 'admin':
                user.is_admin = True
            
            user.save()
            
            messages.success(request, "Registration successful! Please login.")
            return redirect('login')
            
        except Exception as e:
            messages.error(request, f"Error during registration: {str(e)}")
            return render(request, 'accounts/register.html', {
                'username': username,
                'email': email,
                'first_name': first_name,
                'last_name': last_name,
                'role': role
            })
    
    return render(request, 'accounts/register.html')

# ====================== Dashboard Views ======================
class StudentDashboardView(TemplateView):
    template_name = 'dashboard/student_dashboard.html'
    
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_student:
            messages.error(request, "You don't have permission to access this page.")
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)

class TutorDashboardView(TemplateView):
    template_name = 'dashboard/tutor_dashboard.html'
    
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_tutor:
            messages.error(request, "You don't have permission to access this page.")
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)

class AdminDashboardView(TemplateView):
    template_name = 'dashboard/admin_dashboard.html'
    
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_admin:
            messages.error(request, "You don't have permission to access this page.")
            return redirect('login')
        return super().dispatch(request, *args, **kwargs)