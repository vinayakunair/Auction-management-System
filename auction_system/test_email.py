import os
import sys

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(__file__))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'auction_system.settings')

try:
    import django
    django.setup()
    print("Django setup successful")
except Exception as e:
    print(f"Django setup failed: {e}")
    sys.exit(1)

from django.core.mail import send_mail
from django.conf import settings

print("Email settings:")
print(f"EMAIL_BACKEND: {settings.EMAIL_BACKEND}")
print(f"EMAIL_HOST: {settings.EMAIL_HOST}")
print(f"EMAIL_PORT: {settings.EMAIL_PORT}")
print(f"EMAIL_USE_TLS: {settings.EMAIL_USE_TLS}")
print(f"EMAIL_HOST_USER: {settings.EMAIL_HOST_USER}")

try:
    result = send_mail(
        'Test Subject',
        'Test message from Auction Management System',
        'vinayakunair@gmail.com',
        ['vinayakunair@gmail.com'],  # sending to self for testing
        fail_silently=False,
    )
    print(f"Email sent successfully, result: {result}")
except Exception as e:
    print(f"Email sending failed: {e}")
    import traceback
    traceback.print_exc()
