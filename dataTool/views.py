from django.shortcuts import render
from django.views import View
from django.core.paginator import Paginator
from django.db.models import Max
from company.models import Company, StockInfo
from django.http import JsonResponse
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
import base64
from datetime import datetime, timedelta
import yfinance as yf
from django.views.generic import TemplateView
from django.contrib import messages 

class checkLatestRecords(View):
    template_name = 'dataTool/check_available_records.html'

    def get(self, request, *args, **kwargs):
        companies = Company.objects.all()
        context = {
            'all_companies': companies, 
            'company_count': len(companies),
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



class TopBottomSymbolsView(View):
    template_name = 'dataTool/top_bottom_symbols.html'

    def get(self, request, *args, **kwargs):
        # Get top 4 symbols by closing price over the last 5 days
        top_symbols = self.get_top_bottom_symbols(order_by='-Close')

        # Get bottom 4 symbols by closing price over the last 5 days
        bottom_symbols = self.get_top_bottom_symbols(order_by='Close')

        # Plot trends for top and bottom symbols
        top_subplot = self.plot_symbols_trend(top_symbols)
        bottom_subplot = self.plot_symbols_trend(bottom_symbols)

        # Convert subplots to base64 encoded images
        top_image_base64 = self.subplot_to_base64(top_subplot)
        bottom_image_base64 = self.subplot_to_base64(bottom_subplot)

        context = {
            'top_symbols': top_symbols,
            'bottom_symbols': bottom_symbols,
            'top_image_base64': top_image_base64,
            'bottom_image_base64': bottom_image_base64,
        }
        return render(request, self.template_name, context)

    def get_top_bottom_symbols(self, order_by):
        # Get distinct symbols
        symbols = StockInfo.objects.values_list('symbol__symbol_val', flat=True).distinct()

        # Calculate average closing price over the last 10 days for each symbol
        symbol_averages = {}
        for symbol in symbols:
            closing_prices = StockInfo.objects.filter(symbol__symbol_val=symbol).order_by('-date')[:10].values_list('Close', flat=True)
            if closing_prices:  # Check if closing_prices is not empty
                average_price = sum(closing_prices) / len(closing_prices)
                symbol_averages[symbol] = average_price

        # Sort symbols based on closing price average
        sorted_symbols = sorted(symbol_averages, key=lambda x: symbol_averages[x], reverse=(order_by[0] == '-'))

        # Get top or bottom 10 symbols
        if order_by[0] == '-':
            return sorted_symbols[:10]
        else:
            return sorted_symbols[-10:]



    def plot_symbols_trend(self, symbols):
        # Plot trends for symbols
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        for i, symbol in enumerate(symbols):
            ax = axes[i // 2, i % 2]
            stock_data = StockInfo.objects.filter(symbol=symbol).order_by('date')[:5]
            dates = [data.date for data in stock_data]
            close_prices = [data.Close for data in stock_data]
            ax.plot(dates, close_prices, marker='o', linestyle='-')
            ax.set_title(f'Trend for {symbol}')
            ax.set_xlabel('Date')
            ax.set_ylabel('Close Price')
            ax.grid(True)
        return fig

    def subplot_to_base64(self, subplot):
        buffer = io.BytesIO()
        subplot.savefig(buffer, format='png')
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.read()).decode()
        plt.close(subplot)
        return image_base64


class PullDataView(View):
    template_name = 'dataTool/stock_data.html'
    
    def get(self, request, *args, **kwargs):
        context = {
            
        }
        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        # Get the latest date record available
        latest_date_recorded = StockInfo.objects.order_by('-date').first().date
        yesterday = str(latest_date_recorded)
        today = str(datetime.today().date())

        symbols_list = list(Company.objects.values_list('symbol_val', flat=True))
        print(symbols_list)
        # Fetch stock data for each symbol
        # stock_data_df = pd.DataFrame(columns=['Date', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume', 'Symbol'])
        new_records_count = 0
        try:    
            for symbol in symbols_list:
                try:
                    stock_data = yf.download(symbol, start=yesterday, end=today).reset_index()
                    print(stock_data)
                    stock_data['Symbol'] = symbol
                    for _, row in stock_data.iterrows():
                        if not StockInfo.objects.filter(symbol__symbol_val=symbol, date=row['Date']).exists():
                            # Create new StockInfo object if it doesn't already exist
                            StockInfo.objects.create(
                                symbol=Company.objects.get(symbol_val=symbol),
                                date=row['Date'],
                                Open=row['Open'],
                                High=row['High'],
                                Low=row['Low'],
                                Close=row['Close'],
                                Adj_Close=row['Adj Close'],
                                Volume=row['Volume']
                            )
                            new_records_count += 1
                except Exception as e:
                    print(f"Failed to fetch data for {symbol}: {e}")
            messages.success(self.request, "All New items successfully added")
        except Exception as e:
            messages.error(self.request, str(e))
        # Update context with new_records_count
        context = {
            'new_records_count': new_records_count
        }

        return render(request, self.template_name, context)


# class CheckNewStockDataView(TemplateView):
#     template_name = 'dataTool/stock_data.html'

#     def get(self, request, *args, **kwargs):
#         context = {
            
#         }
#         return render(request, self.template_name, context)
