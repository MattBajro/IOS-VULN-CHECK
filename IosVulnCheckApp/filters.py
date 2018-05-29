from django_filters import FilterSet

from .models import CiscoDevice

class CiscoDeviceFilter(FilterSet):
    class Meta:
        model = CiscoDevice
        fields = {
            'ios_version': ['contains'],
            'device_name': ['contains']
        }
