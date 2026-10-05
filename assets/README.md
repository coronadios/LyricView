# Assets

This folder stores the project visual identity used across the docs, landing pages, README, and social previews.

## Recommended files

| File | Size | Purpose |
| --- | --- | --- |
| `banner.png` | 1600 × 900 | project hero banner for docs and landing pages |
| `ico.png` | 512 × 512 | main app icon / brand mark |
| `logo.png` | 1024 × 1024 | square logo for README and product pages |
| `og-image.png` | 1200 × 630 | social preview for sharing |
| `favicon.png` | 64 × 64 | small favicon in browser tabs |
| `icon-128.png` | 128 × 128 | app/icon asset for package metadata or docs |

## Visual rules

- use a black background with white borders or typography
- keep the design minimal and editorial
- prefer a clean monogram or wordmark rather than busy backgrounds
- maintain enough negative space for the docs to feel premium and open-source-ready

## Example usage in HTML

```html
<link rel="icon" type="image/png" href="assets/ico.png" />
<meta property="og:image" content="assets/og-image.png" />
<img src="assets/banner.png" alt="LyricView banner" />
```

## Example usage in Markdown / README

```md
![LyricView banner](assets/banner.png)

<img src="assets/logo.png" alt="LyricView logo" width="180" />
```

## Notes

- `banner.png` is the main hero asset for the landing docs.
- `ico.png` should be the master icon file, used as the base for favicon or smaller exports.
- `og-image.png` is recommended for previews in social cards and documentation embeds.
- Keep the filenames stable and lowercase for consistency.
