from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from .models import User, Student, Tutor

class StudentRegisterForm(UserCreationForm):
    grade_level = forms.CharField(max_length=50, required=True)
    
    class Meta:
        model = User
        fields = ['email', 'username', 'password1', 'password2', 'grade_level']

class TutorRegisterForm(UserCreationForm):
    qualifications = forms.CharField(widget=forms.Textarea)
    subjects = forms.CharField(max_length=255)
    
    class Meta:
        model = User
        fields = ['email', 'username', 'password1', 'password2', 'qualifications', 'subjects']



class EmailAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={'autofocus': True}))
