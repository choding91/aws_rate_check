from django.urls import path
from api.views import UsageView

urlpatterns = [
    path("aws/usage/", UsageView.as_view(), name="usage_view"),
]
