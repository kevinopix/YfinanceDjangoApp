from django.core.management.base import BaseCommand
from company.models import StockInfo, Company
import pyarrow.parquet as pq
import pandas as pd

class Command(BaseCommand):
    help = 'Import data from a Parquet file'

    def add_arguments(self, parser):
        parser.add_argument('parquet_file', type=str, help='Path to the Parquet file')

    def handle(self, *args, **kwargs):
        parquet_file = kwargs['parquet_file']
        table = pq.read_table(parquet_file)
        df = table.to_pandas()
        try:
            batch_size = 4999
            for i in range(0, len(df), batch_size):
                batch = df[i:i + batch_size]
                print(f"Batch number {i} uploading now..........")
                objects = []
                for index, row in batch.iterrows():
                    company, created = Company.objects.get_or_create(symbol_val=row['symbol'])
                    try:
                        obj = StockInfo.objects.get(symbol=company, 
                                                    date=row['date'],
                                                    Open=row['Open'],
                                                    High=row['High'],
                                                    Low=row['Low'],
                                                    Close=row['Close'],
                                                    Adj_Close=row['Adj Close'],
                                                    Volume=row['Volume'])
                    except StockInfo.DoesNotExist:
                        company, created = Company.objects.get_or_create(symbol_val=row['symbol'])
                        stock_info = StockInfo(
                            symbol=company,
                            date=row['date'],
                            Open=row['Open'],
                            High=row['High'],
                            Low=row['Low'],
                            Close=row['Close'],
                            Adj_Close=row['Adj Close'],
                            Volume=row['Volume']
                        )
                        objects.append(stock_info)
                StockInfo.objects.bulk_create(objects)
            self.stdout.write(self.style.SUCCESS('Data imported successfully'))
        except Exception as e:
            print(e)
