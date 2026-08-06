# iddygames.com

Static site for iddy Games / Skuffle. Three pages, no build step, no dependencies.

```
index.html        landing page
support.html      FAQ + support@iddygames.com   <- the Steamworks support URL points here
press.html        fact sheet, description, asset download
assets/css        site.css (all styling)
assets/fonts      Bebas Neue, Saira Condensed, Share Tech Mono (woff2, self-hosted)
assets/img        webp, resized for web
assets/press      press asset ZIP (9 MB, full-res)
build_preview.py  bundles all three pages into one self-contained preview.html
CNAME             apex domain for GitHub Pages
```

## Design

Palette and fonts are the game's own, not invented for the site:

- Colours mirror `Zambie/ui/HUD/hud_palette.gd` — ground `#04080d`, and the four
  seat hues CRIMSON `#ff3d5a`, CYAN `#2fb8ff`, AMBER `#ffd23f`, LIME `#5ee34a`.
  The seat colours are used as a system — one per panel, four panels — because
  four players is the product.
- Fonts are the TTFs from `Zambie/fonts/`, converted to woff2. All three are
  OFL licensed, so self-hosting and redistribution are fine.

Everything is token-driven from `:root` in `site.css`. Change a colour there and
it propagates. The site commits to dark; there's no light theme by design.

## Deploying to GitHub Pages

1. Create a repo (e.g. `kem828/iddygames-site`) and push this folder.
2. Repo → Settings → Pages → Source: *Deploy from a branch*, branch `main`, folder `/`.
3. Settings → Pages → Custom domain: `iddygames.com`. Tick *Enforce HTTPS* once the
   certificate is issued (can take a few minutes to an hour).

The `CNAME` and `.nojekyll` files in this folder are both required — don't delete them.

## DNS at Namecheap

Domain List → Manage → **Advanced DNS**. Delete the default parking/redirect
records first, then add:

| Type  | Host | Value                  |
|-------|------|------------------------|
| A     | @    | 185.199.108.153        |
| A     | @    | 185.199.109.153        |
| A     | @    | 185.199.110.153        |
| A     | @    | 185.199.111.153        |
| CNAME | www  | `<your-username>.github.io.` |

Propagation is usually minutes but can take a few hours.

## Email forwarding (support@iddygames.com)

Namecheap includes this free with the domain.

1. Domain List → Manage → **Mail Settings** → choose *Email Forwarding*.
   (This sets the MX records for you.)
2. Advanced DNS → **Mail Settings** section → add a forwarder:
   `support` → your real inbox.

Send yourself a test message before putting the address anywhere public.

Why an alias rather than your personal address: it's on a public store page, so
it will be scraped, and the volume will be key requests rather than real support.
If it ever gets unmanageable you rotate the alias, not your actual email.

## Before this goes live — things to verify

The FAQ was written against how the game currently works, but a few answers name
UI that should be checked against the shipping build:

- **"Performance Mode"** and **render scale** — confirm those are the exact
  setting names players will see.
- **Controller troubleshooting** — the Steam Input / native fallback advice is
  right in principle; confirm the wording matches what actually helps.
- **Workshop maps mount at startup** — confirm a restart is genuinely required.
- **Lobby join is `A` on an empty slot** — taken from the lobby screenshot, worth
  a second look.
- **Release year** shows `2027` on the landing page and press kit. Update when the
  date firms up.

The landing page is deliberately a signpost — wordmark, one line, screenshots,
Steam button. Selling happens on the store page; don't grow this one.

## Updating the preview

`build_preview.py` regenerates `preview.html` — one self-contained file with the
CSS, fonts and images inlined and the nav wired to in-page routing. It's derived
from the real pages, so it can't drift from what ships.

```bash
python build_preview.py
```

`preview.html` is for sharing a look at the site. It isn't part of the deploy.
