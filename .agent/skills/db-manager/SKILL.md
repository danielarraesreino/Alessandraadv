---
name: PostgreSQL Database Manager
description: Prevents hallucinations in database schema operations by enforcing ground-truth validation before any DDL statements. Forces consultation of actual Django models and PostgreSQL schema.
---

# PostgreSQL Database Manager Skill

## Purpose
This skill **eliminates hallucinations** in PostgreSQL table creation and modifications by implementing a strict "ground truth" validation protocol. You MUST consult the actual database schema and Django models before suggesting any SQL DDL operations.

## Critical Rules

### 🚫 PROHIBITED ACTIONS
- **NEVER** invent column names that don't exist in Django `models.py`
- **NEVER** suggest `CREATE TABLE` or `ALTER TABLE` without first running schema inspection
- **NEVER** assume a column exists - always verify first
- **NEVER** use `camelCase` for PostgreSQL identifiers

### ✅ MANDATORY ACTIONS BEFORE ANY DDL

#### 1. Inspect Django Models First
```python
# Always read the actual models.py file
view_file("/home/dan/Área de Trabalho/alessandra antigravity/src/<app>/models.py")
```

#### 2. Check Current Database Schema
If MCP tools are available, use them:
```python
# List all tables
list_tables()

# Describe specific table
describe_table("table_name")
```

If MCP is not available, use Django management commands:
```bash
python manage.py inspectdb <table_name>
python manage.py sqlmigrate <app> <migration_number>
```

#### 3. Cross-Reference Models vs Database
Run the validation script:
```bash
python .agent/skills/db-manager/scripts/validate_schema.py
```

### Naming Conventions

#### PostgreSQL Standard (ENFORCED)
- **Tables**: `snake_case` (e.g., `in_brief_article`)
- **Columns**: `snake_case` (e.g., `published_at`, `is_active`)
- **Foreign Keys**: `<model>_id` (e.g., `author_id`, `category_id`)
- **Junction Tables**: `<app>_<model1>_<model2>` (e.g., `in_brief_article_categories`)

#### Django Field Mapping to PostgreSQL Types
| Django Field | PostgreSQL Type |
|--------------|-----------------|
| `CharField(max_length=N)` | `VARCHAR(N)` |
| `TextField` | `TEXT` |
| `IntegerField` | `INTEGER` |
| `ForeignKey` | `INTEGER REFERENCES ...` |
| `DateTimeField` | `TIMESTAMP WITH TIME ZONE` |
| `BooleanField` | `BOOLEAN` |
| `ImageField` | `VARCHAR(100)` |
| `SlugField` | `VARCHAR(50)` |

## Relationship Patterns

### 1:1 Relationship (One-to-One)
**Problem**: Each `Article` should have exactly ONE `ArticleImage`.

**❌ WRONG - Common Hallucination**:
```sql
CREATE TABLE article_images (
    id SERIAL PRIMARY KEY,
    article_id INTEGER REFERENCES articles(id),
    image VARCHAR(200)
);
-- Problem: Allows multiple images per article!
```

**✅ CORRECT - Option 1: UNIQUE Constraint**:
```sql
CREATE TABLE article_images (
    id SERIAL PRIMARY KEY,
    article_id INTEGER UNIQUE REFERENCES articles(id),
    image VARCHAR(200) NOT NULL
);
```

**✅ CORRECT - Option 2: Primary Key Sharing (Most Robust)**:
```sql
CREATE TABLE article_images (
    article_id INTEGER PRIMARY KEY REFERENCES articles(id) ON DELETE CASCADE,
    image VARCHAR(200) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

### 1:N Relationship (One-to-Many)
Example: One `Author` has many `Articles`
```sql
CREATE TABLE articles (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200),
    author_id INTEGER REFERENCES authors(id) ON DELETE CASCADE
);
-- No UNIQUE constraint on author_id - allows multiple articles per author
```

### N:N Relationship (Many-to-Many)
Example: `Articles` ↔ `Categories` (Django's ManyToManyField)
```sql
-- Django automatically creates this junction table:
CREATE TABLE in_brief_article_categories (
    id SERIAL PRIMARY KEY,
    article_id INTEGER REFERENCES in_brief_article(id) ON DELETE CASCADE,
    category_id INTEGER REFERENCES in_brief_category(id) ON DELETE CASCADE,
    UNIQUE(article_id, category_id)  -- Prevent duplicate associations
);
```

## Validation Protocol

### Before Creating Migration
1. **Read the Django model** - Confirm field names and types
2. **Check existing schema** - Ensure no conflicts with existing tables
3. **Verify relationships** - Ensure integrity constraints match business logic
4. **Run validation script** - Cross-check models vs actual database
5. **Only then** create the migration with `python manage.py makemigrations`

### After Creating Migration
1. **Review the generated SQL** - Run `python manage.py sqlmigrate <app> <number>`
2. **Verify column names** - Must match `snake_case` convention
3. **Check constraints** - Ensure foreign keys have proper ON DELETE behavior
4. **Test on development** - Run migration locally before production

## Common Hallucination Scenarios

### Scenario 1: Inventing Column Names
**User Request**: "Add an image to each article"

**❌ Hallucinated Response**:
```python
# models.py
class Article(models.Model):
    title = models.CharField(max_length=200)
    # Agent hallucinates these don't exist:
    thumbnail = models.ImageField(upload_to='thumbs/')  # WRONG!
    header_image = models.URLField()  # WRONG!
```

**✅ Grounded Response**:
```python
# FIRST: Read src/in_brief/domain/models.py
# FOUND: image = models.ImageField(upload_to='articles/', null=True, blank=True)
# The field ALREADY EXISTS! No need to create it.
```

### Scenario 2: Wrong Relationship Cardinality
**User Request**: "Ensure each post has exactly one featured image"

**❌ Hallucinated Response**:
```python
class FeaturedImage(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    # Problem: ForeignKey allows MULTIPLE images per post!
```

**✅ Grounded Response**:
```python
class FeaturedImage(models.Model):
    post = models.OneToOneField('Post', on_delete=models.CASCADE, primary_key=True)
    # Enforces exactly ONE image per post
```

## Reference Files

- **Relationship Patterns**: See `references/relationship_patterns.md` for detailed SQL templates
- **Schema Validation**: Run `scripts/validate_schema.py` to cross-check models vs database
- **Django ORM**: Always prefer Django ORM over raw SQL unless performance-critical

## Integration with Project

### Applicable Models
This skill applies to ALL Django apps in the project:
- `src/in_brief/domain/models.py` - Article, Category
- `src/apps/clients/models.py` - Client data
- `src/apps/legal_cases/models.py` - Case management
- `src/apps/intake/models.py` - Lead intake
- `src/apps/finance/models.py` - Financial tracking
- `src/apps/observatory/models.py` - Legal intelligence
- `src/apps/portals/models.py` - Client portal

### When This Skill Activates
This skill loads when the task involves:
- Creating new Django models
- Modifying existing models
- Creating database migrations
- Troubleshooting `ProgrammingError` (column does not exist)
- Schema synchronization issues
- PostgreSQL operations

## Final Checklist Before Any DDL Operation

- [ ] Read the actual `models.py` file in the affected app
- [ ] Inspect current database schema (MCP or `inspectdb`)
- [ ] Verify field names match exactly (case-sensitive)
- [ ] Confirm relationship cardinality (1:1, 1:N, N:N)
- [ ] Check naming follows `snake_case` convention
- [ ] Run `validate_schema.py` if available
- [ ] Generate migration with `makemigrations`
- [ ] Review SQL with `sqlmigrate`
- [ ] Test locally before production deployment
