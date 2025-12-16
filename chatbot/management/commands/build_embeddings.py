from django.core.management.base import BaseCommand
from sentence_transformers import SentenceTransformer
from chatbot.models import FQA as FAQ

class Command(BaseCommand):
    help = "Build embeddings for FAQs (SQLite JSONField)"

    def handle(self, *args, **kwargs):
        model = SentenceTransformer("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
        faqs = FAQ.objects.filter(is_active=True)

        for faq in faqs:
            text = (faq.question_ar or "") + "\n" + (faq.question_fr or "")
            vec = model.encode(text, normalize_embeddings=True).tolist()
            faq.embedding = vec
            faq.save(update_fields=["embedding"])
            self.stdout.write(self.style.SUCCESS(f"Embedded FAQ {faq.id}"))
