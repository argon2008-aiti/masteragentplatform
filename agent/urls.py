from django.conf.urls import url
from django.views.generic import UpdateView
from views import *
from model import Vendor
from forms import VendorForm

urlpatterns = [
    url(r'^all/$', VendorListView.as_view(), name="all"),
    url(r'^all/json$', VendorJSONListView.as_view(), name="all-json"),
    url(r'^new/$', VendorCreate.as_view(), name="new"),
    url(r'^details/(?P<pk>\d+)/$', VendorDetailView.as_view(), name="detail"),
    url(r'^update/(?P<pk>\d+)/$', UpdateView.as_view(
        model=Vendor,
        form_class=VendorForm,
        template_name='agent/vendor_create_form.html',
        success_url='/vendors/all/'
        ), name="update"),
]
