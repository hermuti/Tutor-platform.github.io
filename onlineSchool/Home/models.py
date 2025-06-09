from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator, MinValueValidator
from django.utils import timezone

# === Constants ===
ROLE_CHOICES = (
    ('admin', 'Admin'),
    ('student', 'Student'),
    ('tutor', 'Tutor'),
)

GENDER_CHOICES = (
    ("Female", "Female"),
    ("Male", "Male"),
    ("Other", "Other"),
    ("Prefer not to say", "Prefer not to say")
)

SESSION_MODE_CHOICES = (
    ('online', 'Online'),
    ('in_person', 'In Person'),
    ('hybrid', 'Hybrid')
)

PAYMENT_STATUS_CHOICES = (
    ('pending', 'Pending'),
    ('completed', 'Completed'),
    ('failed', 'Failed'),
    ('refunded', 'Refunded')
)

# === Utility ===
def user_directory_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{instance.id}.{ext}"
    return f"user_{instance.id}/{filename}"

# === Core User Model ===
class User(AbstractUser):
    email = models.EmailField(unique=True)
    phone = models.CharField(
        max_length=17,
        validators=[RegexValidator(r'^\+?1?\d{9,15}$')],
        blank=True,
        null=True
    )
    gender = models.CharField(
        max_length=20,
        choices=GENDER_CHOICES,
        default="Prefer not to say"
    )
    profile_picture = models.ImageField(
        upload_to=user_directory_path,
        null=True,
        blank=True
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    status = models.CharField(
        max_length=20,
        default='active',
        choices=(
            ('active', 'Active'),
            ('inactive', 'Inactive'),
            ('suspended', 'Suspended')
        )
    )

    username = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        return f"{self.get_full_name()} ({self.role})"

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ['-date_joined']

# === Role-Specific Models ===
class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile',primary_key=True )
    grade_level = models.CharField(max_length=50)
    learning_preference = models.TextField(blank=True)
    preferred_language = models.CharField(max_length=50, default='English')

    def __str__(self):
        return f"Student: {self.user.get_full_name()}"

class Tutor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='tutor_profile',primary_key=True)
    qualifications = models.TextField()
    subjects = models.CharField(max_length=255)
    availability = models.JSONField(default=dict)
    rating = models.FloatField(default=0.0, validators=[MinValueValidator(0.0)])

    def __str__(self):
        return f"Tutor: {self.user.get_full_name()}"

class Admin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='admin_profile',primary_key=True)
    admin_level = models.CharField(
        max_length=20,
        choices=(
            ('super', 'Super Admin'),
            ('academic', 'Academic Admin'),
            ('support', 'Support Admin')
        )
    )

    def __str__(self):
        return f"Admin: {self.user.get_full_name()}"

# === Academic Models ===
class Course(models.Model):
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE, related_name='courses')
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=100)
    level = models.CharField(max_length=50)
    students = models.ManyToManyField(Student, through='Enrollment', related_name='enrolled_courses')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} (by {self.tutor})"

class Session(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='sessions')
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE, related_name='sessions')
    title = models.CharField(max_length=200)
    scheduled_time = models.DateTimeField()
    duration = models.DurationField()
    mode = models.CharField(max_length=20, choices=SESSION_MODE_CHOICES, default='online')
    video_url = models.URLField(blank=True)
    status = models.CharField(
        max_length=20,
        choices=(
            ('scheduled', 'Scheduled'),
            ('in_progress', 'In Progress'),
            ('completed', 'Completed'),
            ('cancelled', 'Cancelled')
        ),
        default='scheduled'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} at {self.scheduled_time}"

class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrolled_at = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)
    completion_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('student', 'course')

class Material(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='materials')
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE, related_name='uploaded_materials')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    file = models.FileField(upload_to='course_materials/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} (for {self.course})"

class SessionBooking(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name='bookings')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='bookings')
    booked_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=(
            ('confirmed', 'Confirmed'),
            ('cancelled', 'Cancelled'),
            ('attended', 'Attended'),
            ('no_show', 'No Show')
        ),
        default='confirmed'
    )

    class Meta:
        unique_together = ('session', 'student')

class Attendance(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name='attendance_records')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendance')
    status = models.CharField(
        max_length=20,
        choices=(
            ('present', 'Present'),
            ('absent', 'Absent'),
            ('late', 'Late')
        )
    )
    notes = models.TextField(blank=True)
    recorded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Attendance records"

# === Interaction Models ===
class Notification(models.Model):
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    notification_type = models.CharField(max_length=50)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    sent_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='sent_notifications')

    def __str__(self):
        return f"{self.notification_type} notification for {self.recipient}"

class ChatMessage(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name='chat_messages', null=True, blank=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-timestamp']

# === Career Test Models ===
class CareerTestResult(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='career_tests')
    test_date = models.DateTimeField(auto_now_add=True)
    results = models.JSONField()
    interpretation = models.TextField()
    recommendations = models.TextField(blank=True)

    def __str__(self):
        return f"Career test result for {self.student}"

# === Payment Models ===
class Payment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='payments')
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, blank=True)
    session = models.ForeignKey(Session, on_delete=models.SET_NULL, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])
    payment_method = models.CharField(max_length=50)
    transaction_id = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    timestamp = models.DateTimeField(auto_now_add=True)
    receipt_url = models.URLField(blank=True)

    def __str__(self):
        return f"Payment #{self.id} by {self.student}"

class Commission(models.Model):
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE, related_name='commissions')
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name='commissions')
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])
    is_paid = models.BooleanField(default=False)
    paid_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Commission for {self.tutor} from session #{self.session.id}"


class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Add student-specific fields
    created_at = models.DateTimeField(auto_now_add=True)

class TutorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Add tutor-specific fields
    created_at = models.DateTimeField(auto_now_add=True)