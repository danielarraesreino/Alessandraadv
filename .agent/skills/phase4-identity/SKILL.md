---
name: Phase 4 Visual Identity Enforcer
description: Guarantees sophisticated legal aesthetics by prohibiting emojis/clipart and enforcing Playfair Display typography, SVG minimalist icons, and institutional color palette.
---

# Phase 4 Visual Identity Enforcer

## Purpose
This skill ensures that **all user-facing interfaces project authority and sophistication** appropriate for a high-level legal practice. It eliminates amateur design choices and enforces the approved visual identity of **Dra. Alessandra Donadon's Legal Intelligence Platform**.

---

## Core Design Philosophy

### 🎯 Target Aesthetic
**"Sophisticated Legal Authority"** - The platform must convey:
- Professionalism and trustworthiness
- Timeless elegance (not trendy or playful)
- Attention to detail
- Premium quality service

### ❌ ABSOLUTELY PROHIBITED

#### 1. Emojis and Emoticons
**NEVER** use emojis in:
- User notifications
- Dashboard messages
- Email templates
- Error messages
- Success confirmations
- Admin portal
- Client portal

**❌ Examples to Avoid**:
```python
# WRONG!
messages.success(request, "✅ Lead captured successfully!")
messages.error(request, "❌ Invalid email format")
notification_text = "🎉 Your case has been updated!"
```

**✅ Correct Approach**:
```python
# Use text-only professional language
messages.success(request, "Lead captured successfully")
messages.error(request, "Invalid email format")
notification_text = "Your case status has been updated"
```

#### 2. Clip-Art and Generic Icons
- NO cartoon-style illustrations
- NO colorful generic icon packs (Font Awesome colorized, etc.)
- NO stock photo clichés (handshake photos, gavels, scales of justice)

#### 3. Overly Casual Language
- Avoid: "Hey!", "Awesome!", "Cool!", "Yay!"
- Use: Professional, direct, respectful language

---

## Typography System

### Primary Font: Playfair Display (Serif)
**Usage**: Headlines, section titles, hero text

```css
font-family: 'Playfair Display', Georgia, serif;
font-weight: 600; /* SemiBold for titles */
font-weight: 700; /* Bold for main hero */
letter-spacing: -0.02em; /* Slight tightening for elegance */
```

**Where to Apply**:
- Hero section headline
- Section headers (`<h1>`, `<h2>`)
- Card titles in "Áreas de Atuação"
- Article titles
- Dashboard section headers

### Secondary Font: Inter (Sans-Serif)
**Usage**: Body text, UI elements, navigation

```css
font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
font-weight: 400; /* Regular for body */
font-weight: 500; /* Medium for emphasis */
font-weight: 600; /* SemiBold for buttons */
line-height: 1.6; /* Improved readability */
```

**Where to Apply**:
- Paragraph text
- Form labels and inputs
- Navigation menu
- Buttons
- Tables and data displays
- Footer content

### Font Loading
```html
<!-- Add to base.html <head> -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Playfair+Display:wght@600;700&display=swap" rel="stylesheet">
```

---

## Color Palette

### Primary Colors (from CONTEUDO_INSTITUCIONAL_CORRETO.md)
```css
:root {
  /* Primary - Deep Professional Blue */
  --color-primary: #1A1A1A;          /* Near-black for authority */
  --color-primary-light: #2D2D2D;    /* Lighter shade for hover */
  --color-primary-dark: #000000;     /* Pure black for emphasis */
  
  /* Accent - Sophisticated Gold */
  --color-accent: #B8860B;           /* Dark goldenrod - legal authority */
  --color-accent-light: #DAA520;     /* Lighter gold for highlights */
  
  /* Neutrals */
  --color-gray-50: #FAFAFA;
  --color-gray-100: #F5F5F5;
  --color-gray-200: #EEEEEE;
  --color-gray-300: #E0E0E0;
  --color-gray-700: #616161;
  --color-gray-900: #212121;
  
  /* Semantic Colors */
  --color-success: #2E7D32;          /* Dark green - professional */
  --color-warning: #F57C00;          /* Dark orange */
  --color-error: #C62828;            /* Dark red */
  --color-info: #1565C0;             /* Dark blue */
}
```

### Color Usage Guidelines
- **Backgrounds**: Use `--color-gray-50` or `--color-gray-100` for subtle sections
- **Text**: Primary text should be `--color-gray-900` or `--color-primary`
- **Accents**: Use `--color-accent` sparingly for CTAs and important highlights
- **Never**: Bright neon colors, gradients with more than 2 colors

---

## Icon System

### SVG Minimalist Icons Only
All icons must be:
- **Stroke-based** (not filled)
- **Stroke width**: `2px` consistently
- **Color**: `#1A1A1A` (or inherit from parent)
- **Size**: Standardized (24×24px or 32×32px)

### Icon Library Location
```
.agent/skills/phase4-identity/references/svg_icon_library/
├── check-circle.svg
├── alert-triangle.svg
├── document.svg
├── calendar.svg
├── user.svg
└── ... (more as needed)
```

### Icon Template
```svg
<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <!-- Icon paths here -->
</svg>
```

**Example: Success Checkmark**
```svg
<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#1A1A1A" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
  <polyline points="22 4 12 14.01 9 11.01"></polyline>
</svg>
```

### Recommended Icon Source
- **Lucide Icons**: https://lucide.dev (minimalist, professional)
- **Heroicons**: https://heroicons.com (stroke-based)
- **Avoid**: Font Awesome (too common), Material Icons (too colorful)

---

## UI Component Standards

### Buttons
```css
.btn-primary {
  background-color: var(--color-primary);
  color: white;
  font-family: 'Inter', sans-serif;
  font-weight: 600;
  padding: 12px 24px;
  border-radius: 4px; /* Subtle rounding, not pill-shaped */
  border: none;
  transition: background-color 0.2s ease;
}

.btn-primary:hover {
  background-color: var(--color-primary-light);
}

.btn-accent {
  background-color: var(--color-accent);
  color: white;
}
```

### Cards
```css
.card {
  background: white;
  border: 1px solid var(--color-gray-200);
  border-radius: 8px;
  padding: 24px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05); /* Subtle shadow */
  transition: box-shadow 0.2s ease;
}

.card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}
```

### Forms
```css
.form-input {
  font-family: 'Inter', sans-serif;
  font-size: 16px;
  padding: 12px 16px;
  border: 1px solid var(--color-gray-300);
  border-radius: 4px;
  width: 100%;
}

.form-input:focus {
  outline: none;
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px rgba(26, 26, 26, 0.1);
}

.form-label {
  font-family: 'Inter', sans-serif;
  font-weight: 500;
  font-size: 14px;
  color: var(--color-gray-700);
  margin-bottom: 8px;
  display: block;
}
```

---

## Notification System

### Toast Messages (Django Messages Framework)
**Template**: `src/templates/includes/messages.html`

```html
{% if messages %}
<div class="notifications-container">
  {% for message in messages %}
  <div class="notification notification-{{ message.tags }}">
    <!-- SVG icon based on message type -->
    {% if message.tags == 'success' %}
      <svg class="notification-icon" ...><!-- check-circle --></svg>
    {% elif message.tags == 'error' %}
      <svg class="notification-icon" ...><!-- alert-circle --></svg>
    {% elif message.tags == 'warning' %}
      <svg class="notification-icon" ...><!-- alert-triangle --></svg>
    {% else %}
      <svg class="notification-icon" ...><!-- info --></svg>
    {% endif %}
    
    <span class="notification-text">{{ message }}</span>
  </div>
  {% endfor %}
</div>
{% endif %}
```

**CSS**:
```css
.notification {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px 20px;
  border-radius: 8px;
  font-family: 'Inter', sans-serif;
  font-size: 14px;
  margin-bottom: 12px;
}

.notification-success {
  background-color: #E8F5E9; /* Light green */
  border-left: 4px solid var(--color-success);
  color: var(--color-success);
}

.notification-icon {
  width: 20px;
  height: 20px;
  flex-shrink: 0;
}
```

---

## Dashboard Aesthetics

### Metrics Cards
```html
<div class="metric-card">
  <div class="metric-icon">
    <svg><!-- Minimalist icon --></svg>
  </div>
  <div class="metric-value">{{ value }}</div>
  <div class="metric-label">{{ label }}</div>
</div>
```

**NO** colorful background circles around icons
**YES** Subtle monochrome icons with clean typography

---

## Reference Materials

### Design Tokens
See `references/design_tokens.css` for complete CSS variable system

### Icon Library
Browse `references/svg_icon_library/` for approved icons

### Institutional Content
Refer to `/home/dan/Área de Trabalho/alessandra antigravity/CONTEUDO_INSTITUCIONAL_CORRETO.md` for:
- Official color palette
- Typography choices
- Tone of voice guidelines

---

## Validation Checklist

Before merging any frontend changes:

- [ ] NO emojis in user-facing text
- [ ] Typography uses Playfair Display (titles) and Inter (body)
- [ ] Icons are SVG stroke-based with 2px width
- [ ] Colors follow the approved palette (no random hex codes)
- [ ] Buttons have subtle border-radius (4-8px, not pill-shaped)
- [ ] No clip-art or stock photo clichés
- [ ] Language is professional and direct
- [ ] Shadows are subtle (max `rgba(0,0,0,0.1)`)
- [ ] Contrast ratios meet WCAG AA standards
- [ ] Design feels timeless, not trendy

---

## Anti-Patterns to Avoid

### ❌ Anti-Pattern 1: Emoji Overload
```html
<!-- WRONG! -->
<h1>🏛️ Bem-vindo ao Portal! 🎉</h1>
<p>Estamos felizes em tê-lo aqui! 😊</p>
```

**Fix**: Remove all emojis, use professional language

### ❌ Anti-Pattern 2: Comic Sans or Similar Fonts
```css
/* ABSOLUTELY FORBIDDEN */
font-family: 'Comic Sans MS', cursive;
font-family: 'Papyrus', fantasy;
```

### ❌ Anti-Pattern 3: Bright Neon Colors
```css
/* NEVER */
background: #FF00FF; /* Magenta */
color: #00FF00; /* Lime green */
```

### ❌ Anti-Pattern 4: Excessive Animations
```css
/* Too much! */
.element {
  animation: bounce 0.5s infinite, rotate 1s linear infinite, pulse 2s ease-in-out infinite;
}
```

**Use**: Subtle transitions (`0.2s ease`) for hover states only

---

## When This Skill Activates
This skill loads when the task involves:
- Creating or modifying templates (HTML)
- Writing CSS or styling
- Implementing notifications or messages
- Designing dashboard components
- Creating email templates
- Working with the admin portal UI
- Client portal interface
- Any user-facing visual element
