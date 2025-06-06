from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.utils import timezone
from shortuuid.django_fields import ShortUUIDField
import logging

logger = logging.getLogger(__name__)

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

IDENTITY_TYPE = (
    ("Fayda Alias Number (FAN)", "Fayda Alias Number (FAN)"),
    ("Driver's license", "Driver's license"),
    ("International passport", "International passport")
)

STATUS_CHOICES = (
    ('active', 'Active'),
    ('inactive', 'Inactive'),
    ('suspended', 'Suspended'),
    ('pending', 'Pending Verification'),
)

# Phone number validator
phone_validator = RegexValidator(
    regex=r'^\+?1?\d{9,15}$',
    message="Phone number must be in format: '+999999999'. Up to 15 digits allowed."
)

# === Utility ===
def user_directory_path(instance, filename):
    ext = filename.split(".")[-1]
    filename = "%s.%s" % (instance.user.id, ext)
    return "user_{0}/{1}".format(instance.user.id, filename)

# === Custom User Model ===
class User(AbstractUser):
    full_name = models.CharField(
        max_length=100,
        verbose_name="Full Name",
        help_text="Enter user's full legal name"
    )
    username = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Username",
        help_text="Required. 100 characters or fewer. Letters, digits and @/./+/-/_ only."
    )
    email = models.EmailField(
        unique=True,
        verbose_name="Email Address",
        help_text="Required. Must be a valid email address."
    )
    phone = models.CharField(
        max_length=17,
        validators=[phone_validator],
        verbose_name="Phone Number",
        help_text="Format: +999999999",
        blank=True,
        null=True
    )
    gender = models.CharField(
        max_length=20,
        choices=GENDER_CHOICES,
        default="Prefer not to say",
        verbose_name="Gender"
    )
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default="student",
        verbose_name="System Role"
    )
    otp = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name="OTP Code"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name="Account Status"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'full_name']

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

    def is_teacher(self):
        return self.role == 'tutor' and hasattr(self, 'teacher_profile')

    def is_student(self):
        return self.role == 'student' and hasattr(self, 'student_profile')

# === Profile Model ===
class Profile(models.Model):
    pid = ShortUUIDField(
        length=7,
        max_length=25,
        alphabet="abcdefghijklmnopqrstuvwxyz12345",
        unique=True,
        verbose_name="Profile ID"
    )
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name="User Account"
    )
    image = models.FileField(
        upload_to=user_directory_path,
        default="default.jpg",
        null=True,
        blank=True,
        verbose_name="Profile Image"
    )
    mobile_no = models.CharField(
        max_length=17,
        validators=[phone_validator],
        verbose_name="Mobile Number",
        help_text="Primary contact number"
    )
    country = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name="Country"
    )
    city = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name="City"
    )
    state = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name="State/Province"
    )
    address = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name="Full Address"
    )
    identity_type = models.CharField(
        max_length=200,
        choices=IDENTITY_TYPE,
        default="Fayda Alias Number (FAN)",
        null=True,
        blank=True,
        verbose_name="ID Type"
    )
    identity_image = models.ImageField(
        upload_to=user_directory_path,
        default="id.jpg",
        null=True,
        blank=True,
        verbose_name="ID Document"
    )
    facebook = models.URLField(
        null=True,
        blank=True,
        verbose_name="Facebook Profile"
    )
    twitter = models.URLField(
        null=True,
        blank=True,
        verbose_name="Twitter Profile"
    )
    wallet = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0.00,
        verbose_name="Wallet Balance"
    )
    verified = models.BooleanField(
        default=False,
        verbose_name="Verified Account"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username}'s Profile"

    def clean(self):
        if not self.mobile_no and not self.user.phone:
            raise ValidationError("At least one phone number must be provided")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

# === Teacher Model ===
class Teacher(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='teacher_profile',
        verbose_name="User Account"
    )
    qualification = models.CharField(
        max_length=100,
        verbose_name="Qualifications",
        help_text="Degrees, certifications, etc."
    )
    bio = models.TextField(
        null=True,
        blank=True,
        verbose_name="Professional Bio"
    )
    specialties = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name="Teaching Specialties"
    )
    experience_years = models.PositiveIntegerField(
        default=0,
        verbose_name="Years of Experience"
    )
    hourly_rate = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=0.00,
        verbose_name="Hourly Rate"
    )
    is_approved = models.BooleanField(
        default=False,
        verbose_name="Approved Teacher"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Teacher"
        verbose_name_plural = "Teachers"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.full_name} (Teacher)"

    def clean(self):
        if self.user.role != 'tutor':
            raise ValidationError("Associated user must have tutor role")

# === Student Model ===
class Student(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='student_profile',
        verbose_name="User Account"
    )
    grade_level = models.CharField(
        max_length=100,
        verbose_name="Grade Level"
    )
    school = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name="Current School"
    )
    learning_goals = models.TextField(
        null=True,
        blank=True,
        verbose_name="Learning Objectives"
    )
    parent_guardian_name = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name="Parent/Guardian Name"
    )
    parent_guardian_contact = models.CharField(
        max_length=17,
        validators=[phone_validator],
        null=True,
        blank=True,
        verbose_name="Parent/Guardian Contact"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Student"
        verbose_name_plural = "Students"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.full_name} (Student)"

    def clean(self):
        if self.user.role != 'student':
            raise ValidationError("Associated user must have student role")

# === Course Category ===
class CourseCategory(models.Model):
    title = models.CharField(
        max_length=150,
        unique=True,
        verbose_name="Category Title"
    )
    description = models.TextField(
        verbose_name="Category Description"
    )
    icon = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        help_text="Font Awesome icon class"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Active Category"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Course Category"
        verbose_name_plural = "Course Categories"
        ordering = ['title']

    def __str__(self):
        return self.title

# === Course Model ===
class Course(models.Model):
    category = models.ForeignKey(
        CourseCategory,
        on_delete=models.CASCADE,
        related_name='courses',
        verbose_name="Category"
    )
    teacher = models.ForeignKey(
        Teacher,
        on_delete=models.CASCADE,
        related_name='courses',
        verbose_name="Instructor"
    )
    title = models.CharField(
        max_length=150,
        verbose_name="Course Title"
    )
    description = models.TextField(
        verbose_name="Course Description"
    )
    syllabus = models.TextField(
        null=True,
        blank=True,
        verbose_name="Detailed Syllabus"
    )
    duration_weeks = models.PositiveIntegerField(
        default=4,
        verbose_name="Duration (weeks)"
    )
    price = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=0.00,
        verbose_name="Course Price"
    )
    is_featured = models.BooleanField(
        default=False,
        verbose_name="Featured Course"
    )
    status = models.CharField(
        max_length=20,
        choices=(
            ('draft', 'Draft'),
            ('published', 'Published'),
            ('archived', 'Archived'),
        ),
        default='draft',
        verbose_name="Course Status"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Course"
        verbose_name_plural = "Courses"
        ordering = ['-created_at']
        unique_together = ['category', 'title']

    def __str__(self):
        return f"{self.title} by {self.teacher.user.username}"

# === Signals ===
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        try:
            Profile.objects.create(
                user=instance,
                mobile_no=instance.phone or ""
            )
            if instance.role == 'tutor':
                Teacher.objects.create(user=instance)
            elif instance.role == 'student':
                Student.objects.create(user=instance)
        except Exception as e:
            logger.error(f"Error creating profile: {e}")

def update_user_roles(sender, instance, created, **kwargs):
    if not created:
        try:
            if hasattr(instance, 'teacher_profile'):
                instance.role = 'tutor'
                instance.save()
            elif hasattr(instance, 'student_profile'):
                instance.role = 'student'
                instance.save()
        except Exception as e:
            logger.error(f"Error updating user roles: {e}")

post_save.connect(create_user_profile, sender=User)
post_save.connect(update_user_roles, sender=Teacher)
post_save.connect(update_user_roles, sender=Student)