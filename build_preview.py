"""Bundle the three site pages into one self-contained HTML file.

The published preview has no access to sibling files, so CSS, fonts and images
are inlined as data URIs and the nav is rewired to in-page routing. Derived from
the real sources so the preview can't drift from what actually ships.

    python build_preview.py
"""

import base64
import pathlib
import re

ROOT = pathlib.Path(__file__).parent
PAGES = [("index.html", "skuffle"), ("support.html", "support"), ("press.html", "press")]
MIME = {".woff2": "font/woff2", ".webp": "image/webp", ".zip": "application/zip"}


def data_uri(path: pathlib.Path) -> str:
    mime = MIME.get(path.suffix, "application/octet-stream")
    return f"data:{mime};base64,{base64.b64encode(path.read_bytes()).decode()}"


def inline_css() -> str:
    css = (ROOT / "assets/css/site.css").read_text(encoding="utf-8")
    # url("../fonts/X.woff2") -> data URI
    def sub(m):
        rel = m.group(1)
        target = (ROOT / "assets/css" / rel).resolve()
        return f'url("{data_uri(target)}")' if target.exists() else m.group(0)
    return re.sub(r'url\("([^"]+)"\)', sub, css)


def inline_page(html: str) -> str:
    """Strip the document shell and swap asset paths for data URIs."""
    body = re.search(r"<body>(.*)</body>", html, re.S).group(1)
    body = re.sub(r'<a class="skip".*?</a>', "", body, flags=re.S)

    def sub_img(m):
        target = (ROOT / m.group(1)).resolve()
        return f'src="{data_uri(target)}"' if target.exists() else m.group(0)

    body = re.sub(r'src="(assets/img/[^"]+)"', sub_img, body)
    # The press ZIP is 9 MB; keep the button but point it at the live site.
    body = body.replace('href="assets/press/skuffle-press-assets.zip"',
                        'href="https://iddygames.com/assets/press/skuffle-press-assets.zip"')
    return body


sections = []
for filename, route in PAGES:
    body = inline_page((ROOT / filename).read_text(encoding="utf-8"))
    hidden = "" if route == "skuffle" else " hidden"
    sections.append(f'<div class="route" data-route="{route}"{hidden}>{body}</div>')

script = """
<script>
(function () {
  var routes = document.querySelectorAll('.route');
  function show(name) {
    routes.forEach(function (r) { r.hidden = r.dataset.route !== name; });
    document.querySelectorAll('.nav a').forEach(function (a) {
      if (a.dataset.route === name) { a.setAttribute('aria-current', 'page'); }
      else { a.removeAttribute('aria-current'); }
    });
    window.scrollTo(0, 0);
  }
  document.querySelectorAll('a[href]').forEach(function (a) {
    var href = a.getAttribute('href');
    var name = href === '/' ? 'skuffle'
             : href === 'support.html' ? 'support'
             : href === 'press.html' ? 'press' : null;
    if (!name) { return; }
    a.dataset.route = name;
    a.addEventListener('click', function (e) { e.preventDefault(); show(name); });
  });
})();
</script>
"""

banner = (
    '<p style="font-family:\'Share Tech Mono\',monospace;font-size:.7rem;'
    "letter-spacing:.18em;text-transform:uppercase;color:rgba(233,238,242,.34);"
    "text-align:center;padding:.6rem;margin:0;border-bottom:1px solid rgba(255,255,255,.08)\">"
    "Preview build &middot; nav is wired in-page</p>"
)

out = (
    "<title>Skuffle — iddy Games</title>\n"
    f"<style>{inline_css()}</style>\n"
    f"{banner}\n" + "\n".join(sections) + script
)

dest = ROOT / "preview.html"
dest.write_text(out, encoding="utf-8")
print(f"preview.html  {dest.stat().st_size // 1024} KB")
