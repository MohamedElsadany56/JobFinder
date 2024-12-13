from django.db import models
from django.contrib.auth.models import User # type: ignore
from django.db.models.signals import post_save
from django.dispatch import receiver
import random

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=50)
    email = models.EmailField(max_length=100)
    is_verified = models.BooleanField(default=False)
    otp = models.CharField(max_length=6, blank=True, null=True)

    def __str__(self):
        return str(self.user)

    def generate_otp(self):
        self.otp = str(random.randint(100000, 999999))
        self.save()

# Create and save Profile
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()