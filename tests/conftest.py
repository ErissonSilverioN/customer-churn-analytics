import pytest
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'churn_api.settings')
django.setup()
