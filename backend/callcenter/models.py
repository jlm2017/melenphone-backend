# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.utils import timezone
import datetime

__all__ = ['UserExtend', 'Achievement', 'AchievementUnlock', 'NumbersLocation', 'Call']

def get_default_date():
    return timezone.now() - datetime.timedelta(days=1)

class UserExtend(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name="UserExtend")
    agentUsername = models.CharField(max_length=50, unique=True)
    location_lat = models.CharField(default=None, max_length=20, blank=True, null=True)
    location_long = models.CharField(default=None, max_length=20, blank=True, null=True)
    phi = models.IntegerField(default=0, blank=True, null=True)
    phi_multiplier = models.DecimalField(default=1.0, max_digits=2, decimal_places=1, blank=True, null=True)
    first_call_of_the_day = models.DateTimeField(default=get_default_date, blank=True)

    def __str__(self):
        return self.agentUsername

    def get_achievements(self):
        return self.achievements_aux.all()

class Achievement(models.Model):
    codeName = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=50)
    condition = models.CharField(max_length=300)
    phi = models.IntegerField(default=0)
    unlockers = models.ManyToManyField(UserExtend,through='AchievementUnlock', related_name="achievements_aux")

    def __str__(self):
        return self.codeName

class AchievementUnlock(models.Model):
    userExtend = models.ForeignKey(UserExtend)
    achievement = models.ForeignKey(Achievement)

class NumbersLocation(models.Model):
    code = models.CharField(max_length=6)
    pays = models.CharField(max_length=3)
    zone = models.CharField(max_length=1)
    indicatif = models.CharField(max_length=2)
    location_lat = models.CharField(max_length=20)
    location_long = models.CharField(max_length=20)

    def get_location(self):
        return self.location_lat, self.location_long

class Call(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True)
    date = models.DateTimeField(auto_now=True)
