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

# Rendered as a code object in the editor card (str -> string, list -> array, bool -> boolean).
CODE_OBJECT = [
    ("hq", "Berlin, DE"),
    ("backend", ["PHP", "Laravel", "Node.js"]),
    ("frontend", ["JavaScript", "AngularJS", "HTML5", "CSS3"]),
    ("mobile", ["iOS", "Android", "Hybrid"]),
    ("commerce", ["Shopify", "WooCommerce", "Magento", "JTL", "Afterbuy"]),
    ("builds", ["web apps", "shops", "ERP", "CRM", "APIs", "AI"]),
    ("openToProjects", True),
]

SERVICES = [
    ("web", "Web Applications", ["Laravel & Node.js backends,", "JavaScript / AngularJS frontends,", "responsive by default."], ("#ff2a40", "#ff7a2a")),
    ("cart", "Commerce Engineering", ["Shopify, WooCommerce, Magento,", "Gambio & xt:Commerce builds,", "custom plugins and themes."], ("#ff8a00", "#fbbc05")),
    ("database", "Custom Software", ["Tailor-made ERP, CRM & CMS,", "database design and business", "process automation."], ("#2f6bff", "#5b3df5")),
    ("plug", "APIs & Integrations", ["JTL Wawi, Afterbuy, Amazon", "& eBay connections — data", "synced between systems."], ("#16c784", "#0ea5a4")),
    ("phone", "Mobile Apps", ["Native iOS & Android and", "hybrid apps, shipped to the", "App Store & Play Store."], ("#a245ff", "#ff3d9a")),
    ("spark", "AI Solutions", ["Custom AI integrations that", "are practical and measurable", "in real workflows."], ("#ff2a40", "#a245ff")),
]

STEPS = [("Spec", "Requirements &", "architecture"),
         ("Build", "Clean code under", "version control"),
         ("Test", "QA & code review", "before release"),
         ("Ship", "Deploy, monitor", "& maintain")]

PLATFORM_GROUPS = [
    ("Backend", RED_LIGHT, ["PHP", "Laravel", "Node.js", "Databases", "REST APIs", "Automation"]),
    ("Frontend", "#2f6bff", ["JavaScript", "AngularJS", "HTML5", "CSS3", "Responsive UI"]),
    ("Mobile", "#a245ff", ["iOS (native)", "Android (native)", "Hybrid apps"]),
    ("Commerce", "#fbbc05", ["Shopify", "WooCommerce", "Magento", "Gambio", "xt:Commerce", "JTL Wawi & Shop", "Afterbuy"]),
    ("CMS", "#16c784", ["WordPress", "TYPO3", "Joomla"]),
    ("Integrations & tracking", "#ff7a2a", ["Amazon", "eBay", "Google Tag Manager", "Google Analytics", "Matomo"]),
]

CODE_FONT = "'SFMono-Regular', Menlo, Consolas, 'Liberation Mono', monospace"
SYNTAX = {"kw": RED_LIGHT, "name": "#ffd166", "prop": "#7dd3fc", "str": "#a5e075",
          "punct": "#c9d2e3", "bool": "#fbbc05", "comment": "#6b7a99"}

TERMINAL_LOG = [("a3f9c21", "Laravel web app with custom CRM"),
                ("7be104d", "Shopify store synced with JTL Wawi"),
                ("c91e5aa", "native iOS & Android app release"),
                ("4d2b8f0", "REST API for Amazon & eBay listings"),
                ("e18c7b3", "AI assistant built into the workflow")]
TERM = {"ok": "#34d399", "dir": "#7dd3fc", "git": "#5b8cff", "branch": RED_LIGHT, "cmd": "#ffffff",
        "out": "#c9d2e3", "hash": "#fbbc05", "type": "#a5e075", "msg": "#e6ebf5", "star": RED_LIGHT}

ARCH_CLIENTS = [("web", "Web App", "Laravel · JavaScript"), ("cart", "Webshop", "Shopify · WooCommerce"),
                ("phone", "Mobile App", "iOS · Android · Hybrid")]
ARCH_CORE = [("spark", "AI Services", "Automation & assistants", 200, 60),
             ("code", "API & Backend", "PHP · Laravel · Node.js", 298, 120),
             ("database", "Database", "ERP · CRM · CMS data", 456, 60)]
ARCH_INTEGRATIONS = [("JTL Wawi", "#3f7be0"), ("Afterbuy", "#ff7a2a"), ("Amazon", "#FF9900"),
                     ("eBay", "#e53238"), ("Analytics", "#a245ff")]

PRINCIPLES = [("lint", "Clean, readable code"), ("review", "Code review on every change"),
              ("test", "QA before each release"), ("git", "Everything version-controlled"),
              ("security", "Secure & GDPR-aware"), ("perf", "Fast & responsive by default"),
              ("docs", "Documented & handed over"), ("deploy", "Shipped, monitored, maintained")]

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
    "database": '<ellipse cx="16" cy="8" rx="10" ry="4"/><path d="M6 8v16c0 2.2 4.5 4 10 4s10-1.8 10-4V8M6 16c0 2.2 4.5 4 10 4s10-1.8 10-4"/>',
    "plug": '<path d="M12 4v7M20 4v7M8 11h16v5a8 8 0 0 1-16 0zM16 24v5"/>',
    "branch": '<circle cx="9" cy="7" r="3"/><circle cx="9" cy="25" r="3"/><circle cx="23" cy="10" r="3"/><path d="M9 10v12M23 13c0 6-14 4-14 9"/>',
    "check": '<path d="M8 16.5l5 5 11-11"/>',
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

ANIMATED = ".float,.float2,.float3,.pulse,.rise,.draw,.flow,.ring,.blink"
BASE_CSS = f"""
text {{ font-family: {FONT}; }}
.mono {{ font-family: {CODE_FONT}; }}
.blink {{ animation: blink 1.1s steps(1) infinite; }}
@keyframes blink {{ 50% {{ opacity: 0; }} }}
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


def hero_logo():
    """The brand lockup scaled up as the hero's only text; maps lockup point (70, 75) to (70, 320)."""
    scale = 2.6
    return f'<g transform="translate({70 - 70 * scale} {320 - 75 * scale}) scale({scale})">{brand_lockup()}</g>'


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
                 + f'<path d="{curve} V 492 H 670 Z" fill="url(#spark)"/>'
                 + f'<path class="draw" d="{curve}" fill="none" stroke="#34d399" stroke-width="3" stroke-linecap="round"/>'
                 + '<circle class="pulse" cx="882" cy="408" r="5" fill="#34d399"/></g>')
    order = ('<g class="float3" filter="url(#shadow)">'
             '<rect x="950" y="432" width="222" height="78" rx="18" fill="#0f2a57" stroke="#fff" stroke-opacity=".14"/>'
             '<circle cx="982" cy="471" r="19" fill="url(#accent)"/>'
             + icon("cart", 973.2, 462.2, .55, "#fff", 3)
             + '<rect x="1014" y="455" width="104" height="10" rx="5" fill="#fff" fill-opacity=".85"/>'
             + '<rect x="1014" y="475" width="132" height="8" rx="4" fill="#fff" fill-opacity=".3"/></g>')
    rating = ('<g class="float2" filter="url(#shadow)">'
              '<rect x="1010" y="84" width="166" height="66" rx="16" fill="#0f2a57" stroke="#fff" stroke-opacity=".14"/>'
              + text(1093, 126, "★★★★★", 24, "#fbbc05", 400, "middle") + '</g>')
    return analytics + order + rating


def build_hero():
    height = 640
    defs = (gradient("heroimg", "#1d3f7a", RED)
            + gradient("spark", "#34d399", "#0f2a57", vertical=True)
            + gradient("p0", RED_LIGHT, "#ff7a2a") + gradient("p1", "#2f6bff", "#5b3df5") + gradient("p2", "#16c784", "#0ea5a4"))
    bottom_bar = f'<rect y="{height - 8}" width="{WIDTH}" height="8" fill="url(#accent)"/>'
    body = panel(height, bottom_bar) + hero_logo() + browser_mock() + floating_cards()
    return svg(height, "List & Sell", body, defs)

# ---------------------------------------------------------------- sections


def window(x, y, w, h, fill, bar_h, clipped="", lights=True):
    """App-window chrome: shadowed rounded frame, tinted title bar, optional traffic lights."""
    dots = "".join(f'<circle cx="{x + 24 + i * 18}" cy="{y + bar_h / 2}" r="5" fill="{c}"/>'
                   for i, c in enumerate(["#ff5f57", "#febc2e", "#28c840"])) if lights else ""
    return (f'<clipPath id="win"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="16"/></clipPath>'
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="16" fill="{fill}" filter="url(#shadow)"/>'
            f'<g clip-path="url(#win)"><rect x="{x}" y="{y}" width="{w}" height="{bar_h}" fill="#fff" fill-opacity=".035"/>{clipped}</g>'
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="16" fill="none" stroke="#fff" stroke-opacity=".12"/>{dots}')


def code_text(x, y, tokens, palette, size):
    """One monospace line from (text, kind) tokens coloured via palette."""
    spans = "".join(f'<tspan fill="{palette[kind]}">{escape(s)}</tspan>' for s, kind in tokens)
    return f'<text x="{x}" y="{y}" font-size="{size}" class="mono" xml:space="preserve">{spans}</text>'


def value_tokens(value):
    if isinstance(value, bool):
        return [("true" if value else "false", "bool")]
    if isinstance(value, str):
        return [(f'"{value}"', "str")]
    tokens = [("[", "punct")]
    for i, item in enumerate(value):
        tokens += [(", ", "punct")] if i else []
        tokens.append((f'"{item}"', "str"))
    return tokens + [("]", "punct")]


def code_lines():
    lines = [[("// List & Sell GmbH — full-stack engineering team", "comment")],
             [("export const ", "kw"), ("listAndSell", "name"), (" = {", "punct")]]
    lines += [[("  " + key, "prop"), (": ", "punct"), *value_tokens(value), (",", "punct")] for key, value in CODE_OBJECT]
    return lines + [[("};", "punct")]]


def build_about():
    lines, line_h, win_y = code_lines(), 34, 160
    win_w = CONTENT_RIGHT - CONTENT_LEFT
    first_base = win_y + 44 + 40
    last_base = first_base + (len(lines) - 1) * line_h
    status_y = last_base + 30
    win_h = status_y + 32 - win_y
    height = status_y + 32 + 48
    code_x, char_w = CONTENT_LEFT + 76, 12.04  # monospace advance at 20px

    rows = []
    for i, tokens in enumerate(lines):
        y = first_base + i * line_h
        rows.append(f'<g class="rise" style="animation-delay:{i * .08:.2f}s">'
                    + text(CONTENT_LEFT + 48, y, str(i + 1), 17, "#4a5a7a", 500, "end", 'class="mono"')
                    + code_text(code_x, y, tokens, SYNTAX, 20) + '</g>')
    cursor_x = code_x + len("};") * char_w + 4
    highlight = f'<rect x="{CONTENT_LEFT}" y="{last_base - 24}" width="{win_w}" height="{line_h}" fill="#fff" fill-opacity=".04"/>'
    cursor = f'<rect class="blink" x="{cursor_x:.0f}" y="{last_base - 19}" width="11" height="24" fill="{RED_LIGHT}"/>'

    tab = (f'<rect x="{CONTENT_LEFT + 96}" y="{win_y + 8}" width="196" height="36" rx="8" fill="#0d2348"/>'
           f'<rect x="{CONTENT_LEFT + 110}" y="{win_y + 17}" width="20" height="18" rx="3" fill="#3178c6"/>'
           + text(CONTENT_LEFT + 120, win_y + 30, "TS", 10, "#fff", 800, "middle")
           + text(CONTENT_LEFT + 140, win_y + 31, "listandsell.ts", 15, "#e6ebf5", 500, extra='class="mono"'))
    status = (f'<rect x="{CONTENT_LEFT}" y="{status_y}" width="{win_w}" height="32" fill="url(#accent)"/>'
              + icon("branch", CONTENT_LEFT + 16, status_y + 8, .5, "#fff", 3.5)
              + text(CONTENT_LEFT + 38, status_y + 21, "main   ✓ 0 problems", 13, "#fff", 600, extra='xml:space="preserve"')
              + text(CONTENT_RIGHT - 16, status_y + 21, "TypeScript   UTF-8   LF", 13, "#fff", 600, "end", extra='xml:space="preserve"'))
    editor = (window(CONTENT_LEFT, win_y, win_w, win_h, "#071630", 44, highlight + status)
              + tab + "".join(rows) + cursor)
    body = panel(height) + heading(CONTENT_LEFT, 80, "Who we are", "Engineers who ship.") + editor
    label = "listandsell.ts: " + "; ".join(f"{k}: {v if not isinstance(v, list) else ', '.join(v)}" for k, v in CODE_OBJECT)
    return svg(height, label, body)


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
    body = panel(height) + heading(CONTENT_LEFT, 80, "What we build", "From backend to app store.") + "".join(cards)
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
    body = panel(height) + heading(CONTENT_LEFT, 80, "How we ship", "From spec to production.") + track + nodes
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
    body = panel(height) + heading(CONTENT_LEFT, 80, "Tech stack", "Tools we build with.") + "".join(parts)
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
            + text(70, 132, "Have a project to build?", 48, "#fff", 800, extra='letter-spacing="-1"')
            + text(70, 192, "Let's ship it.", 48, "#fff", 800, extra='letter-spacing="-1"')
            + text(70, 244, "Web · Shop · App · Software · AI — one engineering team", 19, "#fff", 500, extra='fill-opacity=".85"')
            + '<rect class="ring" x="850" y="128" width="280" height="72" rx="36" fill="none" stroke="#fff" stroke-width="2"/>'
            + '<rect x="850" y="128" width="280" height="72" rx="36" fill="#fff" filter="url(#shadow)"/>'
            + text(990, 172, "Start a project  →", 22, NAVY, 800, "middle"))
    return svg(height, "Have a project to build? Let's ship it.", body, defs)


def prompt(cmd=""):
    return [("➜  ", "ok"), ("listandsell ", "dir"), ("git:(", "git"), ("main", "branch"), (") ", "git"), (cmd, "cmd")]


def terminal_lines():
    lines = [prompt("whoami"), [("List & Sell GmbH · full-stack engineering team · Berlin, DE", "out")],
             prompt("git log --oneline -5")]
    for i, (sha, msg) in enumerate(TERMINAL_LOG):
        head = [(" (", "git"), ("HEAD -> ", "dir"), ("main", "branch"), (")", "git")] if i == 0 else []
        lines.append([("* ", "star"), (sha, "hash"), *head, (" feat:", "type"), (" " + msg, "msg")])
    deploy = [("✓ ", "ok"), ("build    ", "out"), ("✓ ", "ok"), ("tests    ", "out"),
              ("✓ ", "ok"), ("deploy    ", "out"), ("→ live in production", "ok")]
    return lines + [prompt("npm run deploy"), deploy, prompt()]


def build_terminal():
    lines, line_h, win_y, size = terminal_lines(), 34, 160, 19
    win_w = CONTENT_RIGHT - CONTENT_LEFT
    first_base = win_y + 40 + 40
    last_base = first_base + (len(lines) - 1) * line_h
    win_h = last_base + 30 - win_y
    height = win_y + win_h + 48
    code_x = CONTENT_LEFT + 28
    rows = "".join(f'<g class="rise" style="animation-delay:{i * .22:.2f}s">'
                   + code_text(code_x, first_base + i * line_h, tokens, TERM, size) + '</g>'
                   for i, tokens in enumerate(lines))
    cursor_x = code_x + sum(len(s) for s, _ in prompt()) * size * .602
    cursor = f'<rect class="blink" x="{cursor_x:.0f}" y="{last_base - 18}" width="11" height="23" fill="{RED_LIGHT}"/>'
    title = text(WIDTH / 2, win_y + 26, "zsh — ~/listandsell", 14, MUTED, 500, "middle", 'class="mono"')
    body = (panel(height) + heading(CONTENT_LEFT, 80, "Terminal", "Straight from the command line.")
            + window(CONTENT_LEFT, win_y, win_w, win_h, "#050b18", 40) + title + rows + cursor)
    label = "Terminal: whoami → List & Sell GmbH engineering team. Recent work: " + "; ".join(m for _, m in TERMINAL_LOG)
    return svg(height, label, body)


def arch_edge(d, color):
    return (f'<path d="{d}" fill="none" stroke="#fff" stroke-opacity=".14" stroke-width="2"/>'
            f'<path class="flow" d="{d}" fill="none" stroke="{color}" stroke-width="2.5" stroke-dasharray="6 30" stroke-linecap="round"/>')


def arch_node(x, y, w, h, icon_name, title, sub, grad, highlight=False):
    stroke = 'stroke="url(#accent)" stroke-width="2"' if highlight else 'stroke="#fff" stroke-opacity=".14"'
    tile_y = y + (h - 44) / 2
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="#0f2a57" {stroke} filter="url(#shadow)"/>'
            f'<rect x="{x + 16}" y="{tile_y}" width="44" height="44" rx="12" fill="url(#{grad})"/>'
            + icon(icon_name, x + 25.6, tile_y + 9.6, .8)
            + text(x + 74, y + h / 2 - 2, title, 22 if highlight else 18, "#fff", 800)
            + text(x + 74, y + h / 2 + 20, sub, 13, MUTED, 500))


def build_architecture():
    height, core_x, core_w, core_cy = 572, 460, 280, 358
    client_x, client_w, integ_x, integ_w = CONTENT_LEFT, 250, 912, 240
    grads = [("#ff2a40", "#ff7a2a"), ("#ff8a00", "#fbbc05"), ("#a245ff", "#ff3d9a"),
             ("#ff2a40", "#a245ff"), ("#2f6bff", "#5b3df5"), ("#16c784", "#0ea5a4")]
    defs = "".join(gradient(f"a{i}", *g) for i, g in enumerate(grads))
    client_cys = [248 + i * 110 for i in range(len(ARCH_CLIENTS))]
    integ_ys = [192 + i * 70 for i in range(len(ARCH_INTEGRATIONS))]

    edges = "".join(arch_edge(f"M{client_x + client_w} {cy} C 380 {cy}, 380 {core_cy}, {core_x} {core_cy}", RED_LIGHT) for cy in client_cys)
    edges += "".join(arch_edge(f"M{core_x + core_w} {core_cy} C 830 {core_cy}, 830 {y + 26}, {integ_x} {y + 26}", "#ff7a2a") for y in integ_ys)
    edges += arch_edge("M600 298V260", "#a245ff") + arch_edge("M600 418V456", "#2f6bff")

    clients = "".join(arch_node(client_x, cy - 36, client_w, 72, ic, t, s, f"a{i}") for i, ((ic, t, s), cy) in enumerate(zip(ARCH_CLIENTS, client_cys)))
    core = "".join(arch_node(core_x, y, core_w, h, ic, t, s, f"a{3 + i}", highlight=(i == 1))
                   for i, (ic, t, s, y, h) in enumerate(ARCH_CORE))
    integrations = "".join(
        f'<rect x="{integ_x}" y="{y}" width="{integ_w}" height="52" rx="26" fill="#0f2a57" stroke="#fff" stroke-opacity=".14"/>'
        f'<circle cx="{integ_x + 26}" cy="{y + 26}" r="7" fill="{color}"/>' + text(integ_x + 46, y + 32, name, 17, "#fff", 700)
        for (name, color), y in zip(ARCH_INTEGRATIONS, integ_ys))
    labels = "".join(text(x, 180, s, 13, MUTED, 700, a, 'letter-spacing="2"')
                     for x, s, a in [(client_x, "CLIENTS", "start"), (600, "CORE", "middle"), (integ_x, "INTEGRATIONS", "start")])
    body = (panel(height) + heading(CONTENT_LEFT, 80, "Architecture", "How our systems fit together.")
            + labels + edges + clients + core + integrations)
    label = ("Architecture: web app, webshop and mobile app clients connect to an API & backend (PHP, Laravel, Node.js) "
             "with database and AI services, integrated with " + ", ".join(n for n, _ in ARCH_INTEGRATIONS))
    return svg(height, label, body, defs)


def build_principles():
    win_y, header_h, row_h = 160, 84, 62
    win_w = CONTENT_RIGHT - CONTENT_LEFT
    per_col = (len(PRINCIPLES) + 1) // 2
    win_h = header_h + per_col * row_h + 16
    height = win_y + win_h + 48
    col_w = win_w / 2
    green = "#34d399"
    header = (f'<circle cx="{CONTENT_LEFT + 44}" cy="{win_y + 42}" r="18" fill="#16c784"/>'
              + icon("check", CONTENT_LEFT + 32.8, win_y + 30.8, .7, "#fff", 4)
              + text(CONTENT_LEFT + 76, win_y + 38, "All checks have passed", 22, "#fff", 800)
              + text(CONTENT_LEFT + 76, win_y + 62, f"{len(PRINCIPLES)} successful checks on main", 15, MUTED, 500)
              + f'<rect x="{CONTENT_RIGHT - 140}" y="{win_y + 26}" width="116" height="32" rx="16" fill="#16c784" fill-opacity=".15"/>'
              + text(CONTENT_RIGHT - 82, win_y + 47, "passing", 15, green, 700, "middle", 'class="mono"')
              + f'<path d="M{CONTENT_LEFT} {win_y + header_h}H{CONTENT_RIGHT}" stroke="#fff" stroke-opacity=".1"/>'
              + f'<path d="M{CONTENT_LEFT + col_w} {win_y + header_h}V{win_y + win_h}" stroke="#fff" stroke-opacity=".08"/>')
    rows = []
    for i, (job, desc) in enumerate(PRINCIPLES):
        x0 = CONTENT_LEFT + (i // per_col) * col_w
        cy = win_y + header_h + 8 + (i % per_col) * row_h + row_h / 2
        chip_w = len(job) * 9.03 + 24
        rows.append(f'<g class="rise" style="animation-delay:{i * .15:.2f}s">'
                    f'<circle cx="{x0 + 40}" cy="{cy}" r="13" fill="{green}" fill-opacity=".15" stroke="{green}" stroke-width="1.5"/>'
                    + icon("check", x0 + 32, cy - 8, .5, green, 4.5)
                    + f'<rect x="{x0 + 66}" y="{cy - 15}" width="{chip_w:.0f}" height="30" rx="7" fill="#fff" fill-opacity=".06"/>'
                    + text(x0 + 78, cy + 5, job, 15, "#e6ebf5", 600, extra='class="mono"')
                    + text(x0 + 80 + chip_w, cy + 6, desc, 17, "#e6ebf5", 500)
                    + text(x0 + col_w - 28, cy + 5, "passed", 14, green, 600, "end", 'class="mono"') + '</g>')
    body = (panel(height) + heading(CONTENT_LEFT, 80, "Engineering principles", "Every release passes the checks.")
            + window(CONTENT_LEFT, win_y, win_w, win_h, "#071630", header_h, lights=False) + header + "".join(rows))
    return svg(height, "Engineering principles: " + "; ".join(d for _, d in PRINCIPLES), body)


def build_activity():
    height = 150
    return svg(height, "Commit activity", panel(height) + heading(CONTENT_LEFT, 66, "Commit activity", "Always shipping."))


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
    outputs = {"hero": build_hero(), "about": build_about(), "terminal": build_terminal(),
               "services": build_services(), "architecture": build_architecture(), "process": build_process(),
               "principles": build_principles(), "platforms": build_platforms(), "activity": build_activity(),
               "cta": build_cta(), **build_buttons()}
    ASSETS.mkdir(exist_ok=True)
    for name, content in outputs.items():
        ET.fromstring(content)  # fail fast on malformed XML
        (ASSETS / f"{name}.svg").write_text(content, encoding="utf-8")
    print(f"wrote {len(outputs)} SVGs to {ASSETS}")


if __name__ == "__main__":
    main()
