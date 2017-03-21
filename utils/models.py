from __future__ import unicode_literals

from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20)
    unit_price   = models.FloatField()

    def __unicode__(self):
        return self.name + "(" + self.code + ")"
