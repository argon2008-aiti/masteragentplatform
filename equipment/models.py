from __future__ import unicode_literals

from django.db import models


EQUIPMENT_TYPE = [
      (0, "Bicycle"),
      (1, "Push Cart"),
      (2, "Chest Freezer"),
      (3, "Refridgerator"),
]

EQUIPMENT_STATUS = [
      (0, "OK"),
      (1, "Broken"),
]

class GenericEquipment(models.Model):
    equipment_type = models.IntegerField(choices=EQUIPMENT_TYPE)
    serial_number = models.CharField(max_length=30)
    commission_date = models.DateField()
    status = models.IntegerField(choices=EQUIPMENT_STATUS)


class MaintenanceHistory(models.Model):
    equipment = models.ForeignKey(GenericEquipment)
    fault = models.CharField(max_length=1024)
    date_sent = models.DateField()
    date_received = models.DateField()


class TemperatureRecords(models.Model):
    date = models.DateField()
    equipment = models.ForeignKey(GenericEquipment)
    temperature = models.DecimalField(decimal_places=1, max_digits=2)


