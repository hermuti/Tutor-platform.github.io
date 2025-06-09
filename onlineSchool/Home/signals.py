from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import StudentProfile, TutorProfile

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        # Check session for role or add other logic to determine role
        StudentProfile.objects.create(user=instance)
        # Or TutorProfile based on your registration logic