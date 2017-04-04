from django.conf.urls import url
from views import *

urlpatterns = [
    url(r'^all/$', VendorListView.as_view(), name="all"),
    url(r'^all/json$', VendorJSONListView.as_view(), name="all-json"),
    url(r'^new/$', VendorCreate.as_view(), name="new"),
]
