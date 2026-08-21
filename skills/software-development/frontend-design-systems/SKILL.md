---
name: frontend-design-systems
description: "Architect and build production-grade web interfaces with modern design systems: Tailwind CSS v4, Shadcn UI primitives, Radix UI, dark mode tokens, and accessible WCAG AA components."
version: 1.0.0
author: Anthropic / skills.sh Community
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [frontend, design-systems, tailwind, shadcn, react, ui-ux]
    related_skills: [nextjs-app-router-patterns, frontend-visual-verification]
---

# Frontend Design Systems & UI Architecture

> **Attribution**: Originating from Anthropic & the skills.sh open ecosystem. Maintained in canonical SKILL.md format.

This skill guides the construction of modern, accessible, responsive frontend applications utilizing design tokens, component primitives, and Tailwind CSS.

---

## Key Guidelines

1. **Token Hierarchy**: Separate global design tokens (colors, spacing, typography) from component-specific styles.
2. **Accessible Primitives**: Use headless accessible primitives (Radix UI, React Aria) for complex interactions like dialogs, dropdowns, and comboboxes.
3. **Responsive by Default**: Mobile-first breakpoints (`sm`, `md`, `lg`, `xl`) with dark mode class strategy (`class="dark"`).
