import os
import sys
import django

# Add src to path
sys.path.append(os.path.join(os.getcwd(), 'src'))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model

def setup_support():
    print("Setting up Technical Support...")
    
    # 1. Create Group
    group, created = Group.objects.get_or_create(name='Technical_Support')
    if created:
        print("- Group 'Technical_Support' created.")
    else:
        print("- Group 'Technical_Support' already exists.")
    
    # 2. Add 'Daniel' to Group
    User = get_user_model()
    try:
        user = User.objects.get(username='daniel')
        user.groups.add(group)
        user.is_staff = True # Ensure staff access
        user.save()
        print(f"- User 'daniel' assigned to Technical_Support and granted staff access.")
    except User.DoesNotExist:
        print("- WARNING: User 'daniel' not found. Please create it first.")

if __name__ == "__main__":
    setup_support()
