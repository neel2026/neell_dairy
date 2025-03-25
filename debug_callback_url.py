import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ec.settings')
django.setup()

from django.urls import reverse
from django.contrib.sites.models import Site

site = Site.objects.get_current()
callback_url = f"http://{site.domain}{reverse('socialaccount_login_callback', args=['google'])}"

print("=== EXACT CALLBACK URL ===")
print(callback_url)
print("=== ADD THIS URL TO GOOGLE CLOUD CONSOLE ===")
print("Also try these alternative formats:")
print(f"http://{site.domain}{reverse('socialaccount_login_callback', args=['google'])}/")
print(f"http://localhost:8000/accounts/google/login/callback/")
print(f"http://127.0.0.1:8000/accounts/google/login/callback/") 