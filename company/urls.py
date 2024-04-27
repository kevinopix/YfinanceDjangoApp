from django.urls import path
# from django.views.generic.base import View
from .views import CompanyAllView, SingleCompanyView

urlpatterns = [
    path('', CompanyAllView.as_view(), name='home'),
    path('company/<int:company_id>/', SingleCompanyView.as_view(), name='company_detail'),
]