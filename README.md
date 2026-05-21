# matteoscurati.dev

> Personal portfolio and project showcase — a terminal you can read.

[![Live](https://img.shields.io/badge/live-matteoscurati.dev-c47a5a?style=flat-square)](https://matteoscurati.dev)
[![CI](https://github.com/matteoscurati/matteoscurati.dev/actions/workflows/ci.yml/badge.svg)](https://github.com/matteoscurati/matteoscurati.dev/actions/workflows/ci.yml)

Static site built with Astro v5, sprinkled with Svelte 5 for interactivity. Dark-only, JetBrains Mono everywhere, terracotta brand. Deployed on Vercel.

Not a product. A curated window into what I build.

## Stack

- **[Astro v5](https://astro.build)** — static generation, content collections
- **[Svelte 5](https://svelte.dev)** — only where interactivity is needed (`client:visible`)
- **[Tailwind CSS v4](https://tailwindcss.com)** — `@theme` directive in `src/styles/global.css`
- **TypeScript** — strict mode
- **Vercel** — hosting + CDN

## Local development

```bash
npm install
npm run dev        # localhost:4321
npm run build      # production build to ./dist/
npm run preview    # preview production build
npm run lint       # ESLint (Astro + TypeScript)
npm run check      # Astro type checking
npm run format     # Prettier
```

Requires Node `>= 20.3` (Astro v5 minimum).

## Structure

```
src/
├── content/              # content collections (markdown + json)
│   ├── projects/         # project entries
│   ├── lab/              # lab posts
│   └── identity.json     # single source of truth for name/role/bio/links
├── layouts/Base.astro    # head, metadata, JSON-LD
├── sections/             # Hero, Projects, Lab, Identity, Footer
├── components/           # shared Astro + Svelte components
└── styles/global.css     # Tailwind theme tokens
public/
├── favicon.svg           # abstract terminal mark
├── og-image.png          # 1200x630 social card
└── robots.txt
```

Content lives in `src/content/`. Add a project: drop a `.md` file in `src/content/projects/` matching the schema in `src/content.config.ts`.

## Conventions

- **Commits**: conventional (`feat:`, `fix:`, `chore:`, `docs:`, `refactor:`)
- **Components**: Astro for static, Svelte only when client-side state is needed
- **Styling**: Tailwind v4 — no `tailwind.config.js`, custom tokens in `@theme` block
- **Accessibility**: respect `prefers-reduced-motion`, skip-link, semantic landmarks

## Deployment

Auto-deploy on push to `main` via Vercel. Preview deployments on every PR.

## License

Personal project. Code is public as reference — feel free to read and learn from it, but please don't copy the personal content (identity, bio, project entries) verbatim.
