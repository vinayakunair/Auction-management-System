#!/usr/bin/env python
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'auction_system.settings')
sys.path.append(os.path.dirname(__file__))
django.setup()

from accounts.models import CustomUser

# Unblock all admin users
admins = CustomUser.objects.filter(role='admin')
for admin in admins:
    if admin.is_blocked:
        admin.is_blocked = False
        admin.save()
        print(f"Unblocked admin: {admin.username}")
    else:
        print(f"Admin {admin.username} is already unblocked")

print("Admin unblocking script completed.")
