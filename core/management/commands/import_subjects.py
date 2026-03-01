import csv
from django.core.management.base import BaseCommand
from core.models import Subject  # change "your_app" to your app name


class Command(BaseCommand):
    help = "Import subjects from a CSV file"

    def add_arguments(self, parser):
        parser.add_argument(
            "csv_file",
            type=str,
            help="Path to the CSV file containing subjects",
        )

    def handle(self, *args, **kwargs):
        csv_file = kwargs["csv_file"]
        created_count = 0

        with open(csv_file, newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            for row in reader:
                name = row.get("name").strip()
                code = row.get("code", "").strip()
                category = row.get("category", "").strip()

                # Avoid duplicates
                subject, created = Subject.objects.get_or_create(
                    name=name,
                    defaults={
                        "code": code,
                        "category": category,
                    },
                )

                if created:
                    created_count += 1

        self.stdout.write(
            self.style.SUCCESS(f"Successfully imported {created_count} subjects")
        )