from django.contrib.auth.models import User
from django.db import models

from ublogging.models import *
from django.contrib import admin

class Follower (models.Model):
    user = models.ForeignKey(User, related_name='users')
    follower = models.ForeignKey(User, related_name='followers')
    class Meta:
        unique_together = ('user', 'follower')

admin.site.register(Follower)