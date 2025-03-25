import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ec.settings')
django.setup()

from django.contrib.sites.models import Site

# Update site with ID 1 or create it if it doesn't exist
Site.objects.update_or_create(
    id=1,
    defaults={
        'domain': 'localhost:8000',
        'name': 'localhost'
    }
)

print("Site created/updated successfully!") 