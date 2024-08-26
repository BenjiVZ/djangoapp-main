from django.contrib.auth.models import User
from django.db import models

class Profile(models.Model):
    USER_ROLES = (
        ('admin', 'Admin'),
        ('regular', 'Regular User'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=USER_ROLES, default='regular')

    def __str__(self):
        return self.user.username

#=========================

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
