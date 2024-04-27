from django.shortcuts import render
from django.views import View
from django.views.generic import DetailView
from django.shortcuts import get_object_or_404
from .models import Company, CompanyMetric, StockInfo
import matplotlib.pyplot as plt
import io
import base64

# Create your views here.
class CompanyAllView(View):
    template_name = 'home/index.html'
    def get(self,request,*args,**kwargs):
        companies = Company.objects.all()
        context={
            'all_companies': companies 
        }
        # print(context)
        return render(request, self.template_name,context)




class SingleCompanyView(DetailView):
    model = Company
    template_name = 'companies/single_company.html'
    context_object_name = 'company'
    pk_url_kwarg = 'company_id'

    def get(self,request,*args,**kwargs):
        company = get_object_or_404(self.model, id=kwargs['company_id'])
        # print(str(post_obj))
        companymetric = CompanyMetric.objects.get(symbol_id=company.id)
        context={
            'company': company,
            'companymetric': companymetric,
        }
        stock_data = StockInfo.objects.filter(symbol=company).order_by('date')

        # Extract date and close price for plotting
        dates = [data.date for data in stock_data]
        close_prices = [data.Close for data in stock_data]
        # Plot the data
        plt.figure(figsize=(10, 6))
        plt.plot(dates, close_prices, linestyle='-')
        plt.title(f'Trend for {company}')
        plt.xlabel('Date')
        plt.ylabel('Close Price')
        plt.grid(True)

        # Convert plot to image

        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.read()).decode()
        plt.close()

        context['image_url'] = image_base64
        return render(request, self.template_name,context)
