# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from .models import CiscoDevice, IosVulnerability, VulnMapper

admin.site.register(CiscoDevice)
admin.site.register(IosVulnerability)
admin.site.register(VulnMapper)
