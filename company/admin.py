from django.contrib import admin
from .models import Company, StockInfo

# Register your models here.
class CompanyAdmin(admin.ModelAdmin):
    list_display = ("symbol_val", "title")

class StockInfoAdmin(admin.ModelAdmin):
    list_display = ("symbol", "date", "Open", "Close", "Volume")


admin.site.register(Company, CompanyAdmin)
admin.site.register(StockInfo, StockInfoAdmin)