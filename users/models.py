# users/models.py
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    membership_id = models.CharField(max_length=36, unique=True, editable=False)  # UUID for digital card

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        if not self.membership_id:  # Only set on initial creation if not already set
            self.membership_id = str(uuid.uuid4())
        super().save(*args, **kwargs)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    # Ensures the profile is saved whenever the User is saved
    try:
        instance.profile.save()
    except Profile.DoesNotExist:
        # Create a profile if somehow missing for an existing user
        Profile.objects.create(user=instance)
