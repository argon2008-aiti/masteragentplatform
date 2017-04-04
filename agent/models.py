from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User

from PIL import Image

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


class Vendor(models.Model):
    first_name = models.CharField(max_length=100)
    last_name  = models.CharField(max_length=100)
    phone      = models.CharField(max_length=50)
    hometown   = models.CharField(max_length=100)
    date_of_birth = models.DateField(blank=True, null=True)

    guarantor  = models.CharField(max_length=100)
    guarantor_location = models.CharField(max_length=100, default="Accra")
    relation   = models.CharField(max_length=100)
    guarantor_phone = models.CharField(max_length=50)

    profile = models.ImageField(upload_to="static/profiles/", blank=True, default="static/profiles/default.png")

    agent       = models.ForeignKey(Agent, blank=True, null=True)

    def __unicode__(self):
        return self.first_name + " " + self.last_name

