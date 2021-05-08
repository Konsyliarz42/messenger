from django.contrib import admin

from .models import Profile, Conversation


admin.site.register(Profile)
admin.site.register(Conversation)