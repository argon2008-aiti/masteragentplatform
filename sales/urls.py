from django.conf.urls import url
from views import *

urlpatterns = [
    url(r'^bookings/all$', AllBookingView.as_view(), name="bookings-all"),
    url(r'^bookings/add/$', NewBookingView.as_view(), name="add-booking"),
    url(r'^metrics/$', NewBookingView.as_view(), name="metrics"),
    url(r'^bookings/edit/(?P<pk>\d+)/$', BookingUpdateView.as_view(), name="edit"),
    url(r'^bookings/close/(?P<pk>\d+)/$', CloseBookingView.as_view(), name="close"),
    url(r'^bookings/pay/(?P<pk>\d+)/$', PayBookingView.as_view(), name="pay"),
    url(r'^bookings/view/(?P<pk>\d+)/$', BookingsDetailView.as_view(), name="view"),
]
