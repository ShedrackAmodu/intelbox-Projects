 
#To ensure that whenever a user (superuser or normal user) is created,
# their profile is automatically saved to the storefront_userprofile table,
# you can use Django's signals. Signals allow you to hook into the user creation process 
# and perform actions automatically when a user is created.
# this is not used again because it doesnt save email as email are not created upon registering 
# user in the admin sitte.  if you want to use uncomment in apps.py
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import UserProfile

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()


# Signal to create or update a UserProfile instance when a User instance is created or saved
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    else:
        instance.userprofile.save()