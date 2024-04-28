from django.urls import path
# from django.views.generic.base import View
from .views import checkLatestRecords, PullDataView

urlpatterns = [
    path('dataTool/check_latest', checkLatestRecords.as_view(), name='check_latest_records'),
    # path('dataTool/checknew', CheckNewStockDataView.as_view(), name='check_new_records'),
    path('dataTool/pull', PullDataView.as_view(), name='pull_data')
]