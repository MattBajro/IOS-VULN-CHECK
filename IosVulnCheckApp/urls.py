from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^device-table$', views.FilteredCiscoListView.as_view(), name='device-table'),
    url(r'^detail/(?P<device_id>[\S ]+)$', views.device_details, name='device-details'),
    url(r'^vuln-detail/(?P<vuln_id>[\S]+)$', views.vuln_details, name='vuln-details')
]
