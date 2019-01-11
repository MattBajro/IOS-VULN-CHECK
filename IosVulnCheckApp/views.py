# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import logging

from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django_tables2 import RequestConfig
from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin
from django.core.exceptions import ObjectDoesNotExist

from .models import CiscoDevice, IosVulnerability
from .tables import CiscoDeviceTable, VulnerabilityTable
from .filters import CiscoDeviceFilter, IosVulnerabilityFilter
from .forms import UpdateDeviceDbForm

logger = logging.getLogger('testlogger')

def index(request):
    return HttpResponse("Hello, world. This is VulnCheckApp index.")


class FilteredDeviceListView(SingleTableMixin, FilterView):
    table_class = CiscoDeviceTable
    paginate_by = 20
    model = CiscoDevice
    template_name = 'IosVulnCheckApp/devicetable.html'

    filterset_class = CiscoDeviceFilter


class FilteredVulnListView(SingleTableMixin, FilterView):
    table_class = VulnerabilityTable
    paginate_by = 20
    model = IosVulnerability
    template_name = 'IosVulnCheckApp/vulntable.html'

    filterset_class = IosVulnerabilityFilter


def device_details(request, device_id):
    dev = CiscoDevice.objects.get(pk=device_id)
    table = VulnerabilityTable(
        data=dev.vulnerabs.all(),
        orderable=True,
        order_by='severity',
        template_name='django_tables2/bootstrap.html'
    )
    RequestConfig(request, paginate={'per_page': 25}).configure(table)

    logger.info('Testing my logging!')

    return render(
        request,
        'IosVulnCheckApp/devicedetail.html',
        {
            'table' : table,
            'device' : dev
        }
    )


def vuln_details(request, vuln_id):
    try:
        vuln = IosVulnerability.objects.get(pk=vuln_id)
    except ObjectDoesNotExist as e:
        errmsg = "Vulnerability '{}' was not found in our database.".format(vuln_id) 
        return HttpResponse(errmsg)

    table = CiscoDeviceTable(
        data=vuln.ciscodevice_set.all(),
        orderable=True,
        order_by='severity',
        template_name='django_tables2/bootstrap.html'
    )
    RequestConfig(request, paginate={'per_page': 25}).configure(table)

    return render(
        request,
        'IosVulnCheckApp/vulndetail.html',
        {
            'table' : table,
            'vuln' : vuln
        }
    )


def maintenance(request):

    if request.method == 'POST':
        form = UpdateDeviceDbForm(request.POST)
        if form.is_valid():
            return render(
                request,
                'IosVulnCheckApp/maintenance2.html',
                {
                    'form' : form,
                    'tab' : 'tablet lol',
                    'vul' : 'vul lol'
                }
            )
    
    else:
        form = UpdateDeviceDbForm()
            
    return render(
        request,
        'IosVulnCheckApp/maintenance.html',
        {
            'form' : form,
            'tab' : 'tablet lol',
            'vul' : 'vul lol'
        }
    )
