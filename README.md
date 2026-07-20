# tanayadatar.bio

Personal portfolio site for Tanaya Datar — bioinformatics, machine learning, and computational biology.

**Live site:** [tanayadatar.bio](https://tanayadatar.bio)

## Built With

- [Astro](https://astro.build) — static site framework
- Vanilla JavaScript & CSS (no UI framework) — custom components, animations, and theming
- Hosted on Vercel

## Pages

- **Home** — intro + animated brain/neural-network visual
- **About** — background, research interests, education
- **Skills** — technical skills overview
- **Projects** — filterable project grid (bioinformatics, ML, tools)
- **Research** — posters and research work
- **Extracurriculars** — activities, awards, volunteering
- **Blog** — [Genome Insider](https://genome-insider.vercel.app/) (separate site)
- **Contact**

## Features

- Light/dark mode toggle (defaults to dark, preference saved via `localStorage`)
- Responsive layout
- Custom animated components (SVG + vanilla JS, no external animation libraries)

## Structure

```
src/
  components/   reusable UI (Nav, Footer, BrainNetwork, etc.)
  layouts/      shared page layout
  pages/        site routes
  styles/       global CSS + theme tokens
```