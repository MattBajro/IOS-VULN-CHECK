import django_tables2 as tables
from django_tables2.utils import A

from .models import CiscoDevice, IosVulnerability

class CiscoDeviceTable(tables.Table):
    device_name = tables.LinkColumn('device-details', args=[A('pk')], orderable=True)
    ios_version = tables.Column(orderable=True)
    ios_type = tables.Column(orderable=True)
    vulnerabs = tables.Column(orderable=True)

    def render_vulnerabs(self, value):
        return '%s' % (len(value.all()))


class VulnerabilityTable(tables.Table):
    cisco_id = tables.LinkColumn('vuln-details', args=[A('pk')], orderable=True)
    severity = tables.Column(orderable=True)
    url = tables.Column(orderable=True)
