from __future__ import unicode_literals

from django.db import models
from utils.models import Product
from agent.models import Shop

PURCHASE_TYPE = [
    (0, "Credit Purchase"),
    (1, "Cash Purchase")
]

PAYMENT_TYPE = [
    (0, "Cheque Payment"),
    (1, "Cash Payment")
]

class Cheque(models.Model):
    bank = models.CharField(max_length=100)
    account_number = models.CharField(max_length=100)
    cheque_date = models.DateField()
    cheque_number = models.IntegerField()

class ProductPayment(models.Model):
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    payment_type = models.IntegerField(choices=PAYMENT_TYPE, default=1) 
    amount_paid = models.FloatField()
    cheque = models.ForeignKey(Cheque, null=True, blank=True)

class DayPurchase(models.Model):
    shop = models.ForeignKey(Shop)
    date = models.DateField()
    purchase_type = models.IntegerField(choices=PURCHASE_TYPE, default=1)
    invoice_number = models.CharField(max_length=100)
    payment = models.ForeignKey(ProductPayment, null=True, blank=True)
    total = models.FloatField()
    month = models.IntegerField()

    class Meta:
        ordering = ['-date']

    def __unicode__(self):
        return self.shop.location + " ---- " + self.date.strftime('%m/%d/%Y')

    def get_total(self):
        total = 0
        purchases = self.productpurchase_set.all()
        for purchase in purchases:
            total = total + purchase.quantity*purchase.product.unit_price 
        return total

    def get_payment_status(self):
        if self.payment == None:
            return "Unpaid"
        else:
            return "Paid"

    def save(self, *args, **kwargs):
        self.total = self.get_total()
        self.month = self.date.month
        return super(DayPurchase, self).save(*args, **kwargs)

class ProductPurchase(models.Model):
    product = models.ForeignKey(Product) 
    quantity = models.IntegerField()
    master_purchase = models.ForeignKey(DayPurchase)

    def __unicode__(self):
        return self.product.name + " ---- "+ str(self.quantity)

