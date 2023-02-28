from django.urls import path
from api.views import BillView, UsageView

urlpatterns = [
    path("aws/usage/", UsageView.as_view(), name="usage_view"),
    path("aws/bill/", BillView.as_view(), name="bill_view"),
]
