from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.urlresolvers import reverse


class UserProfile(models.Model):
    # class Meta:
    #     app_label = 'userprofile'
    # This links to the user to the user provided by django auth
    user = models.OneToOneField(User, related_name="profile")
    email_notification = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        # userprofile_object.get_absolute_url - userprofile_object (eg UserProfile.objects.get(user_id=request.user.id)
        # that specific user profile object will link to the appropriate url with the kwarg 'profile_id' below relating
        # to <profile_id> in the url.py file
        return reverse('user:profile', kwargs={'profile_id': self.user_id})


# sends a signal every time a new user is created, and calls this method to create the profile
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        profile, new = UserProfile.objects.get_or_create(user=instance)
