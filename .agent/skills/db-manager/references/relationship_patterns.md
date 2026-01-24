# PostgreSQL Relationship Patterns for Legal Domain

## Overview
This document provides SQL templates for common database relationships in the legal intelligence platform, ensuring proper integrity constraints.

---

## 1:1 Relationships (One-to-One)

### Use Case: Case → Lead Document
Each legal case has exactly ONE intake lead document.

#### Django Model
```python
class Case(models.Model):
    case_number = models.CharField(max_length=50, unique=True)
    client = models.ForeignKey('Client', on_delete=models.PROTECT)
    status = models.CharField(max_length=20)

class LeadDocument(models.Model):
    case = models.OneToOneField(
        'Case',
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='intake_document'
    )
    submitted_at = models.DateTimeField()
    pdf_file = models.FileField(upload_to='intake/')
```

#### Generated PostgreSQL
```sql
CREATE TABLE legal_cases_case (
    id SERIAL PRIMARY KEY,
    case_number VARCHAR(50) UNIQUE NOT NULL,
    client_id INTEGER REFERENCES clients_client(id) ON DELETE PROTECT,
    status VARCHAR(20)
);

CREATE TABLE legal_cases_leaddocument (
    case_id INTEGER PRIMARY KEY REFERENCES legal_cases_case(id) ON DELETE CASCADE,
    submitted_at TIMESTAMP WITH TIME ZONE NOT NULL,
    pdf_file VARCHAR(100)
);
```

**Key Point**: `case_id` is both PRIMARY KEY and FOREIGN KEY, enforcing 1:1.

---

## 1:N Relationships (One-to-Many)

### Use Case: Client → Multiple Cases
One client can have multiple legal cases.

#### Django Model
```python
class Client(models.Model):
    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    encrypted_cpf = models.BinaryField()  # LGPD compliance

class Case(models.Model):
    client = models.ForeignKey(
        'Client',
        on_delete=models.PROTECT,  # Prevent deletion if cases exist
        related_name='cases'
    )
    case_number = models.CharField(max_length=50)
    area_of_law = models.CharField(max_length=100)
```

#### Generated PostgreSQL
```sql
CREATE TABLE clients_client (
    id SERIAL PRIMARY KEY,
    full_name VARCHAR(200) NOT NULL,
    email VARCHAR(254) UNIQUE NOT NULL,
    phone VARCHAR(20),
    encrypted_cpf BYTEA
);

CREATE TABLE legal_cases_case (
    id SERIAL PRIMARY KEY,
    client_id INTEGER NOT NULL REFERENCES clients_client(id) ON DELETE PROTECT,
    case_number VARCHAR(50) UNIQUE NOT NULL,
    area_of_law VARCHAR(100)
);

-- Index for performance
CREATE INDEX idx_case_client ON legal_cases_case(client_id);
```

**Key Point**: NO UNIQUE constraint on `client_id` - allows multiple cases.

---

## N:N Relationships (Many-to-Many)

### Use Case: Articles ↔ Categories
One article can belong to multiple categories; one category can have multiple articles.

#### Django Model
```python
class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

class Article(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    categories = models.ManyToManyField(
        'Category',
        related_name='articles'
    )
```

#### Generated PostgreSQL
```sql
CREATE TABLE in_brief_category (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    slug VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE in_brief_article (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    slug VARCHAR(50) UNIQUE NOT NULL
);

-- Django auto-creates junction table
CREATE TABLE in_brief_article_categories (
    id SERIAL PRIMARY KEY,
    article_id INTEGER NOT NULL REFERENCES in_brief_article(id) ON DELETE CASCADE,
    category_id INTEGER NOT NULL REFERENCES in_brief_category(id) ON DELETE CASCADE,
    CONSTRAINT unique_article_category UNIQUE (article_id, category_id)
);

-- Indexes for performance
CREATE INDEX idx_article_categories_article ON in_brief_article_categories(article_id);
CREATE INDEX idx_article_categories_category ON in_brief_article_categories(category_id);
```

**Key Point**: Junction table with UNIQUE constraint prevents duplicate associations.

---

## Self-Referential Relationships

### Use Case: Case → Parent Case (Appeals)
A case can be an appeal of another case.

#### Django Model
```python
class Case(models.Model):
    case_number = models.CharField(max_length=50)
    parent_case = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='appeals'
    )
```

#### Generated PostgreSQL
```sql
CREATE TABLE legal_cases_case (
    id SERIAL PRIMARY KEY,
    case_number VARCHAR(50) NOT NULL,
    parent_case_id INTEGER REFERENCES legal_cases_case(id) ON DELETE SET NULL
);
```

---

## Polymorphic Relationships (Generic Foreign Keys)

### Use Case: Comments on Multiple Entity Types
Comments can be attached to cases, documents, or articles.

⚠️ **NOT RECOMMENDED**: Django's GenericForeignKey is not backed by database constraints.

#### Alternative: Explicit Foreign Keys with CHECK Constraint
```python
class Comment(models.Model):
    author = models.ForeignKey('User', on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Only ONE of these should be set
    case = models.ForeignKey('Case', null=True, blank=True, on_delete=models.CASCADE)
    document = models.ForeignKey('Document', null=True, blank=True, on_delete=models.CASCADE)
    article = models.ForeignKey('Article', null=True, blank=True, on_delete=models.CASCADE)
    
    class Meta:
        constraints = [
            models.CheckConstraint(
                check=(
                    models.Q(case__isnull=False, document__isnull=True, article__isnull=True) |
                    models.Q(case__isnull=True, document__isnull=False, article__isnull=True) |
                    models.Q(case__isnull=True, document__isnull=True, article__isnull=False)
                ),
                name='only_one_parent'
            )
        ]
```

---

## Cascade Behavior Reference

| ON DELETE | Behavior | Use When |
|-----------|----------|----------|
| `CASCADE` | Delete child records | Tight coupling (e.g., Case → Documents) |
| `PROTECT` | Prevent deletion if children exist | Business logic requires preservation |
| `SET_NULL` | Set FK to NULL | Optional relationships |
| `SET_DEFAULT` | Set FK to default value | Fallback to default entity |
| `DO_NOTHING` | No action (may violate integrity) | ⚠️ Avoid unless you know what you're doing |

### Recommendations for Legal Platform
- **Client ← Case**: `PROTECT` (cannot delete client with active cases)
- **Case ← Documents**: `CASCADE` (case and its documents are tightly coupled)
- **Article ← Comments**: `CASCADE` (delete comments when article is deleted)
- **User ← Audit Logs**: `SET_NULL` (preserve logs even if user deleted)

---

## Common Anti-Patterns to Avoid

### ❌ Anti-Pattern 1: Fake 1:1 with Multiple=True
```python
# WRONG! This allows multiple images per article
class ArticleImage(models.Model):
    article = models.ForeignKey('Article', on_delete=models.CASCADE)
```

**Fix**: Use `OneToOneField`

### ❌ Anti-Pattern 2: Missing Unique Constraint in Junction Table
```sql
-- WRONG! Allows duplicate article-category associations
CREATE TABLE article_categories (
    article_id INTEGER,
    category_id INTEGER
);
```

**Fix**: Add `UNIQUE(article_id, category_id)`

### ❌ Anti-Pattern 3: Nullable Foreign Keys Without Default
```python
# DANGEROUS! Can lead to orphaned records
class Document(models.Model):
    case = models.ForeignKey('Case', null=True, on_delete=models.CASCADE)
```

**Fix**: Either make it required (`null=False`) or use `SET_NULL` with proper handling

---

## Verification Checklist

Before deploying any relationship change:

- [ ] Relationship cardinality matches business logic (1:1, 1:N, N:N)
- [ ] Cascade behavior is appropriate for the use case
- [ ] Indexes are created for foreign key columns (Django does this automatically)
- [ ] UNIQUE constraints are in place where needed
- [ ] Field names follow `snake_case` convention
- [ ] Migration has been reviewed with `sqlmigrate`
- [ ] Changes tested on development database first
