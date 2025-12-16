import csv
from django.core.management.base import BaseCommand
from chatbot.models import FQA as FAQ

class Command(BaseCommand):
    help = "Import FAQ from CSV file"

    def handle(self, *args, **kwargs):
        with open("faq_supnum.csv", newline="", encoding="cp1252") as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                FAQ.objects.create(
                    category=row.get("category", ""),
                    question_ar=row.get("question_ar", ""),
                    answer_ar=row.get("answer_ar", ""),
                    question_fr=row.get("question_fr", ""),
                    answer_fr=row.get("answer_fr", ""),
                    keywords=row.get("keywords", ""),
                )

        self.stdout.write(self.style.SUCCESS("✅ FAQ imported successfully"))
