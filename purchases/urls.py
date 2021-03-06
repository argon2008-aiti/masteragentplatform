from django.conf.urls import url
from views import *

urlpatterns = [
    url(r'^all/$', DayPurchaseListView.as_view(), name="all"),
    url(r'^damages/all/$', DamageCountListView.as_view(), name="damages-all"),
    url(r'^new/$', NewPurchaseView.as_view(), name="new"),
    url(r'^damages/new/$', NewDamageCountView.as_view(), name="damages-new"),
    url(r'^metrics/$', PurchaseMetricsView.as_view(), name="metrics"),
    url(r'^detail/(?P<pk>\d+)/$', DayPurchaseDetail.as_view(), name="detail"),
]
