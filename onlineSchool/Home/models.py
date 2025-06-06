from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from shortuuid.django_fields import ShortUUIDField


# === Constants ===

ROLE_CHOICES = (
    ('admin', 'Admin'),
    ('student', 'Student'),
    ('tutor', 'Tutor'),
)

GENDER = (
    ("Female", "Female"),
    ("Male", "Male"),
    ("gender", "gender")
)

IDENTITY_TYPE = (
    ("Fayda Alias Number (FAN)", "Fayda Alias Number (FAN)"),
    ("Driver's license", "Driver's license"),
    ("International passport", "International passport")
)


# === Utility ===

def user_directory_path(instance, filename):
    ext = filename.split(".")[-1]
    filename = "%s.%s" % (instance.user.id, ext)
    return "user_{0}/{1}".format(instance.user.id, filename)


# === Custom User Model ===

class User(AbstractUser):
    full_name = models.CharField(max_length=100, null=True, blank=True)
    username = models.CharField(max_length=100, unique=True)
    mobile_no = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=100, null=True, blank=True)
    gender = models.CharField(max_length=20, choices=GENDER, default="gender")
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="student")
    otp = models.CharField(max_length=100, null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username


# === Profile for Additional Info ===

class Profile(models.Model):
    pid = ShortUUIDField(length=7, max_length=25, alphabet="abcdefghijklmnopqrstuvwxyz12345")
    image = models.FileField(upload_to=user_directory_path, default="default.jpg", null=True, blank=True)
    mobile_no = models.CharField(max_length=100)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=100, null=True, blank=True)
    gender = models.CharField(max_length=20, choices=GENDER, default="gender")
    country = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)

    identity_type = models.CharField(max_length=200, choices=IDENTITY_TYPE, default="Fayda Alias Number (FAN)", null=True, blank=True)
    identity_image = models.ImageField(upload_to=user_directory_path, default="id.jpg", null=True, blank=True)

    facebook = models.URLField(null=True, blank=True)
    twitter = models.URLField(null=True, blank=True)

    wallet = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    verified = models.BooleanField(default=False)

    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['date']

    def __str__(self):
        return self.user.full_name or self.user.username


# === Teacher Model ===

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    qualification = models.CharField(max_length=100)
    address = models.TextField()

    def __str__(self):
        return self.user.full_name or self.user.username


# === Student Model ===

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    grade_level = models.CharField(max_length=100)
    address = models.TextField()
    interested_categories = models.TextField()

    def __str__(self):
        return self.user.full_name or self.user.username


# === Course Category ===

class CourseCategory(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField()

    def __str__(self):
        return self.title


# === Course ===

class Course(models.Model):
    category = models.ForeignKey(CourseCategory, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    description = models.TextField()

    def __str__(self):
        return self.title


# === Signal: Auto-create Profile for New Users ===

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

post_save.connect(create_user_profile, sender=User)
post_save.connect(save_user_profile, sender=User)
