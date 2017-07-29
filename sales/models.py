from __future__ import unicode_literals

from django.db import models

from agent.models import Vendor
from utils.models import Product

class VendorBooking(models.Model):
    date   = models.DateField()
    vendor = models.ForeignKey(Vendor)
    closed = models.BooleanField(default=False)
    paid   = models.BooleanField(default=False)
    total  = models.FloatField(blank=True, null=True, default=0.0)
    amount_paid = models.FloatField(blank=True, null=True, default=0.0)

    class Meta:
        ordering= ['-date']

    '''
    def get_total(self):
        total = 0
        bookings = self.productbooking_set.all()
        for booking in bookings:
            total = total + booking.booking*booking.product.unit_price 
        return total

    def save(self, *args, **kwargs):
        self.total = self.get_total()
        return super(VendorBooking, self).save(*args, **kwargs)
    '''

class ProductBooking(models.Model):
    product = models.ForeignKey(Product)
    master_booking = models.ForeignKey(VendorBooking)
    booking = models.IntegerField()
    returns = models.IntegerField(default=0)
    
