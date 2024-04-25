from django.db import models

class Company(models.Model):
    symbol_val = models.CharField(max_length=10, null=False, blank=False)
    title = models.TextField(null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.symbol_val
    
    class Meta:
        verbose_name_plural = "Companies"


class StockInfo(models.Model):
    symbol = models.ForeignKey(Company, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=False)
    Open = models.FloatField()
    High = models.FloatField()
    Low = models.FloatField()
    Close = models.FloatField()
    Adj_Close = models.FloatField()
    Volume = models.BigIntegerField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.symbol.symbol_val
    
    class Meta:
        verbose_name_plural = "Stock Information"