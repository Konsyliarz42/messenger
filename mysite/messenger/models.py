from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    firends = models.ManyToManyField(User, related_name='user_firends', blank=True)

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
