# tools

Source for the brand assets. Nothing here is served by the website — GitHub
Pages ignores it. It lives in the repo so the assets are reproducible instead
of being mystery files.

## Fonts

Both generators need Spectral and IBM Plex Mono as `.ttf`. Both are OFL.
From this folder:

```bash
mkdir -p fonts && cd fonts
GF=https://raw.githubusercontent.com/google/fonts/main
curl -sSLO $GF/ofl/spectral/Spectral-Light.ttf
curl -sSLO $GF/ofl/spectral/Spectral-LightItalic.ttf
curl -sSLO $GF/ofl/ibmplexmono/IBMPlexMono-Light.ttf
curl -sSLO $GF/ofl/ibmplexmono/IBMPlexMono-Regular.ttf
curl -sSLO $GF/ofl/ibmplexmono/IBMPlexMono-Medium.ttf
```

`fonts/` is gitignored. Re-download it on a new machine.

## og-generator.py

Builds the 1200x630 link-preview image.

```bash
pip install pillow
python3 og-generator.py
```

Writes `og.png` (Spanish) and `og-en.png`. Copy `og.png` to the repo root
**and** to `card/og.png` — both pages point at their own copy.

Edit the `COPY` dict at the top when the tagline changes. The layout is
measured in pixels against the printed card, so keep `DESIGN TOKENS` in sync
with `card-generator.py`.

## card-generator.py

Builds the print-ready business card PDFs: 3.5 x 2 in, 0.125 in bleed, crop
marks, CMYK, embedded fonts, vCard QR on the back.

```bash
pip install reportlab qrcode pillow
python3 card-generator.py
```

Writes `business-card-EN.pdf` and `business-card-ES.pdf`. These are print
deliverables, not website files — send them to the printer, don't commit the
output.
