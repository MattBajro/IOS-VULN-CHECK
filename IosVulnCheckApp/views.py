# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django_tables2 import RequestConfig
from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin

from .models import CiscoDevice
from .tables import CiscoDeviceTable, CiscoFDeviceTable, VulnDeviceTable
from .filters import CiscoDeviceFilter

def index(request):
    return HttpResponse("Hello, world. This is VulnCheckApp index.")


def device_table(request):
    table = CiscoDeviceTable(
        data=CiscoDevice.objects.all(),
        orderable=True,
        order_by='device_name',
        template_name='django_tables2/bootstrap.html'
    )
    RequestConfig(request, paginate={'per_page': 25}).configure(table)

    return render(
        request,
        'IosVulnCheckApp/devicetable.html',
        {'table' : table}
    )


class FilteredCiscoListView(SingleTableMixin, FilterView):
    table_class = CiscoDeviceTable
    paginate_by = 20
    model = CiscoDevice
    template_name = 'IosVulnCheckApp/filterdevicetable.html'

    filterset_class = CiscoDeviceFilter


def device_details(request, device_id):
    dev = CiscoDevice.objects.get(pk=device_id)
    table = VulnDeviceTable(
        data=dev.vulnerabs.all(),
        orderable=True,
        order_by='severity',
        template_name='django_tables2/bootstrap.html'
    )
    RequestConfig(request, paginate={'per_page': 25}).configure(table)

    return render(
        request,
        'IosVulnCheckApp/devicedetail.html',
        {
            'table' : table,
            'device' : dev
        }
    )


def vuln_details(request, vuln_id):
    return HttpResponse("Hello, world. This is Vuln detail page.")
