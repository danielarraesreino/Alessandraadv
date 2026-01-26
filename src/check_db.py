import os
import sys
import django
from django.db import connection

# Add src to path
sys.path.append(os.getcwd())

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

def check():
    print("Checking in_brief_article columns...")
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT column_name FROM information_schema.columns WHERE table_name = 'in_brief_article'")
            columns = [row[0] for row in cursor.fetchall()]
            for col in columns:
                print(f"- {col}")
            
            if 'image' in columns:
                print("\n✅ Column 'image' EXISTS in production.")
            else:
                print("\n❌ Column 'image' is MISSING in production.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check()
