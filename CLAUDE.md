# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

matteoscurati.dev is Matteo Scurati's personal portfolio and project showcase. It's not a product — it's a curated window into his work as a builder. Projects and content will change over time; the site structure is designed to accommodate that via content collections.

The tone is personal, opinionated, and technical — like a terminal you can read. Every change should serve the goal of presenting Matteo's work clearly and memorably. Don't turn it into a generic SaaS landing page.

Built with Astro v5 (static), Svelte 5 (interactivity), Tailwind CSS v4, deployed on Vercel.

## Commands

- `npm run dev` — dev server on localhost:4321
- `npm run build` — production build to ./dist/
- `npm run preview` — preview production build
- `npm run lint` — ESLint (Astro + TypeScript)
- `npm run check` — Astro type checking
- `npm run format` — Prettier (auto-runs on edit via hook)

## Conventions

- **Commits**: conventional commits (feat:, fix:, chore:, docs:, style:, refactor:)
- **Styling**: Tailwind v4 uses `@theme` directive in global.css (not tailwind.config.js). Custom color tokens are defined there.
- **Components**: Astro components for static content, Svelte (with `client:load` or `client:visible`) only when client-side interactivity is needed
- **Content**: uses Astro Content Collections with `glob()` loader in `src/content.config.ts`. Projects are Markdown in `src/content/projects/`, lab posts in `src/content/lab/`, identity data in `src/content/identity.json`
- **TypeScript**: strict mode (extends `astro/tsconfigs/strict`)

## Design System

- Dark-only theme with terminal/monospace aesthetic (JetBrains Mono)
- Brand color: terracotta `#c47a5a`, accent: cyan `#5eead4`
- Glass morphism cards via `.glass-card` utility class
- Sections use shell-like prompt headings (`$ ls`, `$ cat`)
- Status badges: live (green), beta (amber), wip (indigo), shipped (cyan), archived (muted)

## Gotchas

- Tailwind v4 syntax differs from v3 — no `theme.extend`, use `@theme` block in CSS
- Astro v5 content collections use the new `glob()` loader, not the legacy API
- Scroll animations use Intersection Observer with `.scroll-reveal` CSS class — respect `prefers-reduced-motion`
