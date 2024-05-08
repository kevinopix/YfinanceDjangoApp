from django.shortcuts import render
from django.views import View
from django.views.generic import DetailView
from django.shortcuts import get_object_or_404
from .models import Company, CompanyMetric, StockInfo
from django.template.defaulttags import register
from django.core.paginator import Paginator
from django.db.models import Max
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
import base64
import numpy as np
import pandas as pd

@register.filter  # Register the custom filter
def zip_lists(list1, list2):
    return zip(list1, list2)

def Average(lst): 
    return sum(lst) / len(lst) 

# Create your views here.
class CompanyAllView(View):
    template_name = 'home/index.html'
    
    def get(self, request, *args, **kwargs):
        # Get top and bottom symbols
        all_symbols = self.get_top_bottom_symbols(order_by='-average_close')
        top_symbols = all_symbols[:6]
        bottom_symbols = all_symbols[-6:]

        # Ensure top and bottom symbols are exclusive
        common_symbols = set(top_symbols) & set(bottom_symbols)
        if common_symbols:
            top_symbols = [symbol for symbol in top_symbols if symbol not in common_symbols]
            bottom_symbols = [symbol for symbol in bottom_symbols if symbol not in common_symbols]

        # Plot trends for top and bottom symbols
        top_images = self.plot_symbols_trend(top_symbols)
        bottom_images = self.plot_symbols_trend(bottom_symbols)

        context = {
            'top_symbols': top_symbols,
            'bottom_symbols': bottom_symbols,
            'top_images': top_images,
            'bottom_images': bottom_images,
        }
        # Get the latest date for each symbol
        latest_dates = (
            StockInfo.objects
            .values('symbol')
            .annotate(latest_date=Max('date'))
        )
        
        # Retrieve the corresponding record for each symbol with the latest date
        latest_records = []
        for entry in latest_dates:
            symbol = entry['symbol']
            latest_date = entry['latest_date']
            record = StockInfo.objects.filter(symbol=symbol, date=latest_date).first()
            if record:
                latest_records.append(record)

        # Convert objects to dictionaries
        records_dict = [{
            'symbol': record.symbol,
            'symbol_pk': record.symbol.pk,
            'date': record.date,
            'Open': record.Open,
            'Close': record.Close,
            'Volume': record.Volume,
        } for record in latest_records]
        
        # Convert list of dictionaries to DataFrame
        latest_records_df = pd.DataFrame(records_dict)
        # Pagination
        paginator = Paginator(latest_records, 20)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj
        context['df'] = latest_records_df
        context['avail_company_count'] = latest_records_df['symbol'].nunique()
        return render(request, self.template_name, context)

    def get_top_bottom_symbols(self, order_by):
        # Get distinct symbols
        symbols = StockInfo.objects.values_list('symbol__symbol_val', flat=True).distinct()

        # Calculate average closing price over the last 30 days for each symbol
        symbol_averages = {}
        for symbol in symbols:
            closing_prices = StockInfo.objects.filter(symbol__symbol_val=symbol
                                                      ).exclude(Close__isnull=True).values_list('Close', flat=True
                                                                    ).order_by('-date')[:30]
            if len(closing_prices) >1:
                average_price = sum(closing_prices) / len(closing_prices) if closing_prices else None
                symbol_averages[symbol] = average_price

        # Sort symbols based on average closing price
        sorted_symbols = sorted(symbol_averages, key=lambda x: symbol_averages[x] or 0, reverse=(order_by[0] == '-'))
        # Return all symbols sorted
        return sorted_symbols

    def plot_symbols_trend(self, symbols):
        # Plot trends for symbols
        images = []
        for symbol in symbols:
            plt.figure(figsize=(6, 4))
            stock_data = StockInfo.objects.filter(symbol__symbol_val=symbol).order_by('-date')[:90]
            dates = [data.date for data in stock_data]  # Extract date objects
            close_prices = [data.Close for data in stock_data]
            plt.plot(dates, close_prices, linestyle='-')
            plt.title(f'Trend for {symbol} over the last month')
            plt.xlabel('Date')
            plt.ylabel('Close Price')
            plt.grid(True)

            # Customize x-axis ticks
            num_dates = len(dates)
            if num_dates > 3:
                step = num_dates // 3  # Show 5 ticks
                plt.xticks(dates[::step], [str(date) for date in dates[::step]])

            # Convert plot to base64 encoded image
            buffer = io.BytesIO()
            plt.savefig(buffer, format='png')
            buffer.seek(0)
            image_base64 = base64.b64encode(buffer.read()).decode()
            plt.close()
            images.append(image_base64)
        return images




def get_latest_stock_info(company):
    # Get the latest record for the specified company
    latest_stock_info = StockInfo.objects.filter(symbol__pk=company).latest('date')
    return latest_stock_info




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
            'stock_info': get_latest_stock_info(company.pk)
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
