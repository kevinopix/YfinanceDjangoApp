from django.urls import path
# from django.views.generic.base import View
from .views import checkLatestRecords

urlpatterns = [
    path('dataTool/check_latest', checkLatestRecords.as_view(), name='check_latest_records'),
]