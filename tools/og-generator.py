# -*- coding: utf-8 -*-
"""
og-generator.py — Open Graph link-preview images for melendeztech.com
1200 x 630 | Spectral + IBM Plex Mono | ES + EN

Produces:
    og.png        -> repo root, used by index.html
    og-en.png     -> optional English variant

Fonts — put these .ttf files in a ./fonts folder next to this script.
Both families are OFL; they live in the google/fonts repo under
ofl/spectral and ofl/ibmplexmono:
    Spectral-Light.ttf
    IBMPlexMono-Regular.ttf
    IBMPlexMono-Medium.ttf

Run:   python3 og-generator.py
Needs: pip install pillow
"""
import os
from PIL import Image, ImageDraw, ImageFont

# ─────────────────────────────────────────────────────────────
# CONTACT + COPY — edit here
# ─────────────────────────────────────────────────────────────
D = {
    "nombre": "Pedro R. Meléndez",
    "tel":    "787 630 6364",
    "web":    "MELENDEZTECH.COM",
}

COPY = {
    "es": {
        "cintillo": "CONSULTOR DE IT · SAN JUAN, PR",
        "rol":      "REDES · SEGURIDAD · MICROSOFT 365 · RESPALDOS",
        "linea":    "El departamento de IT que tu negocio no tiene.",
    },
    "en": {
        "cintillo": "IT CONSULTANT · SAN JUAN, PR",
        "rol":      "NETWORKS · SECURITY · MICROSOFT 365 · BACKUPS",
        "linea":    "The IT department your small business doesn't have.",
    },
}

# ─────────────────────────────────────────────────────────────
# DESIGN TOKENS — sampled from the printed card, keep in sync
# ─────────────────────────────────────────────────────────────
W, H = 1200, 630
PAPER  = (223, 226, 218)
INK    = (22, 25, 27)
MUTED  = (95, 100, 95)
RULE   = (173, 178, 168)
ACCENT = (27, 60, 196)

L, R = 93, 1107
FONTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fonts")


def F(name, size):
    return ImageFont.truetype(os.path.join(FONTS, name), size)


def layer(w, h):
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    return im, ImageDraw.Draw(im)


def tracked(draw, xy, text, font, fill, track=0.0):
    """Draw text with uniform letter-spacing, from a left baseline."""
    x, y = xy
    for ch in text:
        draw.text((x, y), ch, font=font, fill=fill, anchor="ls")
        x += draw.textlength(ch, font=font) + track


def place(base, tmp, x0, y0, right=None):
    """Paste `tmp` so its ink begins at (x0, y0), or ends at `right`."""
    bb = tmp.getbbox()
    if bb is None:
        return
    ox = (right - (bb[2] - bb[0])) if right is not None else x0
    base.alpha_composite(tmp.crop(bb), (int(round(ox)), int(round(y0))))


def fit_size(font_name, text, target_ink):
    """Point size whose rendered ink width lands closest to target_ink."""
    best, err = 8, 1e9
    for size in range(8, 200):
        im, d = layer(2600, 400)
        d.text((30, 300), text, font=F(font_name, size), fill=(0, 0, 0, 255), anchor="ls")
        bb = im.getbbox()
        if bb is None:
            continue
        w = bb[2] - bb[0]
        if abs(w - target_ink) < err:
            best, err = size, abs(w - target_ink)
        if w > target_ink + 40:
            break
    return best


def fit_track(text, font, target_ink):
    """Letter-spacing whose rendered ink width lands on target_ink."""
    lo, hi = -5.0, 40.0
    for _ in range(40):
        mid = (lo + hi) / 2
        im, d = layer(2600, 200)
        tracked(d, (30, 150), text, font, (0, 0, 0, 255), track=mid)
        bb = im.getbbox()
        w = (bb[2] - bb[0]) if bb else 0
        if w < target_ink:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def escala(draw, x, y, width, mark_at=0.216, step=12.7):
    """Calibration rule — the signature element, same as the printed card."""
    n = int(width / step)
    mark_i = int(n * mark_at)
    for i in range(n + 1):
        px = x + i * step
        if i == mark_i:
            draw.line([(px, y - 6), (px, y)], fill=ACCENT, width=2)
        else:
            h = 6 if i % 5 == 0 else 3
            draw.line([(px, y - h), (px, y)], fill=RULE, width=1)
    draw.line([(x, y), (x + n * step, y)], fill=RULE, width=1)


def build(path, lang="es"):
    T = COPY[lang]
    im = Image.new("RGBA", (W, H), PAPER + (255,))
    d = ImageDraw.Draw(im)

    mono_m = F("IBMPlexMono-Medium.ttf", 17)
    mono_r = F("IBMPlexMono-Regular.ttf", 17)
    mono_b = F("IBMPlexMono-Medium.ttf", 18)

    t, dd = layer(1600, 60)
    tracked(dd, (30, 40), T["cintillo"], mono_m, MUTED + (255,),
            track=fit_track(T["cintillo"], mono_m, 431))
    place(im, t, L, 88)

    t, dd = layer(1800, 220)
    dd.text((30, 160), D["nombre"], font=F("Spectral-Light.ttf",
            fit_size("Spectral-Light.ttf", D["nombre"], 774)),
            fill=INK + (255,), anchor="ls")
    place(im, t, 94, 136)

    escala(d, 92, 250, 991)

    t, dd = layer(1600, 60)
    tracked(dd, (30, 40), T["rol"], mono_r, MUTED + (255,),
            track=fit_track(T["rol"], mono_r, 704))
    place(im, t, L, 279)

    t, dd = layer(1800, 220)
    dd.text((30, 160), T["linea"], font=F("Spectral-Light.ttf",
            fit_size("Spectral-Light.ttf", T["linea"], 691)),
            fill=INK + (255,), anchor="ls")
    place(im, t, 94, 334)

    t, dd = layer(1600, 60)
    tracked(dd, (30, 40), D["web"], mono_b, INK + (255,),
            track=fit_track(D["web"], mono_b, 277))
    place(im, t, L, 530)

    t, dd = layer(1600, 60)
    tracked(dd, (30, 40), D["tel"], mono_b, ACCENT + (255,),
            track=fit_track(D["tel"], mono_b, 213))
    place(im, t, 0, 530, right=R)

    im.convert("RGB").save(path, "PNG", optimize=True)
    print("->", path)


if __name__ == "__main__":
    build("og.png", "es")
    build("og-en.png", "en")
