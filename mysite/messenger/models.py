from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save

from datetime import datetime

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    firends = models.JSONField(default=list)

    #--------------------------------

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)


    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()


    def __repr__(self):
        return f"<Profile: {self.user.username} | ID: {self.id}>"


    def __str__(self):
        return self.user.username

    #--------------------------------

    def add_friend(self, user_id):
        """Add id of user as friend.\n
        Return True if all is ok.
        Return False if id user not exist or user is already as friend."""

        if User.objects.filter(pk=user_id).all() and str(user_id) not in self.firends:
            self.firends.append(user_id)

            return True
        
        return False


    def remove_friend(self, user_id):
        """Remove user from friend list."""
        
        self.firends.remove(str(user_id))

    
    def check_firend(self, user_id):
        """Return True if user is a friend or False if not."""

        return str(user_id) in self.firends


    def get_all_friends(self):
        """Return all users as friends."""

        return [User.objects.get(pk=int(user_id)) for user_id in self.firends]


    
        
