from django.conf.urls import url
from views import *

urlpatterns = [
    url(r'^bookings/all$', AllBookingView.as_view(), name="bookings-all"),
    url(r'^bookings/add/$', NewBookingView.as_view(), name="add-booking"),
    url(r'^metrics/$', NewBookingView.as_view(), name="metrics"),
    url(r'^bookings/detail/(?P<pk>\d+)/$', NewBookingView.as_view(), name="detail"),
]
