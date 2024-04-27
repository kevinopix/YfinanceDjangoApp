from django.core.management.base import BaseCommand
from django.db.models import Q
from company.models import StockInfo, Company, CompanyMetric
import pyarrow.parquet as pq
import pandas as pd

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        try:
            stocks_df = pd.DataFrame(StockInfo.objects.values_list("symbol__symbol_val","date"), columns=['symbol','date'])
            print(print(stocks_df))
            stocks_df_grouped = stocks_df.groupby(['symbol'])['date'].agg(['min','max']).reset_index()
            stocks_df_grouped.columns=['symbol', 'date_min','date_max']
            print(stocks_df_grouped)

            batch_size = 20
            for i in range(0, len(stocks_df_grouped), batch_size):
                batch = stocks_df_grouped[i:i + batch_size]
                print(f"Batch number {i} uploading now..........")
                objects = []
                for index, row in batch.iterrows():
                    company, created = Company.objects.get_or_create(symbol_val=row['symbol'])
                    try:
                        obj = CompanyMetric.objects.get(symbol=company, 
                                                    date_min=row['date_min'],
                                                    date_max=row['date_max']
                                                    )
                    except CompanyMetric.DoesNotExist:
                        stock_info = CompanyMetric(
                            symbol=company,
                            date_min=row['date_min'],
                            date_max=row['date_max']
                        )
                        objects.append(stock_info)
                CompanyMetric.objects.bulk_create(objects)
            self.stdout.write(self.style.SUCCESS('Data imported successfully'))
        except Exception as e:
            print(e)