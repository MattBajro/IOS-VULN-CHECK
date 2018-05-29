# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class IosVulnerability(models.Model):
    cisco_id = models.CharField(max_length=100, primary_key=True)
    title = models.CharField(max_length=300)
    url = models.URLField(max_length=300)
    description = models.TextField()
    severity = models.CharField(max_length=300)

    def __str__(self):
        return self.cisco_id

class CiscoDevice(models.Model):
    device_name = models.CharField(max_length=100, primary_key=True)
    ios_version = models.CharField(max_length=100)
    ios_type = models.CharField(max_length=10, default="unknown")
    vulnerabs = models.ManyToManyField(
        IosVulnerability,
        through='VulnMapper',
        through_fields=('device', 'vulnerab')
    )

    def __str__(self):
        return self.device_name

class VulnMapper(models.Model):
    device = models.ForeignKey(CiscoDevice, on_delete=models.CASCADE)
    vulnerab = models.ForeignKey(IosVulnerability, on_delete=models.CASCADE)
    ios_version = models.CharField(max_length=100)
    affecting = models.BooleanField(default=False)

    def __str__(self):
        return self.device.__str__() + ">>" + self.vulnerab.__str__()
