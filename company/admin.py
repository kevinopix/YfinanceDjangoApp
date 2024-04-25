from django.contrib import admin
from .models import Company, StockInfo

# Register your models here.
admin.site.register(Company)
admin.site.register(StockInfo)