---
name: Step-by-Step Verification Protocol
description: Anti-hallucination protocol that forces validation of file existence, content accuracy, and dependency consistency before executing any code modification.
---

# Step-by-Step Verification Protocol

## Purpose
This skill implements a **rigorous validation protocol** that prevents "hallucination accumulation" by forcing the agent to verify assumptions at each stage before proceeding. It acts as a safety net, ensuring that every action is grounded in actual file system state and codebase reality.

---

## The Hallucination Problem

### What is Hallucination Accumulation?
When an AI agent makes assumptions without verification, small errors compound:
1. **Assumption**: "The file probably exists at this path"
2. **Action**: Edit the file
3. **Result**: File not found error
4. **Compounding**: Next assumption based on faulty premise
5. **Cascade**: Multiple failed attempts, wasted time, user frustration

### Root Causes
- **Context Saturation**: Too much information, agent loses track of reality
- **Pattern Matching Gone Wrong**: Agent applies patterns from training data that don't match current project
- **Profile Switching**: Different conversations create conflicting mental models ("context rot")
- **Lazy Verification**: Skipping basic checks to save tokens/time

---

## The 5-Stage Verification Protocol

### Stage 1: File Existence Check
**Rule**: NEVER assume a file exists. Always check first.

```python
# Before modifying ANY file:
1. Use view_file() to confirm the file exists
2. If it doesn't exist, use find_by_name() to locate it
3. If still not found, ask the USER for clarification
```

**Example**:
```python
# ❌ WRONG - Assuming file location
replace_file_content(
    TargetFile="/home/dan/project/src/models.py",
    # ... rest of arguments
)

# ✅ CORRECT - Verify first
view_file("/home/dan/Área de Trabalho/alessandra antigravity/src/apps/clients/models.py")
# Only AFTER confirming existence, proceed with edit
```

---

### Stage 2: Content Validation
**Rule**: Read current content before suggesting modifications.

**Why**: Prevents inventing fields/functions that don't exist.

```python
# Protocol:
1. view_file() or view_code_item() to see current state
2. Identify EXACT line numbers and content to modify
3. Use TargetContent that EXACTLY matches existing code (including whitespace)
4. Verify StartLine and EndLine contain the target content
```

**Example - Django Model Edit**:
```python
# Step 1: Read the model
view_file("/home/dan/Área de Trabalho/alessandra antigravity/src/in_brief/domain/models.py")

# Step 2: Confirm field names
# Found: image = models.ImageField(upload_to='articles/', null=True, blank=True)
# NOT FOUND: thumbnail, header_image, featured_image

# Step 3: Only suggest changes based on ACTUAL fields
# ✅ "The image field already exists at line 20"
# ❌ "Let's add a thumbnail field" (hallucination - not requested)
```

---

### Stage 3: Dependency Check
**Rule**: Before modifying code, verify all dependencies are in place.

**Checks**:
1. **Imports**: Does the file import the necessary modules?
2. **Foreign Keys**: Do referenced models/tables exist?
3. **Migrations**: Are there pending migrations that affect this change?
4. **Environment**: Are required packages installed?

**Example - Adding a New Model Field**:
```python
# Before creating migration for new ImageField:

# Check 1: Is Pillow installed?
run_command("pip list | grep -i pillow", ...)

# Check 2: Is upload directory configured?
view_file("/home/dan/Área de Trabalho/alessandra antigravity/src/core/settings.py")
# Verify: MEDIA_ROOT and MEDIA_URL are set

# Check 3: Are there pending migrations?
run_command("python manage.py showmigrations --plan", ...)

# Only then: Create makemigrations
```

---

### Stage 4: Execution (Only After 1-3 Pass)
**Rule**: Execute the modification only after all validations succeed.

**Actions**:
- Use replace_file_content or multi_replace_file_content
- Use run_command for migrations/scripts
- Ensure TargetContent EXACTLY matches what was verified in Stage 2

**Safety Checks**:
- [ ] File path is absolute (not relative)
- [ ] TargetContent is exact match (copy-pasted from view_file output)
- [ ] StartLine and EndLine are correct
- [ ] AllowMultiple is set appropriately

---

### Stage 5: Post-Validation
**Rule**: After executing, verify the change had the expected effect.

**Actions**:
1. **Re-read the file** to confirm modification applied correctly
2. **Run syntax checks** (e.g., `python -m py_compile <file>`)
3. **Run tests** if applicable
4. **Check for new errors** in console/logs

**Example - After Model Migration**:
```python
# After running `python manage.py migrate`:

# Check 1: Migration applied successfully?
run_command("python manage.py showmigrations in_brief", ...)
# Expected: [X] 0001_initial (marked as applied)

# Check 2: Schema matches model?
run_command("python .agent/skills/db-manager/scripts/validate_schema.py", ...)

# Check 3: No errors in Django check?
run_command("python manage.py check", ...)
```

---

## Common Scenarios and Protocols

### Scenario 1: User Requests "Add an Image to Articles"

#### Wrong Approach (Hallucination-Prone)
```python
# ❌ Agent hallucinates:
"I'll add a featured_image field to the Article model"
# Problem: Didn't check if image field already exists!
```

#### Correct Approach (Verification Protocol)
```python
# Stage 1: Check file exists
view_file("/home/dan/Área de Trabalho/alessandra antigravity/src/in_brief/domain/models.py")

# Stage 2: Read content
# Found: line 20: image = models.ImageField(upload_to='articles/', null=True, blank=True)

# Stage 3: Verify dependencies
# - Pillow is installed (checked in requirements.txt)
# - MEDIA settings are configured

# Stage 4: Response to user
"The Article model already has an `image` field at line 20. 
Would you like to make any changes to this existing field, 
or did you mean something different?"
```

---

### Scenario 2: Database Migration Error

**Error**: `ProgrammingError: column in_brief_article.image does not exist`

#### Wrong Approach
```python
# ❌ Hallucination:
"Let's add the image column with ALTER TABLE"
# Problem: Bypasses Django migrations, creates inconsistency
```

#### Correct Approach
```python
# Stage 1: Verify model has the field
view_file("/home/dan/Área de Trabalho/alessandra antigravity/src/in_brief/domain/models.py")
# Confirmed: Line 20 has image field

# Stage 2: Check migration status
run_command("python manage.py showmigrations in_brief", ...)
# Result: Some migrations not applied

# Stage 3: Check database schema
run_command("python .agent/skills/db-manager/scripts/validate_schema.py", ...)
# Result: Discrepancy found - image column missing

# Stage 4: Solution
run_command("python manage.py migrate in_brief", ...)

# Stage 5: Post-validation
run_command("python .agent/skills/db-manager/scripts/validate_schema.py", ...)
# Expected: ✅ ALL MODELS SYNCHRONIZED WITH DATABASE
```

---

### Scenario 3: Adding New Functionality

**Request**: "Create a comment system for articles"

#### Verification Protocol
```python
# Stage 1: Check if comment model already exists
find_by_name(
    SearchDirectory="/home/dan/Área de Trabalho/alessandra antigravity/src",
    Pattern="*comment*.py"
)

# Stage 2: If not found, check dependencies
view_file("/home/dan/Área de Trabalho/alessandra antigravity/src/in_brief/domain/models.py")
# Verify: Article model exists, has primary key

# Stage 3: Design validation
# - Relationship: Article (1) → Comments (N)
# - Cascade behavior: ON DELETE CASCADE (comments deleted with article)
# - Required fields: author, text, created_at

# Stage 4: Create model
write_to_file(...)

# Stage 5: Verify
run_command("python manage.py makemigrations", ...)
run_command("python manage.py sqlmigrate in_brief 0002", ...)
# Review SQL: Ensure relationship is correct
```

---

## Integration with Other Skills

### With DB Manager Skill
Before any database operation:
1. **This Skill**: Verify file existence and content
2. **DB Manager Skill**: Validate schema and relationships
3. **This Skill**: Post-validation after migration

### With Phase 4 Identity Skill
Before any frontend change:
1. **This Skill**: Verify template file exists
2. **Phase 4 Identity**: Ensure design follows rules
3. **This Skill**: Validate output contains no emojis

---

## Validation Checklist Template

Use this checklist mentally before EVERY file modification:

```
Pre-Modification Checklist:
[ ] File existence confirmed via view_file()
[ ] Current content read and understood
[ ] Exact line numbers identified
[ ] All imports/dependencies verified
[ ] No pending migrations blocking this change
[ ] TargetContent is EXACT match (whitespace included)

Post-Modification Checklist:
[ ] File re-read to confirm change applied
[ ] Syntax check passed (if code file)
[ ] No new errors in logs/console
[ ] Related tests still pass (if applicable)
```

---

## When This Skill Activates

This skill should be active for ALL tasks, but especially:
- File modifications (any language)
- Database schema changes
- Dependency management
- Migration operations
- Debugging "file not found" or "field does not exist" errors
- Recovering from previous hallucinations

---

## Anti-Patterns to Avoid

### ❌ Anti-Pattern 1: Assumption Cascade
```python
# WRONG sequence:
1. Assume file is at /project/models.py
2. Edit fails - file not found
3. Assume it's at /app/models.py
4. Edit fails again
5. ... (multiple failed attempts)
```

**Fix**: Always verify with `view_file()` or `find_by_name()` FIRST.

### ❌ Anti-Pattern 2: Partial Verification
```python
# INSUFFICIENT:
view_file("/path/to/file.py")  # ✅ Good
# ... then immediately suggest changes WITHOUT reading the content
```

**Fix**: Read and UNDERSTAND the content before suggesting modifications.

### ❌ Anti-Pattern 3: Skip Post-Validation
```python
# DANGEROUS:
replace_file_content(...)
# ❌ Don't check if change actually worked
# Move on to next task
```

**Fix**: Always re-read or run checks after modification.

---

## Error Recovery Protocol

### When Hallucination Detected
If you realize you've made an assumption that proved false:

1. **STOP immediately** - Don't compound the error
2. **Acknowledge explicitly** - "I apologize, I assumed X but didn't verify"
3. **Reset to last known-good state** - Go back to verified facts
4. **Run full Stage 1-3 verification** - Before attempting again
5. **Document the lesson** - What assumption was wrong and why

**Example**:
```
"I apologize - I assumed the `thumbnail` field existed in the Article model
without verifying first. Let me check the actual model structure:

view_file("/home/dan/Área de Trabalho/alessandra antigravity/src/in_brief/domain/models.py")

I can see the model has an `image` field at line 20, not `thumbnail`.
Would you like me to work with this existing field, or add a new field?"
```

---

## Success Metrics

A verification protocol is working when:
- ✅ Zero "file not found" errors due to wrong paths
- ✅ Zero "column does not exist" errors due to hallucinated fields
- ✅ Modifications work on first attempt (no retry loops)
- ✅ User doesn't have to correct assumptions
- ✅ Changes are surgical and precise (no over-editing)

---

## Final Principle

> **"Trust, but Verify"**  
> Even if you're 99% confident, that 1% will waste more time than a quick verification check.
> Always verify. Always validate. Always confirm.
