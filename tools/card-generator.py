# -*- coding: utf-8 -*-
"""
Pedro R. Meléndez — business card
3.5 x 2 in | 0.125 in bleed | crop marks | CMYK | embedded fonts | EN + ES
"""
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import CMYKColor

# ─────────────────────────────────────────────────────────────
# CONTACT — edit here
# ─────────────────────────────────────────────────────────────
D = {
    "nombre":  "Pedro R. Meléndez",
    "email":   "pedro@melendeztech.com",
    "tel":     "787 630 6364",
    "tel_raw": "+17876306364",
    "web":     "melendeztech.com",
    "web_url": "https://melendeztech.com",
}

# ─────────────────────────────────────────────────────────────
# COPY — the part that decides whether they call you
# ─────────────────────────────────────────────────────────────
COPY = {
    "en": {
        "cintillo": "IT consultant · San Juan, PR",
        "rol":      "Networks · Security · Microsoft 365 · Backups",
        "linea":    "The IT department your\nsmall business doesn't have.",
        "prueba":   "NIST CSF · Regulated environments · 15+ years",
        "ciudad":   "San Juan · Puerto Rico",
    },
    "es": {
        "cintillo": "Consultor de IT · San Juan, PR",
        "rol":      "Redes · Seguridad · Microsoft 365 · Respaldos",
        "linea":    "El departamento de IT que\ntu negocio no tiene.",
        "prueba":   "Controles NIST CSF · Ambientes regulados · 15+ años",
        "ciudad":   "San Juan · Puerto Rico",
    },
}

# ─────────────────────────────────────────────────────────────
IN = 72.0
TRIM_W, TRIM_H = 3.5 * IN, 2.0 * IN
BLEED, SLUG = 0.125 * IN, 0.125 * IN
PAGE_W = TRIM_W + 2 * (BLEED + SLUG)
PAGE_H = TRIM_H + 2 * (BLEED + SLUG)
OX = OY = BLEED + SLUG
M = 0.16 * IN

PAPER = CMYKColor(0.09, 0.03, 0.09, 0.05)
INK = CMYKColor(0, 0, 0, 1)
INK_RICH = CMYKColor(0.60, 0.45, 0.40, 1.00)
INK_SOFT = CMYKColor(0, 0, 0, 0.62)
RULE = CMYKColor(0, 0, 0, 0.28)
ACCENT = CMYKColor(0.92, 0.76, 0, 0)
PAPER_ON_INK = CMYKColor(0.05, 0.02, 0.06, 0.00)
SOFT_ON_INK = CMYKColor(0.10, 0.05, 0.12, 0.42)

for n, f in [("Spectral-L", "Spectral-Light"), ("Spectral-LI", "Spectral-LightItalic"),
             ("Plex-L", "IBMPlexMono-Light"), ("Plex-R", "IBMPlexMono-Regular"),
             ("Plex-M", "IBMPlexMono-Medium")]:
    pdfmetrics.registerFont(TTFont(n, f"fonts/{f}.ttf"))


def tracked(c, x, y, text, font, size, color, track=0.0, align="l"):
    c.setFont(font, size); c.setFillColor(color)
    w = sum(pdfmetrics.stringWidth(ch, font, size) + track for ch in text) - track
    if align == "r":
        x -= w
    elif align == "c":
        x -= w / 2
    for ch in text:
        c.drawString(x, y, ch)
        x += pdfmetrics.stringWidth(ch, font, size) + track
    return w


def autofit(text, font, maximo, ancho, track=0.0):
    size = maximo
    while size > 8:
        w = sum(pdfmetrics.stringWidth(ch, font, size) + track for ch in text) - track
        if w <= ancho:
            break
        size -= 0.25
    return size


def vcard(ascii_safe=False):
    """vCard for the QR. ascii_safe strips accents: the payload carries no ECI
    marker, so an older reader could render the UTF-8 bytes as Latin-1."""
    import unicodedata
    def n(t):
        return (unicodedata.normalize("NFKD", t).encode("ascii", "ignore").decode()
                if ascii_safe else t)
    nom = n(D["nombre"])
    return "\r\n".join([
        "BEGIN:VCARD", "VERSION:3.0",
        "N:" + nom.split()[-1] + ";" + " ".join(nom.split()[:-1]),
        "FN:" + nom,
        "EMAIL:" + D["email"],
        "TEL:" + D["tel_raw"],
        # Sin URL a propósito: subía el QR a versión 8 y cada módulo quedaba
        # en 0.32 mm, por debajo de lo fiable a este tamaño. La web va impresa.
        "END:VCARD"])


def escala(c, x, y, width, color, mark_color, mark_at=0.28, step=3.2, flip=False):
    """SIGNATURE ELEMENT: calibration rule — spectrum / typographic ruler."""
    c.saveState(); c.setLineCap(0)
    n = int(width / step); mark_i = int(n * mark_at)
    for i in range(n + 1):
        px = x + i * step
        h = 3.1 if i % 5 == 0 else 1.5
        if i == mark_i:
            c.setStrokeColor(mark_color); c.setLineWidth(0.9); h = 5.0
        else:
            c.setStrokeColor(color); c.setLineWidth(0.35)
        c.line(px, y, px, y + (-h if flip else h))
    c.setStrokeColor(color); c.setLineWidth(0.35)
    c.line(x, y, x + n * step, y)
    c.restoreState()


def crop_marks(c, color):
    c.saveState(); c.setStrokeColor(color); c.setLineWidth(0.25)
    L = SLUG * 0.8
    for x in (OX, OX + TRIM_W):
        c.line(x, OY - BLEED, x, OY - BLEED - L)
        c.line(x, OY + TRIM_H + BLEED, x, OY + TRIM_H + BLEED + L)
    for y in (OY, OY + TRIM_H):
        c.line(OX - BLEED, y, OX - BLEED - L, y)
        c.line(OX + TRIM_W + BLEED, y, OX + TRIM_W + BLEED + L, y)
    c.restoreState()


def anverso(c, T_):
    c.setFillColor(PAPER); c.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)
    crop_marks(c, INK_SOFT)
    L, R = OX + M, OX + TRIM_W - M
    T = OY + TRIM_H - M

    tracked(c, L, T - 5.0, T_["cintillo"].upper(), "Plex-M", 4.4, INK_SOFT, 1.15)

    ns = autofit(D["nombre"], "Spectral-L", 22, R - L)
    c.setFont("Spectral-L", ns); c.setFillColor(INK)
    c.drawString(L - 1.0, T - 52, D["nombre"])

    escala(c, L, T - 64, R - L - 6, RULE, ACCENT, mark_at=0.22)

    rs = autofit(T_["rol"].upper(), "Plex-R", 5.0, R - L, 0.95)
    tracked(c, L, T - 78, T_["rol"].upper(), "Plex-R", rs, INK_SOFT, 0.95)

    tracked(c, L, OY + M - 1.4, D["web"].upper(), "Plex-M", 5.6, INK, 1.1)
    tracked(c, R, OY + M - 1.4, D["tel"], "Plex-M", 5.6, ACCENT, 1.1, align="r")


def reverso(c, T_):
    c.setFillColor(INK_RICH); c.rect(0, 0, PAGE_W, PAGE_H, stroke=0, fill=1)
    crop_marks(c, SOFT_ON_INK)
    L, R = OX + M, OX + TRIM_W - M
    T = OY + TRIM_H - M

    QR = 0.66 * IN
    qx, qy = R - QR, OY + M + 6
    try:
        import qrcode
        from reportlab.lib.utils import ImageReader
        img = qrcode.QRCode(border=0, box_size=10,
                            error_correction=qrcode.constants.ERROR_CORRECT_L)
        img.add_data(vcard(ascii_safe=True))
        img.make(fit=True)
        pil = img.make_image(fill_color="black", back_color="white").convert("RGB")
        c.setFillColor(PAPER_ON_INK)
        c.rect(qx - 2.5, qy - 2.5, QR + 5, QR + 5, stroke=0, fill=1)
        c.drawImage(ImageReader(pil), qx, qy, QR, QR)
        tracked(c, qx + QR / 2, qy + QR + 6.5, "VCARD", "Plex-R", 3.8,
                SOFT_ON_INK, 0.9, align="c")
        print("   QR v%d · %d módulos · %.3f mm/módulo" %
              (img.version, 17 + 4 * img.version,
               QR / (17 + 4 * img.version) * 25.4 / 72))
    except Exception as e:
        print("QR skipped:", e)

    c.setFont("Spectral-LI", 8.6); c.setFillColor(PAPER_ON_INK)
    for i, ln in enumerate(T_["linea"].split("\n")):
        c.drawString(L, T - 8 + (-11.6 * i), ln)

    escala(c, L, T - 52, (R - QR - 14) - L, SOFT_ON_INK, ACCENT, mark_at=0.62, flip=True)

    y = T - 67
    for label, val in [("E", D["email"]), ("T", D["tel"]), ("W", D["web"])]:
        tracked(c, L, y, label, "Plex-R", 4.6, SOFT_ON_INK, 0.6)
        tracked(c, L + 11, y, val, "Plex-R", 6.4, PAPER_ON_INK, 0.25)
        y -= 11.0

    ps = autofit(T_["prueba"].upper(), "Plex-L", 4.0, (R - QR - 14) - L, 0.75)
    tracked(c, L, OY + M - 1, T_["prueba"].upper(), "Plex-L", ps, SOFT_ON_INK, 0.75)


def build(path, lang="en"):
    T_ = COPY[lang]
    c = canvas.Canvas(path, pagesize=(PAGE_W, PAGE_H))
    c.setTitle("Business card — " + D["nombre"])
    c.setAuthor(D["nombre"]); c.setSubject(T_["rol"])
    anverso(c, T_); c.showPage()
    reverso(c, T_); c.showPage()
    c.save()
    print("→", path)


if __name__ == "__main__":
    build("business-card-EN.pdf", "en")
    build("business-card-ES.pdf", "es")
