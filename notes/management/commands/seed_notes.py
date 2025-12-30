from django.core.management.base import BaseCommand
from notes.models import Note
import random

# run: python manage.py seed_notes

WORDS = [
    "django",
    "api",
    "performance",
    "scalability",
    "database",
    "index",
    "query",
    "latency",
    "throughput",
    "search",
    "backend",
    "optimization",
]


class Command(BaseCommand):
    help = "Seed database with notes"

    def handle(self, *args, **options) -> str | None:
        notes = []

        for i in range(10_000):
            content = " ".join(random.choices(WORDS, k=120))

            notes.append(Note(title=f"Note {i}", content=content))

        Note.objects.bulk_create(notes)
        self.stdout.write("Inserted 10k notes")
