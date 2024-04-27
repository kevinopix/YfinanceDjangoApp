from django.contrib import admin
from .models import Company, StockInfo, CompanyMetric

# Register your models here.
class CompanyAdmin(admin.ModelAdmin):
    list_display = ("symbol_val", "title")

class StockInfoAdmin(admin.ModelAdmin):
    list_display = ("symbol", "date", "Open", "Close", "Volume")


class CompanyMetricAdmin(admin.ModelAdmin):
    list_display = ("symbol", "date_min", "date_max")


admin.site.register(Company, CompanyAdmin)
admin.site.register(StockInfo, StockInfoAdmin)
admin.site.register(CompanyMetric, CompanyMetricAdmin)