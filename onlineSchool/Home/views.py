from django.views.generic import TemplateView, CreateView
from django.contrib.auth.views import LoginView, LogoutView
from django.utils.decorators import method_decorator  # Add this import
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import StudentRegisterForm, TutorRegisterForm

# ====================== Authentication Views ======================
class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    
    def form_valid(self, form):
        role = self.request.POST.get('role')
        user = form.get_user()
        
        if not self._validate_user_role(user, role):
            messages.error(self.request, "Invalid role for this user")
            return redirect('login')
        
        login(self.request, user)
        return self._redirect_based_on_role(role)
    
    def _validate_user_role(self, user, role):
        # Implement your actual role validation logic here
        # Example: return user.profile.role == role
        return True  # Placeholder
    
    def _redirect_based_on_role(self, role):
        if role == 'student':
            return redirect('student_dashboard')
        elif role == 'tutor':
            return redirect('tutor_dashboard')
        elif role == 'admin':
            return redirect('/admin/')
        return redirect('home')

class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('login')
    
    def dispatch(self, request, *args, **kwargs):
        messages.success(request, "Logged out successfully.")
        return super().dispatch(request, *args, **kwargs)

# ====================== Registration Views ======================
class StudentRegisterView(CreateView):
    form_class = StudentRegisterForm
    template_name = 'accounts/student_register.html'
    success_url = reverse_lazy('student_dashboard')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.instance
        login(self.request, user)
        # Create student profile here if needed
        return response

class TutorRegisterView(CreateView):
    form_class = TutorRegisterForm
    template_name = 'accounts/tutor_register.html'
    success_url = reverse_lazy('tutor_dashboard')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.instance
        login(self.request, user)
        # Create tutor profile here if needed
        return response

# ====================== Dashboard Views ======================
class StudentDashboardView(TemplateView):
    template_name = 'dashboard/student_dashboard.html'
    
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        # Add role verification if needed
        return super().dispatch(request, *args, **kwargs)

class TutorDashboardView(TemplateView):
    template_name = 'dashboard/tutor_dashboard.html'
    
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        # Add role verification if needed
        return super().dispatch(request, *args, **kwargs)

class AdminDashboardView(TemplateView):
    template_name = 'dashboard/admin_dashboard.html'
    
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        # Add admin verification
        return super().dispatch(request, *args, **kwargs)

# ====================== Function-Based Views ======================
def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        role = request.POST.get('role')

        if password1 != password2:
            messages.error(request, "Passwords don't match.")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('register')

        user = User.objects.create_user(username=username, email=email, password=password1)
        
        # Here you would typically create a profile based on the role
        # Example: StudentProfile.objects.create(user=user, role=role)
        
        messages.success(request, "Registration successful. Please login.")
        return redirect('login')
    
    return render(request, 'accounts/register.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        role = request.POST.get('role')

        user = authenticate(request, username=username, password=password)
        
        # You need to implement role validation here
        # Example: if user is not None and user.profile.role == role:
        if user is not None:
            login(request, user)
            if role == 'student':
                return redirect('student_dashboard')
            elif role == 'tutor':
                return redirect('tutor_dashboard')
            elif role == 'admin':
                return redirect('/admin/')
        else:
            messages.error(request, "Invalid credentials or role.")
            return redirect('login')
    
    return render(request, 'accounts/login.html')

def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect('login')