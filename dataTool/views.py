from django.shortcuts import render
from django.views import View
from django.core.paginator import Paginator
from django.db.models import Max
from company.models import Company, StockInfo
import pandas as pd

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
