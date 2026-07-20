# Personal site (Astro)

Theme: "lab notebook meets terminal" — dark charcoal background, amber
highlighter accent, `Fraunces` for headings, `Inter` for body, `IBM Plex Mono`
for labels/data. Signature feature is an interactive synthetic UMAP on the
homepage: drag the "cluster resolution" slider to watch points regroup and
recolor, mirroring Leiden clustering in Scanpy.

## Run locally

```bash
npm install
npm run dev
```

Visit http://localhost:4321

## Regenerate the UMAP data

The homepage visualization reads `public/data/umap.json`, precomputed by
`gen_umap_data.py`. To change the number of points, clusters, or palette,
edit the constants at the top of that script and rerun:

```bash
python3 gen_umap_data.py
```

Requires only Python's standard library (no numpy/sklearn dependency).

## Add content

- **Blog posts**: add a `.md` file to `src/content/blog/` (see `hello-world.md`
  for the frontmatter shape).
- **Posters/papers**: add a `.md` file to `src/content/posters/` (see
  `sample-poster.md`). Put the actual PDF in `public/posters/`.
- **Projects**: edit the `projects` array directly in `src/pages/projects.astro`.
- **Skills**: edit the `domains` array in `src/pages/skills.astro`.

## Deploy to Vercel

1. Push this repo to GitHub.
2. In Vercel: New Project → Import the repo. Vercel auto-detects Astro
   (build command `astro build`, output `dist/`) — no config needed.
3. Every push to `main` redeploys; every PR gets a preview URL.

## Things to personalize before shipping

- Replace `yourname.bio`, email, GitHub/LinkedIn/Scholar links in
  `src/components/Nav.astro` and `Footer.astro`.
- Replace placeholder copy on `about.astro`, `skills.astro`, `projects.astro`,
  `extracurriculars.astro`.
- Swap `site` URL in `astro.config.mjs` once you have your Vercel domain.
