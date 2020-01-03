from __future__ import unicode_literals

from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20)
    unit_price   = models.FloatField()

    def __unicode__(self):
        return self.name + "(" + self.code + ")"

vending_products = ['FG/000001', 'FG/000002', 'FG/000003', 'FG/000005', \
                    'FG/000007', 'FG/000004', 'FG/000020', 'FG/000026', 'FG/000059']
