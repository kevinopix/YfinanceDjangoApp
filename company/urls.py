from django.urls import path
# from django.views.generic.base import View
from .views import CompanyAllView

urlpatterns = [
    path('', CompanyAllView.as_view(), name='home'),
]