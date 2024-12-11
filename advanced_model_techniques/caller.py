import os
from decimal import Decimal
from django.contrib.postgres.search import SearchVector

from main_app.models import Document

import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

results = Document.objects.filter(search_vector='django web framework')

for result in results:
    print(f"Title: {result.title}")
