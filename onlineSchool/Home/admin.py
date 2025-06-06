from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from .models import User, Profile, Teacher, Student, CourseCategory, Course

# ==================== INLINES ====================
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fields = ('mobile_no', 'country', 'city', 'state', 'address', 
              'identity_type', 'identity_image', 'facebook', 'twitter', 'wallet', 'verified')
    
class TeacherInline(admin.StackedInline):
    model = Teacher
    can_delete = False
    verbose_name_plural = 'Teacher Details'
    fields = ('qualification', 'bio', 'specialties', 'experience_years', 'hourly_rate', 'is_approved')

class StudentInline(admin.StackedInline):
    model = Student
    can_delete = False
    verbose_name_plural = 'Student Details'
    fields = ('grade_level', 'school', 'learning_goals', 'parent_guardian_name', 'parent_guardian_contact')

# ==================== MODEL ADMINS ====================
class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline, TeacherInline, StudentInline)
    list_display = ('username', 'email', 'full_name', 'role', 'status', 'is_active', 'last_login')
    list_filter = ('role', 'status', 'is_active', 'is_staff', 'is_superuser')
    search_fields = ('username', 'email', 'full_name', 'phone')
    ordering = ('-date_joined',)
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('full_name', 'email', 'phone', 'gender')}),
        ('Permissions', {'fields': ('role', 'status', 'is_active', 'is_staff', 'is_superuser', 
                                  'groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'full_name', 'phone', 'role', 'password1', 'password2'),
        }),
    )

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return []
        if obj.role == 'tutor':
            return [TeacherInline(self.model, self.admin_site)]
        elif obj.role == 'student':
            return [StudentInline(self.model, self.admin_site)]
        return []

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'mobile_no', 'country', 'verified', 'wallet_balance')
    list_filter = ('verified', 'country')
    search_fields = ('user__username', 'user__email', 'mobile_no')
    
    def wallet_balance(self, obj):
        return f"${obj.wallet:,.2f}"
    wallet_balance.short_description = 'Balance'

class TeacherAdmin(admin.ModelAdmin):
    list_display = ('user', 'qualification', 'experience', 'hourly_rate', 'is_approved')
    list_filter = ('is_approved', 'experience_years')
    search_fields = ('user__username', 'user__email', 'qualification', 'specialties')
    raw_id_fields = ('user',)
    actions = ['approve_teachers', 'disapprove_teachers']

    def experience(self, obj):
        return f"{obj.experience_years} years"
    experience.short_description = 'Experience'

    def approve_teachers(self, request, queryset):
        queryset.update(is_approved=True)
    approve_teachers.short_description = "Approve selected teachers"

    def disapprove_teachers(self, request, queryset):
        queryset.update(is_approved=False)
    disapprove_teachers.short_description = "Disapprove selected teachers"

class StudentAdmin(admin.ModelAdmin):
    list_display = ('user', 'grade_level', 'school', 'parent_contact')
    list_filter = ('grade_level',)
    search_fields = ('user__username', 'user__email', 'grade_level', 'school')
    raw_id_fields = ('user',)

    def parent_contact(self, obj):
        if obj.parent_guardian_contact:
            return obj.parent_guardian_contact
        return "Not provided"
    parent_contact.short_description = 'Parent Contact'

class CourseCategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'course_count', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('title', 'description')

    def course_count(self, obj):
        return obj.courses.count()
    course_count.short_description = 'Courses'

class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'teacher', 'price', 'status', 'duration')
    list_filter = ('status', 'category', 'is_featured')
    search_fields = ('title', 'description', 'teacher__user__username')
    raw_id_fields = ('teacher',)
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('title', 'category', 'teacher', 'description')
        }),
        ('Details', {
            'fields': ('syllabus', 'duration_weeks', 'price', 'is_featured')
        }),
        ('Status', {
            'fields': ('status', 'created_at', 'updated_at')
        }),
    )

    def duration(self, obj):
        return f"{obj.duration_weeks} weeks"
    duration.short_description = 'Duration'

# ==================== REGISTRATIONS ====================
admin.site.register(User, CustomUserAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Teacher, TeacherAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(CourseCategory, CourseCategoryAdmin)
admin.site.register(Course, CourseAdmin)

# ==================== ADMIN CONFIG ====================
admin.site.site_header = "Tutor Platform Administration"
admin.site.site_title = "Tutor Platform Admin Portal"
admin.site.index_title = "Welcome to Tutor Platform Admin"