#!/usr/bin/env python3
"""
Schema Validation Script - Cross-checks Django models against PostgreSQL schema
Prevents hallucinations by providing "ground truth" comparison
"""
import os
import sys
import django
from pathlib import Path

# Setup Django
project_root = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(project_root / 'src'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.db import connection
from django.apps import apps


def get_model_fields(model):
    """Extract field information from Django model"""
    fields = {}
    for field in model._meta.get_fields():
        if hasattr(field, 'column'):
            fields[field.column] = {
                'type': field.get_internal_type(),
                'null': field.null,
                'blank': field.blank,
                'max_length': getattr(field, 'max_length', None),
            }
    return fields


def get_db_columns(table_name):
    """Get actual columns from PostgreSQL"""
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT column_name, data_type, is_nullable, character_maximum_length
            FROM information_schema.columns
            WHERE table_name = %s
            ORDER BY ordinal_position;
        """, [table_name])
        columns = {}
        for row in cursor.fetchall():
            columns[row[0]] = {
                'db_type': row[1],
                'nullable': row[2] == 'YES',
                'max_length': row[3],
            }
        return columns


def validate_all_models():
    """Compare all Django models against database schema"""
    print("=" * 70)
    print("SCHEMA VALIDATION REPORT")
    print("=" * 70)
    print()
    
    discrepancies = []
    
    for model in apps.get_models():
        app_label = model._meta.app_label
        model_name = model._meta.model_name
        table_name = model._meta.db_table
        
        print(f"📋 {app_label}.{model_name} → {table_name}")
        
        # Check if table exists
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_name = %s
                );
            """, [table_name])
            table_exists = cursor.fetchone()[0]
        
        if not table_exists:
            print(f"   ⚠️  WARNING: Table '{table_name}' does not exist in database!")
            discrepancies.append(f"Missing table: {table_name}")
            print()
            continue
        
        # Compare fields
        model_fields = get_model_fields(model)
        db_columns = get_db_columns(table_name)
        
        # Check for missing columns in database
        for field_name in model_fields:
            if field_name not in db_columns:
                msg = f"   ❌ Column '{field_name}' defined in model but MISSING in database"
                print(msg)
                discrepancies.append(f"{table_name}.{field_name} - {msg}")
        
        # Check for extra columns in database
        for col_name in db_columns:
            if col_name not in model_fields and col_name != 'id':
                msg = f"   ⚠️  Column '{col_name}' exists in database but NOT in model"
                print(msg)
                discrepancies.append(f"{table_name}.{col_name} - {msg}")
        
        # Check matching columns
        matching = set(model_fields.keys()) & set(db_columns.keys())
        if matching:
            print(f"   ✅ {len(matching)} columns match")
        
        print()
    
    print("=" * 70)
    if discrepancies:
        print(f"🚨 FOUND {len(discrepancies)} DISCREPANCIES:")
        print()
        for disc in discrepancies:
            print(f"  • {disc}")
        print()
        print("⚠️  Run migrations to synchronize:")
        print("   python manage.py makemigrations")
        print("   python manage.py migrate")
        sys.exit(1)
    else:
        print("✅ ALL MODELS SYNCHRONIZED WITH DATABASE")
        print()
        sys.exit(0)


if __name__ == '__main__':
    validate_all_models()
