from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save

from datetime import datetime, date
from . import DATETIME_FORMAT

class Profile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    friends = models.ManyToManyField(User, related_name='friends')
    description = models.TextField(blank=True)
    conversations = models.ManyToManyField('Conversation')

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

    def get_conversations(self):
        "Return list of tuples with name and conversation object."

        conversations = list()

        for conversation in self.conversations.all():
            members = conversation.members.all()
            name = ', '.join([user.username for user in members if user != self.user])
            conversations.append((name, conversation))

        return conversations


class Conversation(models.Model):

    start_conversation = models.DateTimeField()
    members = models.ManyToManyField(User)
    entries = models.JSONField(default=dict) # {datetime: (user_id, message)}

    #--------------------------------

    def __repr__(self):

        members = ', '.join([user.username for user in self.members.all()])

        return f"<Conversation: {self.id} | {members}>"

    #--------------------------------

    def get_entries(self):
        """Return entries with user object."""

        entries = dict()
        
        for date in self.entries:
            user_id = self.entries[date][0]
            message = self.entries[date][1]

            if User.objects.filter(pk=user_id).all():
                user = User.objects.get(id=user_id)
            else:
                user = user_id

            entries[date] = (user, message)

        return entries


    def add_entry(self, owner, text):
        """Add entry to the conversation."""

        datetime_entry = str(datetime.now())
        user_id = owner.id
        self.entries[datetime_entry] = (user_id, text)

        if not self.start_conversation:
            self.start_conversation = date.today()

