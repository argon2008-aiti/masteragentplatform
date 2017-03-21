from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User


class Agent(models.Model):
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=200)
    location = models.CharField(max_length=100)
    user = models.OneToOneField(User)

    def __unicode__(self):
        return self.name

class Shop(models.Model):
    location = models.CharField(max_length=100)
    agent = models.ForeignKey(Agent)

    def __unicode__(self):
        return self.agent.name + " " + self.location

class ShopAssistant(models.Model):
    user = models.OneToOneField(User)
    shop = models.OneToOneField(Shop)

    def __unicode__(self):
        return self.user.last_name + " --  " + self.shop.agent.name

