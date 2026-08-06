# iddygames.com

Static site for [Skuffle](https://store.steampowered.com/app/4816860/Skuffle/) by
iddy Games. Three pages, no build step, no dependencies.

```
index.html        landing page
support.html      support contact
press.html        fact sheet, description, asset download
assets/css        site.css — all styling, tokens in :root
assets/fonts      Bebas Neue, Saira Condensed, Share Tech Mono (woff2, OFL)
assets/img        webp
build_preview.py  bundles the three pages into one self-contained file
```

Palette and typefaces are the game's own, so the site and the game read as one
thing. Dark only, by design.

## Press assets

Screenshots and key art are published as GitHub Releases rather than committed,
so the repo stays small. The press page links to `releases/latest/download/`,
which always resolves to the newest set.

```bash
gh release create press-YYYY-MM assets/press/skuffle-press-assets.zip \
  --title "Press assets - Month Year" --notes "..."
```

## Deploying

GitHub Pages serves `main` from the repo root. `CNAME` and `.nojekyll` are both
required — don't delete them.

## Preview

`build_preview.py` writes `preview.html`, a single file with the CSS, fonts and
images inlined and the nav wired to in-page routing. Derived from the real pages,
so it can't drift. Not part of the deploy.
