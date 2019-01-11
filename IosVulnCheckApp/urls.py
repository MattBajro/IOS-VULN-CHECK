from django.conf.urls import url
from django.views.generic.base import RedirectView

from . import views

urlpatterns = [
    url(r'^$', views.FilteredDeviceListView.as_view(), name='index'),
    url(r'^device-table$', views.FilteredDeviceListView.as_view(), name='device-table'),
    url(r'^vuln-table$', views.FilteredVulnListView.as_view(), name='vuln-table'),
    url(r'^device-detail/(?P<device_id>[\S ]+)$', views.device_details, name='device-details'),
    url(r'^vuln-detail/(?P<vuln_id>[\S]+)$', views.vuln_details, name='vuln-details'),
    url(r'^maintenance$', views.maintenance, name='maintenance')
]
