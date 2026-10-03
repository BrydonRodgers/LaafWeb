"""Turns the intermediate English+data-attribute pages from build.py into final static pages:
one crawlable page per language (/, /af/, /xh/, /zu/), with hreflang, canonical, OG/Twitter tags,
JSON-LD (business, offers, FAQ, breadcrumbs), sitemap with alternates, robots.txt and OG image.
Terms, privacy and 404 are English only."""
import html, json, os, re
from urllib.parse import quote

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://web.laafstyl.org"
LANGS = ["en", "af", "xh", "zu"]
LOCALE = {"en": "en_ZA", "af": "af_ZA", "xh": "xh_ZA", "zu": "zu_ZA"}
LABEL = {"en": "EN", "af": "AF", "xh": "XH", "zu": "ZU"}
NAME = {"en": "English", "af": "Afrikaans", "xh": "isiXhosa", "zu": "isiZulu"}
TRANSLATED = ["index.html", "pricing.html", "contact.html"]
LEGAL = ["terms.html", "privacy.html", "404.html"]
LASTMOD = "2026-10-04"

META = {
 "index.html": {
  "en": ("Small Business Websites in Langebaan | LaafWeb", "One-page websites for tradesmen and small businesses on the West Coast. From R949 once-off plus R79 a month. Customers reach you on WhatsApp."),
  "af": ("Webwerwe vir Klein Besighede in Langebaan | LaafWeb", "Eenbladsy-webwerwe vir ambagsmanne en klein besighede aan die Weskus. Vanaf R949 eenmalig plus R79 per maand. Kliënte bereik jou op WhatsApp."),
  "xh": ("Iiwebhusayithi Zamashishini Amancinci eLangebaan | LaafWeb", "Iiwebhusayithi zekhasi elinye zabasebenzi bezandla namashishini amancinci kunxweme lwaseNtshona. Ukusuka kuR949 kanye kuphela kunye ne-R79 ngenyanga. Abathengi bakufikelela kuWhatsApp."),
  "zu": ("Amawebhusayithi Amabhizinisi Amancane eLangebaan | LaafWeb", "Amawebhusayithi ekhasi elilodwa kubasebenzi bezandla nasemabhizinisini amancane Ogwini Lwentshonalanga. Kusukela ku-R949 kanye kuphela kanye ne-R79 ngenyanga. Amakhasimende akufinyelela ku-WhatsApp."),
 },
 "pricing.html": {
  "en": ("Website Prices from R949 | LaafWeb Langebaan", "One-page website R949 once-off plus R79 a month. Larger websites on request. No contract. Based in Langebaan on the West Coast."),
  "af": ("Webwerf Pryse vanaf R949 | LaafWeb Langebaan", "Eenbladsy-webwerf R949 eenmalig plus R79 per maand. Groter webwerwe op aanvraag. Geen kontrak. Gebaseer in Langebaan aan die Weskus."),
  "xh": ("Amaxabiso Ewebhusayithi Ukusuka kuR949 | LaafWeb", "Iwebhusayithi yekhasi elinye R949 kanye kuphela kunye ne-R79 ngenyanga. Iiwebhusayithi ezinkulu xa uzicela. Akukho sivumelwano. Siseleangebaan."),
  "zu": ("Izintengo Zewebhusayithi Kusukela ku-R949 | LaafWeb", "Iwebhusayithi yekhasi elilodwa R949 kanye kuphela kanye ne-R79 ngenyanga. Amawebhusayithi amakhulu uma uwacela. Asikho isivumelwano. Sise-Langebaan."),
 },
 "contact.html": {
  "en": ("Contact LaafWeb | Web Design in Langebaan", "WhatsApp or call LaafWeb in Langebaan. Monday to Saturday 8:00 to 18:00. Free quotes for West Coast businesses."),
  "af": ("Kontak LaafWeb | Webontwerp in Langebaan", "WhatsApp of bel LaafWeb in Langebaan. Maandag tot Saterdag 8:00 tot 18:00. Gratis kwotasies vir Weskus-besighede."),
  "xh": ("Qhagamshelana ne-LaafWeb | Uyilo Lwewebhusayithi eLangebaan", "Bhalela okanye utsalele i-LaafWeb eLangebaan. NgoMvulo ukuya kuMgqibelo 8:00 ukuya 18:00. Ikowuteyishini yasimahla kumashishini aseNtshona."),
  "zu": ("Xhumana ne-LaafWeb | Ukwakhiwa Kwewebhusayithi eLangebaan", "Bhalela noma shayela i-LaafWeb eLangebaan. NgoMsombuluko kuya kuMgqibelo 8:00 kuya ku-18:00. Izilinganiso zentengo zamahhala kumabhizinisi aseNtshonalanga."),
 },
 "terms.html": {"en": ("Terms of Service | LaafWeb", "LaafWeb terms of service: prices, payment, cancellation, content and liability.")},
 "privacy.html": {"en": ("Privacy Policy | LaafWeb", "How LaafWeb handles personal information (POPIA).")},
 "404.html": {"en": ("Page not found | LaafWeb", "This page does not exist.")},
}
CRUMB = {"index.html": "Home", "pricing.html": "Pricing", "contact.html": "Contact", "terms.html": "Terms", "privacy.html": "Privacy"}


def pref(lang):
    return "" if lang == "en" else "/" + lang


def url(lang, page):
    p = "" if page == "index.html" else page
    base = SITE + (pref(lang) + "/" if lang != "en" else "/")
    return base + p


def path_for(lang, page):
    p = "/" if page == "index.html" else "/" + page
    return (pref(lang) + p) if lang != "en" else p


def curly(x):
    return re.sub(r'>([^<>]+)<', lambda m: '>' + m.group(1).replace("'", "’") + '<', x)


T_RE = re.compile(r'<(?P<tag>\w+)(?P<pre>[^<>]*?)\s*data-en="(?P<en>[^"]*)" data-af="(?P<af>[^"]*)" data-xh="(?P<xh>[^"]*)" data-zu="(?P<zu>[^"]*)"(?P<post>[^<>]*)>(?P<inner>.*?)</(?P=tag)>', re.S)
WA_RE = re.compile(r'href="https://wa\.me/27636691391\?text=[^"]*" data-wa-en="([^"]*)" data-wa-af="([^"]*)" data-wa-xh="([^"]*)" data-wa-zu="([^"]*)"')
PH_RE = re.compile(r'placeholder="[^"]*" data-ph-en="([^"]*)" data-ph-af="([^"]*)" data-ph-xh="([^"]*)" data-ph-zu="([^"]*)"')


def apply_lang(src, lang):
    idx = {"en": 0, "af": 1, "xh": 2, "zu": 3}[lang]

    def t(m):
        val = html.unescape(m.group(lang))
        val = val.replace("'", "’")
        return f'<{m.group("tag")}{m.group("pre")}{m.group("post")}>{val}</{m.group("tag")}>'
    out = T_RE.sub(t, src)
    out = WA_RE.sub(lambda m: 'href="https://wa.me/27636691391?text=' + quote(html.unescape(m.group(idx + 1))) + '"', out)
    out = PH_RE.sub(lambda m: 'placeholder="' + html.escape(html.unescape(m.group(idx + 1)), quote=True) + '"', out)
    return out


def switcher(page, cur):
    items = []
    for l in LANGS:
        pg = page if page in TRANSLATED else "index.html"
        on = ' class="on" aria-current="true"' if l == cur else ""
        items.append(f'<a href="{path_for(l, pg)}" hreflang="{l}" lang="{l}" data-l="{l}"{on} aria-label="{NAME[l]}">{LABEL[l]}</a>')
    return '<div class="lang" role="group" aria-label="Language">' + "".join(items) + "</div>"


def faqs_of(final_html):
    out = []
    for q, a in re.findall(r'<details><summary>(.*?)</summary><p>(.*?)</p></details>', final_html, re.S):
        strip = lambda x: html.unescape(re.sub(r'<[^>]+>', '', x)).strip()
        out.append((strip(q), strip(a)))
    return out


def jsonld(page, lang, title, desc, final_html):
    biz = SITE + "/#business"
    graph = [
        {
            "@type": ["ProfessionalService", "LocalBusiness"], "@id": biz, "name": "LaafWeb",
            "alternateName": "LaafWeb by LaafStyl", "url": SITE + "/", "logo": SITE + "/assets/logo.png", "image": SITE + "/assets/og.png",
            "telephone": "+27636691391", "email": "laafstylfamily@gmail.com",
            "description": "One-page websites for tradesmen and small businesses on the West Coast of South Africa.",
            "priceRange": "R949 once-off + R79/month",
            "address": {"@type": "PostalAddress", "addressLocality": "Langebaan", "addressRegion": "Western Cape", "postalCode": "7357", "addressCountry": "ZA"},
            "geo": {"@type": "GeoCoordinates", "latitude": -33.0897, "longitude": 18.0356},
            "areaServed": [{"@type": "City", "name": n} for n in ["Langebaan", "Saldanha", "Vredenburg", "Velddrif", "Paternoster", "St Helena Bay"]],
            "knowsLanguage": ["en", "af", "xh", "zu"],
            "openingHoursSpecification": [{"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"], "opens": "08:00", "closes": "18:00"}],
            "parentOrganization": {"@type": "Organization", "name": "BROD Traders (Pty) Ltd", "url": "https://laafstyl.org"},
            "makesOffer": {
                "@type": "Offer", "name": "One-page website", "priceCurrency": "ZAR", "price": "949",
                "description": "One neat mobile-first page, WhatsApp and call buttons, hosting and one small change a month.",
                "priceSpecification": [
                    {"@type": "UnitPriceSpecification", "priceCurrency": "ZAR", "price": "949", "name": "Once-off setup"},
                    {"@type": "UnitPriceSpecification", "priceCurrency": "ZAR", "price": "79", "name": "Monthly hosting and updates", "billingDuration": "P1M", "billingIncrement": 1, "unitCode": "MON"},
                ],
            },
        },
        {"@type": "WebSite", "@id": SITE + "/#website", "url": SITE + "/", "name": "LaafWeb", "publisher": {"@id": biz}, "inLanguage": ["en", "af", "xh", "zu"]},
        {"@type": "WebPage", "@id": url(lang, page) + "#webpage", "url": url(lang, page), "name": title, "description": desc, "inLanguage": lang, "isPartOf": {"@id": SITE + "/#website"}, "about": {"@id": biz}},
    ]
    if page in ("pricing.html", "contact.html", "terms.html", "privacy.html"):
        graph.append({"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "LaafWeb", "item": url(lang, "index.html")},
            {"@type": "ListItem", "position": 2, "name": title.split(" | ")[0], "item": url(lang, page)}]})
    f = faqs_of(final_html)
    if f and page in ("index.html", "pricing.html"):
        graph.append({"@type": "FAQPage", "inLanguage": lang, "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in f]})
    return '<script type="application/ld+json">' + json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, separators=(",", ":")) + "</script>"


def head_block(page, lang, title, desc):
    esc = lambda x: html.escape(x, quote=True)
    lines = [f"<title>{html.escape(title)}</title>", f'<meta name="description" content="{esc(desc)}">']
    noindex = page == "404.html"
    lines.append('<meta name="robots" content="noindex,follow">' if noindex else '<meta name="robots" content="index,follow,max-image-preview:large">')
    if not noindex:
        lines.append(f'<link rel="canonical" href="{url(lang, page)}">')
    if page in TRANSLATED:
        for l in LANGS:
            lines.append(f'<link rel="alternate" hreflang="{l}" href="{url(l, page)}">')
        lines.append(f'<link rel="alternate" hreflang="x-default" href="{url("en", page)}">')
    lines += [
        f'<meta property="og:title" content="{esc(title)}">', f'<meta property="og:description" content="{esc(desc)}">',
        '<meta property="og:type" content="website">', f'<meta property="og:url" content="{url(lang, page)}">',
        f'<meta property="og:locale" content="{LOCALE[lang]}">', '<meta property="og:site_name" content="LaafWeb">',
        f'<meta property="og:image" content="{SITE}/assets/og.png">', '<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">',
        '<meta property="og:image:alt" content="LaafWeb: websites for small businesses on the West Coast">',
        '<meta name="twitter:card" content="summary_large_image">', f'<meta name="twitter:title" content="{esc(title)}">',
        f'<meta name="twitter:description" content="{esc(desc)}">', f'<meta name="twitter:image" content="{SITE}/assets/og.png">',
    ]
    return "\n".join(lines)


def strip_old_head(src):
    src = re.sub(r"<title>.*?</title>\n?", "", src, flags=re.S)
    src = re.sub(r'<meta name="description"[^>]*>\n?', "", src)
    src = re.sub(r'<link rel="canonical"[^>]*>\n?', "", src)
    src = re.sub(r'<meta property="og:[^>]*>(<meta property="og:[^>]*>)*\n?', "", src)
    src = re.sub(r'<script type="application/ld\+json">.*?</script>\n?', "", src, flags=re.S)
    return src


def render(src, page, lang):
    out = apply_lang(src, lang)
    meta = META[page].get(lang) or META[page]["en"]
    title, desc = meta
    out = strip_old_head(out)
    out = re.sub(r'<html lang="[a-z]+">', f'<html lang="{lang}">', out)
    out = re.sub(r'<div class="lang" role="group".*?</div>', switcher(page, lang), out, flags=re.S)
    if lang != "en":
        p = pref(lang)
        out = re.sub(r'href="(index|pricing|contact)\.html', lambda m: f'href="{p}/{m.group(1)}.html' if m.group(1) != "index" else f'href="{p}/', out)
        out = re.sub(r'href="(terms|privacy)\.html', r'href="/\1.html', out)
        out = out.replace('href="assets/', 'href="/assets/').replace('src="assets/', 'src="/assets/')
    # head block + JSON-LD after theme-color
    block = head_block(page, lang, title, desc)
    out = out.replace('<meta name="theme-color" content="#0b4f33">', '<meta name="theme-color" content="#0b4f33">\n' + block, 1)
    ld = jsonld(page, lang, title, desc, out)
    out = out.replace("</head>", ld + "\n</head>", 1)
    return curly(out)


def make_assets():
    from PIL import Image, ImageDraw, ImageFont
    fb = "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf"
    fr = "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf"
    if not os.path.exists(fr):
        fr = fb
    og = os.path.join(ROOT, "assets", "og.png")
    if not os.path.exists(og):
        W, H = 1200, 630
        im = Image.new("RGB", (W, H), "#0b4f33")
        d = ImageDraw.Draw(im)
        for y in range(H):
            c = int(0x0b + (0x14 - 0x0b) * y / H), int(0x4f + (0x7a - 0x4f) * y / H), int(0x33 + (0x4e - 0x33) * y / H)
            d.line([(0, y), (W, y)], fill=c)
        gm = Image.open(os.path.join(ROOT, "assets", "logo.png")).convert("RGBA").resize((150, 150), Image.LANCZOS)
        d.ellipse([70, 70, 230, 230], fill="#ffffff")
        im.paste(gm, (75, 75), gm)
        d.text((260, 100), "LaafWeb", font=ImageFont.truetype(fb, 96), fill="#ffffff")
        d.text((80, 270), "Websites for small businesses", font=ImageFont.truetype(fb, 64), fill="#ffffff")
        d.text((80, 350), "on the West Coast", font=ImageFont.truetype(fb, 64), fill="#8fe3b5")
        d.rounded_rectangle([80, 460, 835, 540], 40, fill="#ffffff")
        d.text((115, 475), "From R949 once-off + R79 a month", font=ImageFont.truetype(fb, 40), fill="#0b4f33")
        d.text((80, 565), "Built in Langebaan  ·  EN  AF  XH  ZU", font=ImageFont.truetype(fr, 28), fill="#d6efe1")
        im.save(og, optimize=True)


def sitemap():
    rows = []
    def alt(page):
        return "".join(f'<xhtml:link rel="alternate" hreflang="{l}" href="{url(l, page)}"/>' for l in LANGS) + f'<xhtml:link rel="alternate" hreflang="x-default" href="{url("en", page)}"/>'
    for page, pr in (("index.html", "1.0"), ("pricing.html", "0.9"), ("contact.html", "0.8")):
        for l in LANGS:
            rows.append(f'<url><loc>{url(l, page)}</loc><lastmod>{LASTMOD}</lastmod><priority>{pr}</priority>{alt(page)}</url>')
    for page in ("terms.html", "privacy.html"):
        rows.append(f'<url><loc>{url("en", page)}</loc><lastmod>{LASTMOD}</lastmod><priority>0.3</priority></url>')
    return '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n' + "\n".join(rows) + "\n</urlset>\n"


def run(pages, TR):
    make_assets()
    for page, src in pages.items():
        langs = LANGS if page in TRANSLATED else ["en"]
        for l in langs:
            out = render(src, page, l)
            dest = os.path.join(ROOT, pref(l).lstrip("/"), page)
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            open(dest, "w").write(out)
    open(os.path.join(ROOT, "sitemap.xml"), "w").write(sitemap())
    open(os.path.join(ROOT, "robots.txt"), "w").write("User-agent: *\nAllow: /\nDisallow: /signup.html\nDisallow: /payment.html\nDisallow: /payment-success.html\nDisallow: /payment-cancel.html\n\nSitemap: " + SITE + "/sitemap.xml\n")
    print("localized pages: " + ", ".join(f"{p}x{4 if p in TRANSLATED else 1}" for p in pages))
