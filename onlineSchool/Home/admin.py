from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

# === Custom User Admin ===
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('email', 'username', 'first_name', 'last_name', 'role', 'status', 'is_staff')
    list_filter = ('role', 'status', 'is_staff', 'is_superuser')
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'phone', 'gender', 'profile_picture')}),
        ('Permissions', {'fields': ('role', 'status', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'first_name', 'last_name', 'role', 'password1', 'password2'),
        }),
    )
    search_fields = ('email', 'username', 'first_name', 'last_name')
    ordering = ('-date_joined',)

# === Role-Specific Admin Classes ===
class StudentAdmin(admin.ModelAdmin):
    list_display = ('user', 'grade_level', 'preferred_language')
    search_fields = ('user__email', 'user__first_name', 'user__last_name', 'grade_level')
    raw_id_fields = ('user',)

class TutorAdmin(admin.ModelAdmin):
    list_display = ('user', 'subjects', 'rating', 'get_qualifications_preview')
    search_fields = ('user__email', 'user__first_name', 'user__last_name', 'subjects')
    list_filter = ('rating',)
    raw_id_fields = ('user',)
    
    def get_qualifications_preview(self, obj):
        return f"{obj.qualifications[:50]}..." if len(obj.qualifications) > 50 else obj.qualifications
    get_qualifications_preview.short_description = 'Qualifications Preview'

class AdminProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'admin_level')
    list_filter = ('admin_level',)
    search_fields = ('user__email', 'user__first_name', 'user__last_name')
    raw_id_fields = ('user',)

# === Academic Models Admin ===

class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'tutor', 'category', 'level', 'created_at')
    list_filter = ('category', 'level', 'created_at')
    search_fields = ('title', 'description', 'tutor__user__first_name', 'tutor__user__last_name')
    raw_id_fields = ('tutor',)
   
class SessionAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'tutor', 'scheduled_time', 'duration', 'mode', 'status')
    list_filter = ('mode', 'status', 'scheduled_time')
    search_fields = ('title', 'course__title', 'tutor__user__first_name', 'tutor__user__last_name')
    raw_id_fields = ('course', 'tutor')
    date_hierarchy = 'scheduled_time'
class EnrollmentInline(admin.TabularInline):  # or admin.StackedInline
    model = Enrollment
    extra = 1
    raw_id_fields = ('student',)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'enrolled_at', 'completed', 'completion_date')
    list_filter = ('completed', 'enrolled_at', 'course')
    search_fields = ('student__user__email', 'course__title')
    raw_id_fields = ('student', 'course')

class MaterialAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'tutor', 'created_at')
    search_fields = ('title', 'course__title', 'tutor__user__first_name')
    raw_id_fields = ('course', 'tutor')
    date_hierarchy = 'created_at'

class SessionBookingAdmin(admin.ModelAdmin):
    list_display = ('session', 'student', 'booked_at', 'status')
    list_filter = ('status', 'booked_at')
    search_fields = ('session__title', 'student__user__email')
    raw_id_fields = ('session', 'student')

class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('session', 'student', 'status', 'recorded_at')
    list_filter = ('status', 'recorded_at')
    search_fields = ('session__title', 'student__user__email')
    raw_id_fields = ('session', 'student')

# === Interaction Models Admin ===
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('recipient', 'notification_type', 'is_read', 'created_at', 'sent_by')
    list_filter = ('notification_type', 'is_read', 'created_at')
    search_fields = ('recipient__email', 'message')
    raw_id_fields = ('recipient', 'sent_by')
    date_hierarchy = 'created_at'

class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'recipient', 'session', 'timestamp', 'is_read')
    list_filter = ('is_read', 'timestamp')
    search_fields = ('sender__email', 'recipient__email', 'content')
    raw_id_fields = ('sender', 'recipient', 'session')
    date_hierarchy = 'timestamp'

# === Career Test Admin ===
class CareerTestResultAdmin(admin.ModelAdmin):
    list_display = ('student', 'test_date')
    search_fields = ('student__user__email', 'interpretation')
    raw_id_fields = ('student',)
    date_hierarchy = 'test_date'

# === Payment Models Admin ===
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('student', 'amount', 'payment_method', 'status', 'timestamp')
    list_filter = ('status', 'payment_method', 'timestamp')
    search_fields = ('student__user__email', 'transaction_id')
    raw_id_fields = ('student', 'course', 'session')
    date_hierarchy = 'timestamp'

class CommissionAdmin(admin.ModelAdmin):
    list_display = ('tutor', 'session', 'amount', 'is_paid', 'paid_at')
    list_filter = ('is_paid', 'paid_at')
    search_fields = ('tutor__user__email', 'session__title')
    raw_id_fields = ('tutor', 'session')
    date_hierarchy = 'created_at'

# === Register Models ===
admin.site.register(User, CustomUserAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Tutor, TutorAdmin)
admin.site.register(Admin, AdminProfileAdmin)

admin.site.register(Course, CourseAdmin)
admin.site.register(Session, SessionAdmin)
admin.site.register(Enrollment, EnrollmentAdmin)
admin.site.register(Material, MaterialAdmin)
admin.site.register(SessionBooking, SessionBookingAdmin)
admin.site.register(Attendance, AttendanceAdmin)

admin.site.register(Notification, NotificationAdmin)
admin.site.register(ChatMessage, ChatMessageAdmin)

admin.site.register(CareerTestResult, CareerTestResultAdmin)

admin.site.register(Payment, PaymentAdmin)
admin.site.register(Commission, CommissionAdmin)