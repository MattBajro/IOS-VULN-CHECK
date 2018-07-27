from django_filters import FilterSet

from .models import CiscoDevice, IosVulnerability

class CiscoDeviceFilter(FilterSet):
    class Meta:
        model = CiscoDevice
        fields = {
            'ios_version': ['contains'],
            'device_name': ['contains']
        }


class IosVulnerabilityFilter(FilterSet):
    class Meta:
        model = IosVulnerability
        fields = {
            'cisco_id': ['contains'],
            'severity': ['contains']
        }
