from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver

from .models import Profile


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    """
    Signal to create a Profile instance when a new User is created.

    :param sender: The model class sending the signal.
    :param instance: The instance of the model.
    :param created: Boolean indicating if the instance was created.
    """
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    """
    Signal to save the Profile instance when the User is saved.

    :param sender: The model class sending the signal.
    :param instance: The instance of the model.
    """
    instance.profile.save()

