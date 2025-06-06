from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Profile, Teacher, Student, Course, CourseCategory

# Unregister default User admin if needed
# admin.site.unregister(User)

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'

class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline,)
    list_display = ('username', 'email', 'role', 'is_staff')
    list_select_related = ('profile',)
    
    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super().get_inline_instances(request, obj)

class TeacherAdmin(admin.ModelAdmin):
    list_display = ('user', 'qualification')
    raw_id_fields = ('user',)
    
    def save_model(self, request, obj, form, change):
        # Automatically set user role to teacher
        obj.user.role = 'tutor'
        obj.user.save()
        super().save_model(request, obj, form, change)

class StudentAdmin(admin.ModelAdmin):
    list_display = ('user', 'grade_level')
    raw_id_fields = ('user',)
    
    def save_model(self, request, obj, form, change):
        # Automatically set user role to student
        obj.user.role = 'student'
        obj.user.save()
        super().save_model(request, obj, form, change)

# Register your models
admin.site.register(User, CustomUserAdmin)
admin.site.register(Profile)
admin.site.register(Teacher, TeacherAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Course)
admin.site.register(CourseCategory)