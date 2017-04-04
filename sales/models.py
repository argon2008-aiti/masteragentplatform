from __future__ import unicode_literals

from django.db import models

from agent.models import Vendor
from utils.models import Product

class VendorBooking(models.Model):
    date   = models.DateField()
    vendor = models.ForeignKey(Vendor)
    closed = models.BooleanField(default=False)
    paid   = models.BooleanField(default=False)
    amount_paid = models.NullBooleanField(blank=True, null=True)

    def __unicode__(self):
        return self.vendor.first_name + " " + self.vendor.last_name

class ProductBooking(models.Model):
    product = models.ForeignKey(Product)
    master_booking = models.ForeignKey(VendorBooking)
    booking = models.IntegerField()
    returns = models.IntegerField(default=0)
    
