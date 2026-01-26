from django.db import migrations, connection

def add_image_column(apps, schema_editor):
    table_name = 'in_brief_article'
    column_name = 'image'
    
    with connection.cursor() as cursor:
        if connection.vendor == 'postgresql':
            # PostgreSQL supports IF NOT EXISTS
            cursor.execute(f"ALTER TABLE {table_name} ADD COLUMN IF NOT EXISTS {column_name} varchar(100) NULL;")
        elif connection.vendor == 'sqlite':
            # SQLite does not support IF NOT EXISTS for ADD COLUMN, so we check first
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = [info[1] for info in cursor.fetchall()]
            if column_name not in columns:
                cursor.execute(f"ALTER TABLE {table_name} ADD COLUMN {column_name} varchar(100) NULL;")
        else:
            # Fallback for other DBs (e.g. valid standard SQL if supported, or pass)
            pass

class Migration(migrations.Migration):

    dependencies = [
        ('in_brief', '0003_article_image'),
    ]

    operations = [
        migrations.RunPython(add_image_column, reverse_code=migrations.RunPython.noop),
    ]
