#!/usr/bin/env python3
"""Generates every profile SVG in ../assets from the data below.

Edit the text/data, then run:  python3 scripts/build_svgs.py
Each output is parsed as XML before it is written, so a broken file fails loudly.
"""
from pathlib import Path
from xml.sax.saxutils import escape
import xml.etree.ElementTree as ET

ASSETS = Path(__file__).resolve().parent.parent / "assets"
FONT = "'Segoe UI', system-ui, -apple-system, 'Helvetica Neue', Arial, sans-serif"
RED, RED_LIGHT, NAVY, MUTED = "#d0112a", "#ff2a40", "#00285a", "#a9b5cc"
WIDTH = 1200
CONTENT_LEFT, CONTENT_RIGHT = 48, 1152

# ---------------------------------------------------------------- content data

STATS = [("100s", "projects delivered"), ("4.9★", "Google rating"),
         ("6", "cities in Germany"), ("1", "team for everything")]

PARTNERS = [("Google Partner", "G", "#4285F4"),
            ("Amazon Ads Verified Partner", "a", "#FF9900"),
            ("JTL Servicepartner", "J", "#1E5AA8")]

SERVICES = [
    ("web", "Web Design", ["Responsive websites, CMS builds,", "logos & print media like flyers,", "menus and brochures."], ("#ff2a40", "#ff7a2a")),
    ("growth", "Online Marketing", ["SEO & local SEO, Google Ads,", "Amazon & eBay SEO, content and", "affiliate marketing, audits."], ("#16c784", "#0ea5a4")),
    ("cart", "E-Commerce", ["Webshops that sell, plus Amazon", "& eBay optimization. JTL and", "Afterbuy setup & consulting."], ("#ff8a00", "#fbbc05")),
    ("code", "Software", ["Custom software, backends,", "databases and automation —", "tailor-made ERP, CRM & CMS."], ("#2f6bff", "#5b3df5")),
    ("phone", "Apps", ["Native iOS & Android and hybrid", "apps, from the first concept to", "App Store & Play Store."], ("#a245ff", "#ff3d9a")),
    ("spark", "AI Solutions", ["Custom AI that is understandable,", "practical and measurable —", "verständlich, praxisnah, messbar."], ("#ff2a40", "#a245ff")),
]

STEPS = [("Analyse", "Goals, market &", "keyword research"),
         ("Design", "UX & a brand that", "converts visitors"),
         ("Build", "Websites, shops,", "apps & software"),
         ("Grow", "SEO, ads, data", "& AI that scale")]

PLATFORM_GROUPS = [
    ("Development", RED_LIGHT, ["HTML5", "JavaScript", "PHP", "Laravel", "Node.js", "AngularJS", "iOS", "Android"]),
    ("Shop systems", "#fbbc05", ["Shopify", "WooCommerce", "Magento", "JTL Wawi & Shop", "Afterbuy", "Gambio", "xt:Commerce"]),
    ("CMS", "#2f6bff", ["WordPress", "TYPO3", "Joomla"]),
    ("Advertising & local", "#16c784", ["Google Ads", "Microsoft Ads", "Amazon Ads", "YouTube Ads", "Shopping Ads", "Google My Business"]),
    ("Analytics & SEO", "#a245ff", ["Google Analytics", "Tag Manager", "Search Console", "Semrush", "ahrefs", "Matomo"]),
]

BUTTONS = [
    ("btn-website", "listandsell.de", "globe", RED),
    ("btn-email", "info@listandsell.de", "mail", RED),
    ("btn-phone", "030 2353 8660", "call", "#2f6bff"),
    ("btn-whatsapp", "WhatsApp", "chat", "#25D366"),
    ("btn-linkedin", "LinkedIn", "linkedin", "#0A66C2"),
    ("btn-instagram", "Instagram", "camera", "#E4405F"),
    ("btn-facebook", "Facebook", "facebook", "#1877F2"),
    ("btn-pinterest", "Pinterest", "pin", "#E60023"),
]

# Stroke icons drawn on a 32x32 grid.
ICONS = {
    "web": '<rect x="3" y="5" width="26" height="22" rx="3"/><path d="M3 11h26M8 16h9M8 21h14"/>',
    "growth": '<path d="M4 24l8-8 6 5 10-11"/><path d="M21 10h7v7"/>',
    "cart": '<path d="M3 5h4l3 15h15l3-10H9"/><circle cx="12" cy="26" r="2"/><circle cx="23" cy="26" r="2"/>',
    "code": '<path d="M11 9l-7 7 7 7M21 9l7 7-7 7M18 6l-4 20"/>',
    "phone": '<rect x="9" y="3" width="14" height="26" rx="3"/><path d="M14 25h4"/>',
    "spark": '<path d="M16 3l3 8 8 3-8 3-3 8-3-8-8-3 8-3z"/><path d="M26 21l1 3 3 1-3 1-1 3-1-3-3-1 3-1z"/>',
    "globe": '<circle cx="16" cy="16" r="12"/><ellipse cx="16" cy="16" rx="5" ry="12"/><path d="M4 16h24"/>',
    "mail": '<rect x="4" y="7" width="24" height="18" rx="3"/><path d="M5 9l11 8 11-8"/>',
    "chat": '<path d="M16 4a12 12 0 0 0-10.4 18L4 28l6.2-1.6A12 12 0 1 0 16 4z"/>',
    "call": '<path d="M8 4h5l2 6-3 2a15 15 0 0 0 8 8l2-3 6 2v5a3 3 0 0 1-3 3A23 23 0 0 1 5 7a3 3 0 0 1 3-3z"/>',
    "camera": '<rect x="5" y="5" width="22" height="22" rx="6"/><circle cx="16" cy="16" r="5"/><circle cx="22" cy="10" r="1"/>',
    "linkedin": '<rect x="5" y="5" width="22" height="22" rx="4"/><path d="M11 14v8M11 10v.5M16 22v-8M16 17a3 3 0 0 1 6 0v5"/>',
    "facebook": '<path d="M19 28V17h4l1-4h-5v-3c0-1.2.4-2 2-2h3V4.5A30 30 0 0 0 20 4c-3.5 0-6 2-6 6v3h-4v4h4v11"/>',
    "pin": '<path d="M16 29s9-8 9-15a9 9 0 0 0-18 0c0 7 9 15 9 15z"/><circle cx="16" cy="14" r="3"/>',
}

# ---------------------------------------------------------------- shared design system

BASE_DEFS = f"""
<linearGradient id="card" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0b2a5c"/><stop offset="1" stop-color="#020c1d"/></linearGradient>
<linearGradient id="accent" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{RED_LIGHT}"/><stop offset="1" stop-color="#ff7a2a"/></linearGradient>
<radialGradient id="glow"><stop offset="0" stop-color="{RED_LIGHT}" stop-opacity=".42"/><stop offset="1" stop-color="{RED_LIGHT}" stop-opacity="0"/></radialGradient>
<radialGradient id="glowBlue"><stop offset="0" stop-color="#2f6bff" stop-opacity=".32"/><stop offset="1" stop-color="#2f6bff" stop-opacity="0"/></radialGradient>
<pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse"><path d="M40 0H0V40" fill="none" stroke="#fff" stroke-opacity=".045"/></pattern>
<filter id="shadow" x="-30%" y="-30%" width="160%" height="180%"><feDropShadow dx="0" dy="14" stdDeviation="16" flood-color="#000" flood-opacity=".45"/></filter>
"""

ANIMATED = ".float,.float2,.float3,.pulse,.rise,.draw,.flow,.ring"
BASE_CSS = f"""
text {{ font-family: {FONT}; }}
.float {{ animation: float 6s ease-in-out infinite; }}
.float2 {{ animation: float 7s ease-in-out 1s infinite; }}
.float3 {{ animation: float 5s ease-in-out 2s infinite; }}
.pulse {{ animation: pulse 5s ease-in-out infinite; }}
.rise {{ animation: rise .8s ease-out both; }}
.draw {{ stroke-dasharray: 600; animation: draw 2.4s .6s ease-out both; }}
.flow {{ animation: flow 1.2s linear infinite; }}
.ring {{ transform-box: fill-box; transform-origin: center; animation: ring 2.8s ease-out infinite; }}
@keyframes float {{ 50% {{ transform: translateY(-10px); }} }}
@keyframes pulse {{ 50% {{ opacity: .55; }} }}
@keyframes rise {{ from {{ opacity: 0; transform: translateY(14px); }} to {{ opacity: 1; transform: none; }} }}
@keyframes draw {{ from {{ stroke-dashoffset: 600; }} to {{ stroke-dashoffset: 0; }} }}
@keyframes flow {{ to {{ stroke-dashoffset: -36; }} }}
@keyframes ring {{ from {{ transform: scale(1); opacity: .7; }} to {{ transform: scale(1.35); opacity: 0; }} }}
@media (prefers-reduced-motion: reduce) {{
  {ANIMATED} {{ animation: none !important; }}
  .ring {{ opacity: 0; }}
}}
"""


def svg(height, label, body, defs="", width=WIDTH):
    aria = escape(label, {'"': "&quot;"})
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
            f'viewBox="0 0 {width} {height}" role="img" aria-label="{aria}">'
            f'<defs>{BASE_DEFS}{defs}<style>{BASE_CSS}</style></defs>{body}</svg>')


def panel(height, inner="", width=WIDTH):
    """Dark rounded card with grid texture and soft brand glows."""
    return (f'<clipPath id="clip"><rect width="{width}" height="{height}" rx="28"/></clipPath>'
            f'<g clip-path="url(#clip)"><rect width="{width}" height="{height}" fill="url(#card)"/>'
            f'<rect width="{width}" height="{height}" fill="url(#grid)"/>'
            f'<circle class="pulse" cx="{width - 120}" cy="40" r="340" fill="url(#glow)"/>'
            f'<circle cx="80" cy="{height}" r="300" fill="url(#glowBlue)"/>{inner}</g>'
            f'<rect x=".5" y=".5" width="{width - 1}" height="{height - 1}" rx="28" fill="none" stroke="#fff" stroke-opacity=".08"/>')


def text(x, y, s, size=18, fill="#fff", weight=400, anchor="start", extra=""):
    return (f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" fill="{fill}" '
            f'text-anchor="{anchor}" {extra}>{escape(s)}</text>')


def text_width(s, size):
    """Rough width of bold sans-serif text; SVG can't measure, so chips size from this."""
    def units(c):
        if c in "il.,:;'|!Ijt() ":
            return .3
        if c in "mwMW@":
            return .86
        return .66 if c.isupper() or c.isdigit() else .56
    return sum(units(c) for c in s) * size


def heading(x, y, eyebrow, title):
    return (f'<rect x="{x}" y="{y - 13}" width="28" height="4" rx="2" fill="url(#accent)"/>'
            + text(x + 40, y - 6, eyebrow.upper(), 15, RED_LIGHT, 700, extra='letter-spacing="3"')
            + text(x, y + 46, title, 42, "#fff", 800, extra='letter-spacing="-1"'))


def icon(name, x, y, scale=1.0, color="#fff", stroke=2.2):
    return (f'<g transform="translate({x} {y}) scale({scale})" fill="none" stroke="{color}" '
            f'stroke-width="{stroke}" stroke-linecap="round" stroke-linejoin="round">{ICONS[name]}</g>')


def gradient(gid, start, end, vertical=False):
    x2, y2 = ("0", "1") if vertical else ("1", "1")
    return (f'<linearGradient id="{gid}" x1="0" y1="0" x2="{x2}" y2="{y2}">'
            f'<stop offset="0" stop-color="{start}"/><stop offset="1" stop-color="{end}"/></linearGradient>')


def chip(x, y, label, dot, size=17, height=40):
    width = text_width(label, size) + 50
    markup = (f'<rect x="{x}" y="{y}" width="{width:.0f}" height="{height}" rx="{height / 2}" fill="#fff" '
              f'fill-opacity=".05" stroke="#fff" stroke-opacity=".12"/>'
              f'<circle cx="{x + 20}" cy="{y + height / 2}" r="5" fill="{dot}"/>'
              + text(x + 34, y + height / 2 + 6, label, size, "#e6ebf5", 600))
    return width, markup

# ---------------------------------------------------------------- hero


def brand_lockup():
    bars = "".join(f'<rect x="{70 + i * 10}" y="{86 - h}" width="7" height="{h}" rx="2" fill="{c}"/>'
                   for i, (h, c) in enumerate([(10, RED), (16, "#ff6a2a"), (22, "#fbbc05"), (28, "#34c759")]))
    word = f'<text x="112" y="86" font-size="26" font-weight="800" fill="#fff">List <tspan fill="{RED_LIGHT}">&amp;</tspan></text>'
    tag = ('<g transform="rotate(-8 232 76)"><rect x="192" y="60" width="80" height="32" rx="7" fill="url(#accent)"/>'
           f'<circle cx="203" cy="76" r="3.5" fill="{NAVY}"/>' + text(240, 83, "S€LL", 18, "#fff", 800, "middle") + '</g>')
    return bars + word + tag


def hero_copy():
    eyebrow = "FULL-SERVICE DIGITAL AGENCY · BERLIN"
    pill_w = text_width(eyebrow, 14) + len(eyebrow) * 2.5 + 56
    pill = (f'<rect x="70" y="140" width="{pill_w:.0f}" height="36" rx="18" fill="#fff" fill-opacity=".06" stroke="#fff" stroke-opacity=".16"/>'
            '<circle class="pulse" cx="92" cy="158" r="5" fill="#34d399"/>'
            + text(108, 163, eyebrow, 14, "#e6ebf5", 700, extra='letter-spacing="2.5"'))
    style = 'letter-spacing="-1.5"'
    headline = (text(70, 252, "We don't just build", 56, "#fff", 800, extra=style)
                + text(70, 318, "websites — we make", 56, "#fff", 800, extra=style)
                + f'<text x="70" y="384" font-size="56" font-weight="800" fill="#fff" {style}>them <tspan fill="url(#shine)">successful.</tspan></text>')
    sub = (text(70, 434, "Web design, SEO, e-commerce, apps, software", 21, MUTED, 500)
           + text(70, 464, "and AI — all from one source in Berlin.", 21, MUTED, 500))
    buttons = ('<rect x="70" y="500" width="236" height="58" rx="29" fill="url(#accent)" filter="url(#shadow)"/>'
               + text(188, 536, "Start a project  →", 19, "#fff", 700, "middle")
               + '<rect x="322" y="500" width="210" height="58" rx="29" fill="#fff" fill-opacity=".06" stroke="#fff" stroke-opacity=".22"/>'
               + text(427, 536, "Explore services", 19, "#fff", 600, "middle"))
    footer = (text(70, 606, "Berlin (HQ) · München · Potsdam · Düsseldorf · Hamburg · Frankfurt", 15, MUTED, 600)
              + text(1130, 606, "converting words into sales", 15, MUTED, 600, "end", 'font-style="italic"'))
    return pill + headline + sub + buttons + footer


def browser_mock():
    x, y = 720, 120
    dots = "".join(f'<circle cx="{x + 24 + i * 18}" cy="{y + 19}" r="5" fill="{c}"/>'
                   for i, c in enumerate(["#ff5f57", "#febc2e", "#28c840"]))
    products = "".join(
        f'<rect x="{x + 24 + i * 128}" y="{y + 192}" width="116" height="80" rx="10" fill="#fff" fill-opacity=".05" stroke="#fff" stroke-opacity=".08"/>'
        f'<rect x="{x + 32 + i * 128}" y="{y + 200}" width="100" height="38" rx="6" fill="url(#p{i})"/>'
        f'<rect x="{x + 32 + i * 128}" y="{y + 248}" width="64" height="7" rx="3.5" fill="#fff" fill-opacity=".55"/>'
        f'<rect x="{x + 32 + i * 128}" y="{y + 260}" width="40" height="6" rx="3" fill="{RED_LIGHT}"/>'
        for i in range(3))
    page_hero = (f'<rect x="{x + 24}" y="{y + 62}" width="190" height="14" rx="7" fill="#fff" fill-opacity=".85"/>'
                 f'<rect x="{x + 24}" y="{y + 84}" width="150" height="14" rx="7" fill="#fff" fill-opacity=".5"/>'
                 f'<rect x="{x + 24}" y="{y + 112}" width="180" height="7" rx="3.5" fill="#fff" fill-opacity=".22"/>'
                 f'<rect x="{x + 24}" y="{y + 126}" width="130" height="7" rx="3.5" fill="#fff" fill-opacity=".22"/>'
                 f'<rect x="{x + 24}" y="{y + 146}" width="100" height="28" rx="14" fill="url(#accent)"/>')
    image = (f'<clipPath id="imgclip"><rect x="{x + 236}" y="{y + 58}" width="160" height="118" rx="12"/></clipPath>'
             f'<g clip-path="url(#imgclip)"><rect x="{x + 236}" y="{y + 58}" width="160" height="118" fill="url(#heroimg)"/>'
             f'<circle cx="{x + 360}" cy="{y + 88}" r="12" fill="#ffd166" fill-opacity=".9"/>'
             f'<path d="M{x + 236} {y + 176}L{x + 290} {y + 120}L{x + 330} {y + 150}L{x + 360} {y + 128}L{x + 396} {y + 165}V{y + 176}Z" fill="#fff" fill-opacity=".2"/></g>')
    return (f'<g class="float" filter="url(#shadow)">'
            f'<rect x="{x}" y="{y}" width="420" height="290" rx="16" fill="#0d2348" stroke="#fff" stroke-opacity=".14"/>'
            f'<path d="M{x} {y + 38}H{x + 420}" stroke="#fff" stroke-opacity=".08"/>{dots}'
            f'<rect x="{x + 80}" y="{y + 8}" width="250" height="22" rx="11" fill="#fff" fill-opacity=".07"/>'
            + text(x + 98, y + 23, "https://listandsell.de", 12.5, MUTED, 500)
            + page_hero + image + products + '</g>')


def floating_cards():
    curve = "M670 486 C 700 480, 720 476, 744 466 S 790 456, 812 444 S 856 420, 882 408"
    analytics = ('<g class="float2" filter="url(#shadow)">'
                 '<rect x="648" y="372" width="256" height="132" rx="18" fill="#0f2a57" stroke="#fff" stroke-opacity=".14"/>'
                 + text(670, 402, "Organic traffic", 14, MUTED, 600)
                 + '<rect x="818" y="386" width="66" height="24" rx="12" fill="#16c784" fill-opacity=".18"/>'
                 + text(851, 403, "▲ rising", 12.5, "#34d399", 700, "middle")
                 + f'<path d="{curve} V 492 H 670 Z" fill="url(#spark)"/>'
                 + f'<path class="draw" d="{curve}" fill="none" stroke="#34d399" stroke-width="3" stroke-linecap="round"/>'
                 + '<circle class="pulse" cx="882" cy="408" r="5" fill="#34d399"/></g>')
    order = ('<g class="float3" filter="url(#shadow)">'
             '<rect x="950" y="432" width="222" height="78" rx="18" fill="#0f2a57" stroke="#fff" stroke-opacity=".14"/>'
             '<circle cx="982" cy="471" r="19" fill="url(#accent)"/>'
             + icon("cart", 973.2, 462.2, .55, "#fff", 3)
             + text(1012, 465, "New order", 17, "#fff", 700)
             + text(1012, 488, "just now · webshop", 13, MUTED, 500) + '</g>')
    rating = ('<g class="float2" filter="url(#shadow)">'
              '<rect x="1010" y="84" width="166" height="66" rx="16" fill="#0f2a57" stroke="#fff" stroke-opacity=".14"/>'
              + text(1028, 110, "Google rating", 13, MUTED, 600)
              + text(1028, 136, "★★★★★", 17, "#fbbc05", 400)
              + text(1126, 137, "4.9", 19, "#fff", 800) + '</g>')
    return analytics + order + rating


def build_hero():
    height = 640
    defs = ('<linearGradient id="shine" gradientUnits="userSpaceOnUse" x1="210" y1="0" x2="560" y2="0" spreadMethod="reflect">'
            f'<stop offset="0" stop-color="{RED_LIGHT}"/><stop offset=".5" stop-color="#ff8a3d"/><stop offset="1" stop-color="#ffd166"/>'
            '<animateTransform attributeName="gradientTransform" type="translate" values="0 0;350 0;0 0" dur="6s" repeatCount="indefinite"/></linearGradient>'
            + gradient("heroimg", "#1d3f7a", RED)
            + gradient("spark", "#34d399", "#0f2a57", vertical=True)
            + gradient("p0", RED_LIGHT, "#ff7a2a") + gradient("p1", "#2f6bff", "#5b3df5") + gradient("p2", "#16c784", "#0ea5a4"))
    bottom_bar = f'<rect y="{height - 8}" width="{WIDTH}" height="8" fill="url(#accent)"/>'
    body = panel(height, bottom_bar) + brand_lockup() + hero_copy() + browser_mock() + floating_cards()
    return svg(height, "List & Sell GmbH — We don't just build websites, we make them successful.", body, defs)

# ---------------------------------------------------------------- sections


def build_stats():
    height, col_w = 300, 276
    cols = "".join(
        text(CONTENT_LEFT + col_w / 2 + i * col_w, 112, num, 60, "url(#accent)", 800, "middle", 'letter-spacing="-1"')
        + text(CONTENT_LEFT + col_w / 2 + i * col_w, 150, label, 18, MUTED, 600, "middle")
        for i, (num, label) in enumerate(STATS))
    dividers = "".join(f'<path d="M{CONTENT_LEFT + i * col_w} 62V150" stroke="#fff" stroke-opacity=".1"/>' for i in (1, 2, 3))
    partners, x = [], 300
    for name, letter, color in PARTNERS:
        w = text_width(name, 18) + 76
        partners.append(f'<rect x="{x}" y="226" width="{w:.0f}" height="48" rx="24" fill="#fff" fill-opacity=".05" stroke="#fff" stroke-opacity=".12"/>'
                        f'<circle cx="{x + 26}" cy="250" r="15" fill="{color}"/>'
                        + text(x + 26, 256, letter, 17, "#fff", 800, "middle")
                        + text(x + 50, 256, name, 18, "#e6ebf5", 600))
        x += w + 16
    assert x - 16 <= CONTENT_RIGHT, "partner chips overflow the card"
    row = (f'<path d="M{CONTENT_LEFT} 192H{CONTENT_RIGHT}" stroke="#fff" stroke-opacity=".08"/>'
           + text(CONTENT_LEFT, 256, "CERTIFIED PARTNER", 15, RED_LIGHT, 700, extra='letter-spacing="3"') + "".join(partners))
    return svg(height, "100s of projects delivered, 4.9 Google rating, 6 cities, 1 team. Google Partner, Amazon Ads Verified Partner, JTL Servicepartner.",
               panel(height) + cols + dividers + row)


def build_services():
    height, card_w, card_h, gap = 790, 352, 270, 24
    defs = "".join(gradient(f"s{i}", *colors) for i, (*_, colors) in enumerate(SERVICES))
    cards = []
    for i, (icon_name, title, lines, _) in enumerate(SERVICES):
        x = CONTENT_LEFT + (i % 3) * (card_w + gap)
        y = 170 + (i // 3) * (card_h + gap)
        desc = "".join(text(x + 28, y + 190 + n * 28, line, 18, MUTED, 500) for n, line in enumerate(lines))
        cards.append(f'<g class="rise" style="animation-delay:{i * .12:.2f}s">'
                     f'<rect x="{x}" y="{y}" width="{card_w}" height="{card_h}" rx="22" fill="#fff" fill-opacity=".04" stroke="#fff" stroke-opacity=".09"/>'
                     f'<rect x="{x + 28}" y="{y + 28}" width="64" height="64" rx="16" fill="url(#s{i})"/>'
                     + icon(icon_name, x + 44, y + 44)
                     + text(x + card_w - 28, y + 58, f"0{i + 1}", 22, "#fff", 800, "end", 'fill-opacity=".16"')
                     + text(x + 28, y + 136, title, 26, "#fff", 800)
                     + f'<rect x="{x + 28}" y="{y + 154}" width="36" height="3" rx="1.5" fill="url(#s{i})"/>'
                     + desc + '</g>')
    body = panel(height) + heading(CONTENT_LEFT, 80, "What we do", "Everything from one source.") + "".join(cards)
    label = "Services: " + "; ".join(f"{t}: {' '.join(l)}" for _, t, l, _ in SERVICES)
    return svg(height, label, body, defs)


def build_process():
    height, cy = 400, 220
    centers = [CONTENT_LEFT + 138 + i * 276 for i in range(len(STEPS))]
    line = f"M{centers[0]} {cy}H{centers[-1]}"
    track = (f'<path d="{line}" stroke="#fff" stroke-opacity=".12" stroke-width="2"/>'
             f'<path class="flow" d="{line}" stroke="{RED_LIGHT}" stroke-width="3" stroke-dasharray="10 26" stroke-linecap="round"/>')
    nodes = "".join(
        f'<circle class="ring" style="animation-delay:{i * .7:.1f}s" cx="{cx}" cy="{cy}" r="40" fill="none" stroke="{RED_LIGHT}" stroke-width="2"/>'
        f'<circle cx="{cx}" cy="{cy}" r="40" fill="#0b2a5c" stroke="url(#accent)" stroke-width="3"/>'
        + text(cx, cy + 8, f"0{i + 1}", 22, "#fff", 800, "middle")
        + text(cx, 300, title, 24, "#fff", 800, "middle")
        + text(cx, 332, l1, 17, MUTED, 500, "middle") + text(cx, 358, l2, 17, MUTED, 500, "middle")
        for i, (cx, (title, l1, l2)) in enumerate(zip(centers, STEPS)))
    body = panel(height) + heading(CONTENT_LEFT, 80, "How we work", "From idea to revenue.") + track + nodes
    return svg(height, "How we work: " + " → ".join(s[0] for s in STEPS), body)


def build_platforms():
    chips_left, row_h, row_gap, group_gap = CONTENT_LEFT, 40, 12, 30
    y, parts = 168, []
    for label, color, items in PLATFORM_GROUPS:
        parts.append(text(CONTENT_LEFT, y + 14, label.upper(), 14, MUTED, 700, extra='letter-spacing="1.5"'))
        y += 28
        x = chips_left
        for item in items:
            w = text_width(item, 17) + 50
            if x + w > CONTENT_RIGHT:
                x, y = chips_left, y + row_h + row_gap
            parts.append(chip(x, y, item, color)[1])
            x += w + 10
        y += row_h + group_gap
    height = y + 22
    body = panel(height) + heading(CONTENT_LEFT, 80, "Tech & platforms", "Tools we master.") + "".join(parts)
    label = "Tech and platforms: " + "; ".join(f"{g}: {', '.join(i)}" for g, _, i in PLATFORM_GROUPS)
    return svg(height, label, body)


def build_cta():
    height = 320
    defs = (f'<linearGradient id="ctabg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{RED_LIGHT}"/>'
            f'<stop offset=".55" stop-color="{RED}"/><stop offset="1" stop-color="#4a0a2e"/></linearGradient>'
            f'<radialGradient id="ctaglow"><stop offset="0" stop-color="{NAVY}" stop-opacity=".75"/><stop offset="1" stop-color="{NAVY}" stop-opacity="0"/></radialGradient>')
    radar = "".join(f'<circle cx="990" cy="164" r="{r}" fill="none" stroke="#fff" stroke-opacity=".1"/>' for r in (120, 190, 260, 330))
    body = (f'<clipPath id="clip"><rect width="{WIDTH}" height="{height}" rx="28"/></clipPath>'
            f'<g clip-path="url(#clip)"><rect width="{WIDTH}" height="{height}" fill="url(#ctabg)"/>'
            f'<rect width="{WIDTH}" height="{height}" fill="url(#grid)"/>{radar}'
            f'<circle cx="1120" cy="{height}" r="420" fill="url(#ctaglow)"/></g>'
            + text(70, 132, "Ready to turn your words", 48, "#fff", 800, extra='letter-spacing="-1"')
            + text(70, 192, "into sales?", 48, "#fff", 800, extra='letter-spacing="-1"')
            + text(70, 244, "Fair, transparent pricing · mostly fixed prices · one team", 19, "#fff", 500, extra='fill-opacity=".85"')
            + '<rect class="ring" x="850" y="128" width="280" height="72" rx="36" fill="none" stroke="#fff" stroke-width="2"/>'
            + '<rect x="850" y="128" width="280" height="72" rx="36" fill="#fff" filter="url(#shadow)"/>'
            + text(990, 172, "Start your project  →", 22, NAVY, 800, "middle"))
    return svg(height, "Ready to turn your words into sales? Start your project.", body, defs)


def build_buttons():
    outputs = {}
    for name, label, icon_name, color in BUTTONS:
        width = round(58 + text_width(label, 18) + 26)
        body = (f'<rect x="1" y="1" width="{width - 2}" height="54" rx="27" fill="#0b2a5c" stroke="#fff" stroke-opacity=".16"/>'
                f'<circle cx="28" cy="28" r="18" fill="{color}"/>'
                + icon(icon_name, 18.4, 18.4, .6, "#fff", 3)
                + text(56, 34, label, 18, "#fff", 700))
        outputs[name] = svg(56, label, body, width=width)
    return outputs


def main():
    outputs = {"hero": build_hero(), "stats": build_stats(), "services": build_services(),
               "process": build_process(), "platforms": build_platforms(), "cta": build_cta(),
               **build_buttons()}
    ASSETS.mkdir(exist_ok=True)
    for name, content in outputs.items():
        ET.fromstring(content)  # fail fast on malformed XML
        (ASSETS / f"{name}.svg").write_text(content, encoding="utf-8")
    print(f"wrote {len(outputs)} SVGs to {ASSETS}")


if __name__ == "__main__":
    main()
