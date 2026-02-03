from django.core.management.base import BaseCommand
from inventory.etl import run_etl

class Command(BaseCommand):
    help = "Run inventory ETL pipeline"

    def add_arguments(self, parser):
        parser.add_argument("csv_path", type=str)

    def handle(self, *args, **options):
        run_etl(options["csv_path"])
        self.stdout.write(self.style.SUCCESS("ETL completed successfully"))
