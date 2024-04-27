import csv
from django.core.management.base import BaseCommand
from company.models import Company

class Command(BaseCommand):
    help = 'Import Company data from CSV'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the CSV file')

    def handle(self, *args, **kwargs):
        csv_file = kwargs['csv_file']

        with open(csv_file, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                my_model_instance = Company(
                    symbol_val=row['Symbol'],
                )
                my_model_instance.save()

        self.stdout.write(self.style.SUCCESS('Data imported successfully'))