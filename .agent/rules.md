# Workspace Rules - Dra. Alessandra Legal Platform

This file contains general rules that apply to ALL work within this workspace, regardless of the specific task.

---

## Available Skills

This workspace has specialized skills that provide detailed instructions for specific domains. Skills are loaded automatically when relevant to your task:

### 1. PostgreSQL Database Manager
**Path**: `.agent/skills/db-manager/`  
**When to use**: Database schema operations, migrations, model changes  
**Purpose**: Prevents hallucinations in PostgreSQL table creation by enforcing schema validation

### 2. Phase 4 Visual Identity Enforcer
**Path**: `.agent/skills/phase4-identity/`  
**When to use**: Frontend development, UI changes, notifications, templates  
**Purpose**: Ensures sophisticated legal aesthetics (no emojis, Playfair Display typography, SVG icons)

### 3. Step-by-Step Verification Protocol
**Path**: `.agent/skills/step-verification/`  
**When to use**: ALL file modifications, debugging, error recovery  
**Purpose**: Anti-hallucination protocol that forces validation before execution

---

## Project Context

### Project Name
**Portal de Inteligência Jurídica da Dra. Alessandra Donadon**

### Tech Stack
- **Backend**: Django 5.x, Python 3.13
- **Database**: PostgreSQL (production via Railway), SQLite (development)
- **Frontend**: Django Templates, Vanilla CSS (no Tailwind unless explicitly requested)
- **Deployment**: Railway
- **Environment Management**: Virtual environment (`.venv`)

### Project Structure
```
alessandra antigravity/
├── src/                          # Main Django project
│   ├── core/                     # Project settings
│   ├── admin_portal/             # Custom admin interface
│   ├── apps/                     # Business logic apps
│   │   ├── clients/              # Client management
│   │   ├── legal_cases/          # Case tracking
│   │   ├── intake/               # Lead intake forms
│   │   ├── finance/              # Financial tracking
│   │   ├── observatory/          # Legal intelligence
│   │   └── portals/              # Client portal
│   └── in_brief/                 # Blog/articles system
├── .agent/                       # Skills and rules (THIS DIRECTORY)
├── scripts/                      # Utility scripts
├── media/                        # User uploads
├── requirements.txt              # Python dependencies
└── manage.py                     # Django management
```

---

## Naming Conventions

### Python/Django Code
- **Files**: `snake_case.py` (e.g., `legal_cases.py`)
- **Classes**: `PascalCase` (e.g., `LegalCase`, `ClientProfile`)
- **Functions/Methods**: `snake_case` (e.g., `calculate_lead_score`, `get_active_cases`)
- **Variables**: `snake_case` (e.g., `client_name`, `case_status`)
- **Constants**: `UPPER_SNAKE_CASE` (e.g., `MAX_UPLOAD_SIZE`, `DEFAULT_LEAD_SCORE`)

### Database (PostgreSQL)
- **Tables**: `snake_case` with app prefix (e.g., `in_brief_article`, `legal_cases_case`)
- **Columns**: `snake_case` (e.g., `created_at`, `is_published`, `lead_score`)
- **Foreign Keys**: `<model>_id` (e.g., `author_id`, `client_id`)

### Frontend (Templates/CSS)
- **Template Files**: `snake_case.html` (e.g., `case_detail.html`, `dashboard_index.html`)
- **CSS Classes**: `kebab-case` (e.g., `.card-header`, `.btn-primary`, `.notification-success`)
- **CSS Variables**: `--kebab-case` (e.g., `--color-primary`, `--font-size-lg`)
- **IDs**: `kebab-case` (e.g., `#login-form`, `#case-timeline`)

---

## Git Commit Conventions

Follow **Conventional Commits** format:

```
<type>(<scope>): <short description>

[optional body]

[optional footer]
```

### Types
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style/formatting (no logic change)
- `refactor`: Code restructuring (no feature/bug change)
- `perf`: Performance improvement
- `test`: Adding/updating tests
- `chore`: Maintenance tasks (dependencies, config)

### Scopes (optional)
- `db`: Database/models
- `admin`: Admin portal
- `portal`: Client portal
- `intake`: Lead intake system
- `cases`: Legal case management
- `in-brief`: Blog/articles
- `ui`: Frontend/templates

### Examples
```bash
feat(in-brief): add image field to Article model
fix(db): resolve ProgrammingError for missing column
docs(skills): create db-manager skill documentation
style(admin): enforce Playfair Display typography
refactor(cases): optimize lead scoring algorithm
```

---

## Profile Switching & Context Rot Prevention

### The Problem
Different user profiles or conversation sessions can create conflicting mental models, leading to **"context rot"** where the agent tries to reconcile incompatible patterns.

### The Solution
**ALL project-specific knowledge is stored in `.agent/skills/`** (workspace scope), NOT in global user settings. This ensures:
- Any profile opening this project loads the same rules
- No conflicting patterns between conversations
- Consistent behavior across sessions

### Best Practice
If you notice conflicting information between this workspace's skills and previous conversations:
1. **Prioritize workspace skills** (they are the source of truth)
2. **Ignore global patterns** if they conflict
3. **Ask the user** if genuinely uncertain

---

## Django Management Commands

### Common Commands (Always use from project root)
```bash
# Activate virtual environment first
source .venv/bin/activate

# Development server
python manage.py runserver

# Migrations
python manage.py makemigrations
python manage.py migrate
python manage.py showmigrations

# Database inspection
python manage.py inspectdb [table_name]
python manage.py dbshell

# Create superuser
python manage.py createsuperuser

# Validation
python manage.py check
python manage.py check --deploy

# Tests
python manage.py test
pytest  # If using pytest
```

---

## Environment Variables

### Required for Production (Railway)
```bash
SECRET_KEY=<django-secret-key>
DATABASE_URL=<postgresql-url>
ENCRYPTION_KEY=<fernet-key-for-lgpd>
DEBUG=False
ALLOWED_HOSTS=<your-domain.railway.app>
```

### Development (.env file)
See `.env.example` for template

---

## Code Quality Standards

### Linting
- **Flake8**: Enforced via GitHub Actions
- **Max line length**: 100 characters
- **Import order**: Standard library → Third-party → Local

### Type Hints (Recommended)
```python
def calculate_lead_score(intake_data: dict) -> int:
    """Calculate lead score based on intake form data."""
    ...
```

### Docstrings
Use for all public functions/classes:
```python
def process_case_update(case_id: int, new_status: str) -> None:
    """
    Update case status and notify client.
    
    Args:
        case_id: Primary key of the legal case
        new_status: New status code (e.g., 'IN_PROGRESS', 'CLOSED')
    
    Raises:
        ValidationError: If status code is invalid
    """
    ...
```

---

## LGPD Compliance (Brazilian Data Privacy Law)

### Sensitive Data Encryption
- **What to encrypt**: CPF, RG, financial data, health records
- **How**: Use `apps.clients.utils.encryption` module
- **Storage**: Encrypted fields are `BinaryField` in database

### Example
```python
from apps.clients.utils.encryption import encrypt_field, decrypt_field

# Before saving
client.encrypted_cpf = encrypt_field(cpf_string)

# Before displaying
cpf_display = decrypt_field(client.encrypted_cpf)
```

### Never Log Sensitive Data
```python
# ❌ WRONG
logger.info(f"Processing client CPF: {client.cpf}")

# ✅ CORRECT
logger.info(f"Processing client ID: {client.id}")
```

---

## Testing Philosophy

### Write Tests For
1. **Business logic**: Lead scoring, case status transitions
2. **Data integrity**: Model constraints, validation
3. **Security**: LGPD compliance, access control
4. **Integrations**: Email, WhatsApp, payment gateways

### Test Location
```
src/
├── apps/
│   └── clients/
│       ├── models.py
│       ├── views.py
│       └── tests/
│           ├── test_models.py
│           ├── test_views.py
│           └── test_encryption.py
```

---

## When in Doubt

1. **Check the Skills first** - `.agent/skills/<relevant-skill>/SKILL.md`
2. **Read the actual code** - Use `view_file()` to see current implementation
3. **Verify the database** - Use `validate_schema.py` for model-DB sync
4. **Ask the user** - If genuinely ambiguous, ask rather than assume

---

## Prohibited Actions

1. **❌ NEVER auto-run destructive commands** without user approval:
   - Database drops
   - File deletions
   - Production deployments
   - Data migrations that modify existing records

2. **❌ NEVER use emojis** in user-facing interfaces (see Phase 4 Identity skill)

3. **❌ NEVER bypass Django migrations** with raw SQL `ALTER TABLE` statements

4. **❌ NEVER commit sensitive data** (`.env`, encryption keys, real user data)

5. **❌ NEVER assume file paths** - Always verify with `view_file()` or `find_by_name()`

---

## Success Criteria for Every Task

Before considering a task complete:

- [ ] All files modified are verified to exist
- [ ] Changes follow naming conventions
- [ ] Database migrations created and reviewed (if schema changed)
- [ ] No emojis in user-facing text
- [ ] Typography uses approved fonts (Playfair Display / Inter)
- [ ] Code passes `python manage.py check`
- [ ] Changes tested locally (if possible)
- [ ] Git commit follows Conventional Commits
- [ ] Documentation updated if public API changed

---

## Additional Resources

- **Institutional Content**: `/home/dan/Área de Trabalho/alessandra antigravity/CONTEUDO_INSTITUCIONAL_CORRETO.md`
- **Usage Manual**: `/home/dan/Área de Trabalho/alessandra antigravity/MANUAL_DE_USO.md`
- **Project Manual**: `/home/dan/Área de Trabalho/alessandra antigravity/MANUAL_PROJETO.html`
- **Deployment Guide**: `/home/dan/Área de Trabalho/alessandra antigravity/RAILWAY_DEPLOY_GUIDE.md`
- **Quality Standards**: `/home/dan/Área de Trabalho/alessandra antigravity/QUALITY.md`
