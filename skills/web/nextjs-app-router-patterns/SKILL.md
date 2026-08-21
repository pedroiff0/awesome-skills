---
name: nextjs-app-router-patterns
description: "Architect and implement modern Next.js App Router applications with Server Components (RSC), Server Actions, Parallel/Intercepting Routes, and Streaming SSR."
version: 1.0.0
author: Vercel / Next.js Community
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [nextjs, react, app-router, server-components, web-dev]
    related_skills: [web, frontend-visual-verification]
---

# Next.js App Router Architecture & Patterns

Best practices for structuring modern full-stack web applications using React Server Components and Next.js App Router.

## Key Principles

1. **Default to Server Components**: Keep data fetching on the server; only mark components with client directive when browser APIs, event listeners, or hooks are needed.
2. **Colocation of Route Segments**: Structure routes using folder hierarchies with `page.tsx`, `layout.tsx`, `loading.tsx`, and `error.tsx`.
3. **Mutations via Server Actions**: Use server action functions for forms and state mutations with `revalidatePath` and `revalidateTag`.
