# Agent Skills & Rules - Dra. Alessandra Legal Platform

This directory contains **Agent Skills** and **Workspace Rules** for the Google Antigravity IDE (version 1.15.6+). These skills implement anti-hallucination protocols and enforce visual identity standards.

---

## 📁 Directory Structure

```
.agent/
├── README.md                           # This file
├── rules.md                            # Workspace-wide rules (always active)
└── skills/                             # Modular skills (Progressive Disclosure)
    ├── db-manager/                     # PostgreSQL integrity & anti-hallucination
    │   ├── SKILL.md                    # Main skill instructions
    │   ├── scripts/
    │   │   └── validate_schema.py      # Django ↔ PostgreSQL validator
    │   └── references/
    │       └── relationship_patterns.md
    ├── phase4-identity/                # Visual identity enforcement
    │   ├── SKILL.md
    │   └── references/
    │       ├── design_tokens.css
    │       └── svg_icon_library/       # Minimalist SVG icons
    └── step-verification/              # 5-stage verification protocol
        └── SKILL.md
```

---

## 🎯 Purpose

### Problem Solved
Before these skills:
- ❌ Hallucinated PostgreSQL column names (e.g., inventing `thumbnail` when `image` exists)
- ❌ Created migrations for non-existent fields
- ❌ Used emojis in professional legal interfaces
- ❌ Inconsistent typography and design
- ❌ "Context rot" from profile switching

### Solution Implemented
After these skills:
- ✅ **Ground Truth Validation**: Always verifies Django models before DDL
- ✅ **Schema Integrity**: Automated validation script
- ✅ **Professional Aesthetics**: No emojis, consistent typography (Playfair Display + Inter)
- ✅ **Systematic Verification**: 5-stage protocol prevents hallucination accumulation
- ✅ **Workspace Scope**: Consistent behavior across user profiles

---

## 🛠️ Available Skills

### 1. **PostgreSQL Database Manager** (`db-manager/`)
**Activates when**: Database operations, migrations, model changes

**Prevents**:
- Inventing column names not in `models.py`
- Wrong relationship cardinality (1:1 vs 1:N)
- `camelCase` in PostgreSQL identifiers

**Enforces**:
- Schema validation before DDL
- `snake_case` naming
- Proper foreign key constraints

**Usage**:
```bash
# Validate schema consistency
python .agent/skills/db-manager/scripts/validate_schema.py
```

---

### 2. **Phase 4 Visual Identity Enforcer** (`phase4-identity/`)
**Activates when**: Frontend changes, templates, CSS, notifications

**Prohibits**:
- ❌ Emojis in user-facing text
- ❌ Clip-art or cartoon illustrations
- ❌ Comic Sans or similar fonts
- ❌ Bright neon colors

**Enforces**:
- ✅ Playfair Display (headlines) + Inter (body)
- ✅ Professional color palette (#1A1A1A, #B8860B)
- ✅ Minimalist SVG icons (2px stroke)
- ✅ Subtle shadows and transitions

**Resources**:
- Design tokens: `phase4-identity/references/design_tokens.css`
- Icon library: `phase4-identity/references/svg_icon_library/`

---

### 3. **Step-by-Step Verification Protocol** (`step-verification/`)
**Activates when**: Any file modification, debugging, error recovery

**5-Stage Protocol**:
1. **File Existence Check**: Verify file exists before modifying
2. **Content Validation**: Read current content exactly
3. **Dependency Check**: Verify imports, migrations, packages
4. **Execution**: Only after 1-3 pass
5. **Post-Validation**: Confirm change worked

**Prevents**:
- Assumption cascade errors
- "File not found" loops
- Hallucination accumulation

---

## 📋 Workspace Rules (`rules.md`)

Always-active rules covering:
- 🏗️ Project structure & tech stack
- 📝 Naming conventions (Python, PostgreSQL, CSS)
- 📦 Git commit format (Conventional Commits)
- 🔒 LGPD compliance
- 🚫 Prohibited actions
- ✅ Success criteria

---

## 🚀 Quick Start

### For Database Changes

1. **Before any migration**:
   ```bash
   view_file("src/<app>/models.py")  # Read actual model
   python .agent/skills/db-manager/scripts/validate_schema.py
   ```

2. **After migration**:
   ```bash
   python manage.py migrate
   python .agent/skills/db-manager/scripts/validate_schema.py
   ```

### For Frontend Changes

1. **Check design tokens**:
   ```bash
   view_file(".agent/skills/phase4-identity/references/design_tokens.css")
   ```

2. **Use approved icons**:
   ```bash
   ls .agent/skills/phase4-identity/references/svg_icon_library/
   ```

3. **Validate**: NO emojis, Playfair Display + Inter typography

---

## 📊 Validation

### YAML Frontmatter Check
```bash
python3 -c "import yaml; [yaml.safe_load(open(f).read().split('---')[1]) for f in ['.agent/skills/db-manager/SKILL.md', '.agent/skills/phase4-identity/SKILL.md', '.agent/skills/step-verification/SKILL.md']]; print('✅ All valid')"
```

**Result**: ✅ All YAML frontmatter is valid

### Schema Validation
```bash
cd "/home/dan/Área de Trabalho/alessandra antigravity"
source .venv/bin/activate
python .agent/skills/db-manager/scripts/validate_schema.py
```

---

## 🔄 Progressive Disclosure

Skills use **Progressive Disclosure** pattern from Antigravity 1.15.6:
- Skills load **only when relevant** to current task
- Prevents **context saturation**
- Activation based on YAML `description` keywords
- After task completion, skill unloads

**Activation Keywords**:
- `db-manager`: "PostgreSQL", "migration", "CREATE TABLE", "models.py"
- `phase4-identity`: "template", "CSS", "UI", "notification"
- `step-verification`: Always active (general protocol)

---

## 📚 Documentation

- **Walkthrough**: See `/home/dan/.gemini/antigravity/brain/852f54ee-4968-4d55-81e4-705dc6febfc3/walkthrough.md`
- **Implementation Plan**: See `/home/dan/.gemini/antigravity/brain/852f54ee-4968-4d55-81e4-705dc6febfc3/implementation_plan.md`
- **Task Checklist**: See `/home/dan/.gemini/antigravity/brain/852f54ee-4968-4d55-81e4-705dc6febfc3/task.md`

---

## 🎨 Visual Identity Assets

### Typography
- **Titles**: Playfair Display (SemiBold 600, Bold 700)
- **Body**: Inter (Regular 400, Medium 500, SemiBold 600)

### Colors
- **Primary**: `#1A1A1A` (near-black)
- **Accent**: `#B8860B` (dark goldenrod)
- **Success**: `#2E7D32` (dark green)
- **Error**: `#C62828` (dark red)

### Icons (SVG, 2px stroke)
- `check-circle.svg` - Success
- `alert-triangle.svg` - Warning
- `alert-circle.svg` - Error
- `info-circle.svg` - Information
- `document.svg` - Files
- `user.svg` - User profiles

---

## ✅ Success Metrics

Skills are working when:
- ✅ Zero "column does not exist" errors
- ✅ Zero "file not found" retry loops
- ✅ No emojis in production interface
- ✅ Consistent typography across all pages
- ✅ Surgical, first-attempt code modifications
- ✅ No assumption-based hallucinations

---

## 🔗 References

- **Antigravity 1.15.6 Release**: January 23, 2026
- **Agent Skills Documentation**: Official Antigravity docs
- **Progressive Disclosure Pattern**: Context management best practice
- **Institutional Content**: `/home/dan/Área de Trabalho/alessandra antigravity/CONTEUDO_INSTITUCIONAL_CORRETO.md`

---

## 📝 Maintenance

### Adding New Icons
1. Download from [Lucide Icons](https://lucide.dev)
2. Ensure 2px stroke, 24×24px viewBox
3. Save to `phase4-identity/references/svg_icon_library/`

### Updating Skills
1. Modify `SKILL.md` with new rules
2. Test with relevant scenario
3. Update walkthrough documentation

### Schema Validation Issues
1. Run `validate_schema.py` to identify discrepancies
2. Create migration: `python manage.py makemigrations`
3. Review SQL: `python manage.py sqlmigrate <app> <number>`
4. Apply: `python manage.py migrate`
5. Re-validate: `python .agent/skills/db-manager/scripts/validate_schema.py`

---

**Status**: ✅ **PRODUCTION READY**  
**Last Updated**: 2026-01-24  
**Version**: 1.0.0
