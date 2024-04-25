from django.db import models

class Company(models.Model):
    symbol = models.CharField(max_length=10, null=False, blank=False)
    title = models.TextField(null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.symbol
    
    class Meta:
        verbose_name_plural = "Companies"