#!/usr/bin/env python3
"""Generates the static LaafWeb pages (AF default / EN toggle). Run from repo root: python3 tools/build.py"""
import html, os, re
from urllib.parse import quote
E=lambda s: html.escape(s, quote=True)
ICONS={'chat': '<svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 12a8 8 0 0 1-11.7 7L4 20l1.1-4.2A8 8 0 1 1 21 12z"/></svg>', 'globe': '<svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3a14 14 0 0 1 0 18M12 3a14 14 0 0 0 0 18"/></svg>', 'bolt': '<svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M13 2 4 14h7l-1 8 9-12h-7z"/></svg>', 'image': '<svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="4" width="18" height="16" rx="2"/><circle cx="9" cy="10" r="2"/><path d="m21 16-5-5-8 9"/></svg>', 'form': '<svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="5" y="3" width="14" height="18" rx="2"/><path d="M9 8h6M9 12h6M9 16h3"/></svg>', 'pin': '<svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 21s7-6.2 7-11a7 7 0 0 0-14 0c0 4.8 7 11 7 11z"/><circle cx="12" cy="10" r="2.5"/></svg>', 'plus': '<svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="3"/><path d="M12 8v8M8 12h8"/></svg>', 'pen': '<svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 20h9"/><path d="M16.5 3.5a2.1 2.1 0 0 1 3 3L7 19l-4 1 1-4z"/></svg>'}
def T(af,en,tag="span",cls=None,extra=""):
    c=f' class="{cls}"' if cls else ""
    return f'<{tag}{c} data-af="{E(af)}" data-en="{E(en)}"{extra}>{af}</{tag}>'
WA_ICON='<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm0 18.2c-1.5 0-3-.4-4.2-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8s-.4-.1-.6.1-.6.8-.8 1-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.2-.4.2-.4.7-1.3.1-.2 0-.3 0-.5l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2c0 1.3.9 2.5 1 2.7s1.8 2.8 4.4 3.9c1.6.7 2.3.7 3.1.6.5-.1 1.5-.6 1.7-1.2s.2-1.1.2-1.2-.2-.2-.4-.3z"/></svg>'
LOGO='<svg width="36" height="36" viewBox="0 0 64 64" aria-hidden="true"><rect width="64" height="64" rx="15" fill="#0b4f33"/><rect x="11" y="14" width="42" height="30" rx="5" fill="#fff"/><rect x="16" y="19" width="20" height="4" rx="2" fill="#0e6b45"/><rect x="16" y="26" width="32" height="3" rx="1.5" fill="#cfd8d2"/><rect x="16" y="32" width="26" height="3" rx="1.5" fill="#cfd8d2"/><path d="M20 44v10l10-10z" fill="#fff"/><circle cx="46" cy="38" r="7" fill="#1faa59"/></svg>'
def wa(af,en,cls="btn wa",label=None,extra=""):
    lab=label or T("WhatsApp ons","WhatsApp us")
    return f'<a class="{cls}" href="https://wa.me/27636691391?text={quote(af)}" data-wa-af="{E(af)}" data-wa-en="{E(en)}" rel="noopener" target="_blank"{extra}>{WA_ICON}{lab}</a>'
def head(title,desc,page,canon):
    return f'''<!DOCTYPE html>
<html lang="af">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{E(desc)}">
<meta name="theme-color" content="#0b4f33">
<link rel="canonical" href="https://web.laafstyl.org/{canon}">
<link rel="icon" type="image/svg+xml" href="assets/favicon.svg">
<meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(desc)}"><meta property="og:type" content="website"><meta property="og:url" content="https://web.laafstyl.org/{canon}"><meta property="og:locale" content="af_ZA">
<link rel="stylesheet" href="assets/site.css">
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"ProfessionalService","name":"LaafWeb","description":"Eenbladsy-webwerwe vir klein besighede op die Weskus / One-page websites for small businesses on the West Coast","url":"https://web.laafstyl.org/","telephone":"+27636691391","areaServed":["Langebaan","Saldanha","Vredenburg","Velddrif","Paternoster","St Helena Bay"],"address":{{"@type":"PostalAddress","addressLocality":"Langebaan","addressRegion":"Western Cape","addressCountry":"ZA"}},"parentOrganization":{{"@type":"Organization","name":"BROD Traders (Pty) Ltd"}}}}</script>
</head>
<body>
<a class="skip" href="#main">{T("Spring na inhoud","Skip to content")}</a>
<header class="top"><div class="wrap nav">
<a class="brand" href="index.html" translate="no">{LOGO}<span class="bt">Laaf<em>Web</em></span></a>
<button class="burger" id="burger" aria-expanded="false" aria-controls="menu">{T("Kieslys","Menu")}</button>
<nav class="menu" id="menu" aria-label="Main">
<a class="l" href="index.html#wat" {'aria-current="page"' if page=='home' else ''}>{T("Wat jy kry","What you get")}</a>
<a class="l" href="index.html#hoe">{T("Hoe dit werk","How it works")}</a>
<a class="l" href="pricing.html" {'aria-current="page"' if page=='pricing' else ''}>{T("Pryse","Pricing")}</a>
<a class="l" href="contact.html" {'aria-current="page"' if page=='contact' else ''}>{T("Kontak","Contact")}</a>
<div class="lang" role="group" aria-label="Language"><button type="button" id="bAf" class="on" aria-label="Afrikaans">AF</button><button type="button" id="bEn" aria-label="English">EN</button></div>
{wa("Hallo LaafWeb, ek wil graag 'n webwerf vir my besigheid he.","Hi LaafWeb, I would like a website for my business.","btn wa sm",T("WhatsApp","WhatsApp"))}
</nav></div></header>
<main id="main">
'''
def foot():
    return f'''</main>
<footer><div class="wrap"><div class="cols">
<div><h4 translate="no">LaafWeb</h4><p>{T("Eenvoudige, netjiese webwerwe vir klein besighede op die Weskus. Gebou in Langebaan.","Simple, neat websites for small businesses on the West Coast. Built in Langebaan.")}</p>
<p>WhatsApp <a href="tel:+27636691391" data-tel><span data-cfg="waDisplay"></span></a> &middot; Mon&ndash;Sat 8:00&ndash;18:00<br><a href="mailto:laafstylfamily@gmail.com" data-mail><span data-cfg="email"></span></a></p></div>
<div><h4>{T("Blaaie","Pages")}</h4><a href="pricing.html">{T("Pryse","Pricing")}</a><br><a href="contact.html">{T("Kontak","Contact")}</a><br><a href="terms.html">{T("Voorwaardes","Terms")}</a><br><a href="privacy.html">{T("Privaatheid","Privacy")}</a></div>
<div><h4>{T("Areas","Areas")}</h4>Langebaan<br>Saldanha &middot; Vredenburg<br>Velddrif &middot; Paternoster<br>St Helena Bay</div>
</div>
<small>&copy; <span id="yr"></span> BROD Traders (Pty) Ltd, trading as LaafWeb &middot; Reg. 2025/529742/07 &middot; Langebaan, Western Cape</small></div></footer>
{wa("Hallo LaafWeb, ek wil graag 'n webwerf he.","Hi LaafWeb, I would like a website.","fab","WhatsApp")}
<script src="assets/site.js" defer></script>
</body>
</html>
'''
def card(ic,af_t,en_t,af_p,en_p):
    return f'<div class="card"><div class="ic" aria-hidden="true">{ic}</div><h3>{T(af_t,en_t)}</h3><p>{T(af_p,en_p)}</p></div>'
def step(af_t,en_t,af_p,en_p):
    return f'<div class="step"><h3>{T(af_t,en_t)}</h3><p>{T(af_p,en_p)}</p></div>'
def faq(af_q,en_q,af_a,en_a):
    return f'<details><summary>{T(af_q,en_q)}</summary><p>{T(af_a,en_a)}</p></details>'
MSG_AF="Hallo LaafWeb, ek wil graag 'n webwerf vir my besigheid he."
MSG_EN="Hi LaafWeb, I would like a website for my business."

def polish(x):
    x=x.replace("&#x27;","\u2019")
    return re.sub(r'>([^<>]+)<',lambda m:'>'+m.group(1).replace("'","\u2019")+'<',x)
# ---------------- HOME ----------------
home=head("LaafWeb | Webwerwe vir klein besighede op die Weskus","Netjiese, vinnige eenbladsy-webwerwe vir ambagsmanne en klein besighede. Van R949 eenmalig plus R79 per maand. Kliënte bereik jou op WhatsApp.","home","")
home+=f'''<section class="hero"><div class="wrap hgrid"><div>
<span class="eyebrow">{T("Gebou in Langebaan · Vir die Weskus","Built in Langebaan · For the West Coast")}</span>
<h1>{T("'n Webwerf wat vir jou <em>kliënte</em> werk.","A website that brings you <em>customers</em>.")}</h1>
<p class="lead">{T("Netjiese, vinnige eenbladsy-webwerwe vir ambagsmanne en klein besighede. Kliënte bereik jou met een tik op WhatsApp of 'n oproep.","Neat, fast one-page websites for tradesmen and small businesses. Customers reach you with one tap on WhatsApp or a call.")}</p>
<div class="cta">{wa(MSG_AF,MSG_EN,"btn wa",T("WhatsApp ons","WhatsApp us"))}<a class="btn ghost" href="pricing.html">{T("Sien pryse","See pricing")}</a></div>
<div class="pricepill"><span>{T("Eenbladsy-webwerf","One-page website")}</span><b>R949</b><span>{T("eenmalig +","once-off +")} <b style="font-size:1.1rem">R79</b> {T("per maand","a month")}</span></div>
</div>
<div aria-hidden="true"><div class="phone"><div class="screen"><div class="sh"><i></i><b>{T("Jou besigheid, netjies aanlyn","Your business, neatly online")}</b><small>{T("Gratis kwotasies · Jou dorp","Free quotes · Your town")}</small><span>{T("WhatsApp vir ons","WhatsApp us")}</span></div><div class="sb"><div><u></u><s></s></div><div><u></u><s></s></div><div><u></u><s></s></div></div><div class="badge">{T("Vra 'n kwotasie","Request a quote")}</div></div></div></div>
</div></section>

<section id="wat"><div class="wrap">
<h2>{T("Alles wat 'n klein besigheid nodig het","Everything a small business needs")}</h2>
<p class="sub">{T("Geen kompliseerde goed nie. Ons bou dit, jy gebruik dit.","Nothing complicated. We build it, you use it.")}</p>
<div class="grid">
{card(ICONS["chat"],"WhatsApp en bel-knoppies","WhatsApp and call buttons","Kliënte tik een knoppie en jy kry hul boodskap direk op jou foon.","Customers tap one button and their message lands straight on your phone.")}
{card(ICONS["globe"],"Afrikaans en Engels","Afrikaans and English","Jou webwerf praat jou kliënte se taal, met 'n skakelaar bo-aan.","Your website speaks your customers' language, with a switch at the top.")}
{card(ICONS["bolt"],"Vinnig en veilig","Fast and secure","Laai vinnig op selfone, met 'n veilige skakel (SSL) ingesluit.","Loads fast on phones, with a secure connection (SSL) included.")}
{card(ICONS["image"],"Jou dienste en foto's","Your services and photos","Wat jy doen, waar jy werk, en foto's van jou werk, netjies uiteengesit.","What you do, where you work, and photos of your work, clearly laid out.")}
{card(ICONS["form"],"Kwotasie-vorm","Quote form","Kliënte stuur hul besonderhede en dit kom as 'n WhatsApp-boodskap by jou uit.","Customers send their details and it reaches you as a WhatsApp message.")}
{card(ICONS["pin"],"Plaaslik gebou","Built locally","Ons ken die Weskus. Jy praat met 'n mens, nie 'n bot nie.","We know the West Coast. You deal with a person, not a bot.")}
</div></div></section>

<section class="alt" id="hoe"><div class="wrap">
<h2>{T("Hoe dit werk","How it works")}</h2>
<p class="sub">{T("Drie eenvoudige stappe, geen verrassings.","Three simple steps, no surprises.")}</p>
<div class="steps">
{step("Stuur ons 'n WhatsApp","Send us a WhatsApp","Se vir ons wat jy doen, waar jy werk, en stuur foto's of 'n logo as jy het.","Tell us what you do and where you work, and send photos or a logo if you have them.")}
{step("Ons bou 'n voorskou","We build a preview","Jy sien jou webwerf voordat dit lewendig gaan en vra vir veranderinge.","You see your website before it goes live and ask for changes.")}
{step("Gaan lewendig","Go live","Jy keur dit goed, betaal en ons publiseer dit. Jou kliënte kan jou nou vind.","You approve it, pay and we publish it. Your customers can now find you.")}
</div></div></section>

<section><div class="wrap">
<h2>{T("Eerlike prys","Honest pricing")}</h2>
<p class="sub">{T("Een bladsy, alles ingesluit, geen kontrak nie.","One page, everything included, no contract.")}</p>
<div class="plans" style="max-width:760px">
<div class="plan hot"><span class="tag">{T("Meeste besighede begin hier","Where most businesses start")}</span><h3>{T("Eenbladsy-webwerf","One-page website")}</h3><p class="for">{T("Vir ambagsmanne en klein besighede wat gevind wil word.","For tradesmen and small businesses that want to be found.")}</p>
<div class="amt">R949 <small>{T("eenmalig","once-off")}</small></div><div class="once">+ R79 {T("per maand vir gasheerdiens en klein veranderinge","a month for hosting and small updates")}</div>
<a class="btn dark" href="pricing.html">{T("Sien wat ingesluit is","See what's included")}</a></div>
</div></div></section>

<section class="alt" id="werk"><div class="wrap">
<h2>{T("Ons werk","Our work")}</h2>
<p class="sub">{T("Sien hoe 'n LaafWeb-webwerf lyk. Die drie voorbeelde is voorbeeldontwerpe, nie regte besighede nie. 735 Auto is 'n regte, lewendige webwerf.","See what a LaafWeb website looks like. The three samples are example designs, not real businesses. 735 Auto is a real, live website.")}</p>
<div class="work">
<a class="wk wl" href="https://auto.laafstyl.org" rel="noopener"><span class="tag">{T("Regte webwerf","Live website")}</span><h3>735 Auto</h3><p>{T("Motorwasplek. Dienste, pryse en WhatsApp-bespreking.","Car wash. Services, prices and WhatsApp booking.")}</p><span class="go">{T("Besoek webwerf","Visit website")} &rarr;</span></a>
<a class="wk wl" href="https://lw-sample-plumber.pages.dev" rel="noopener"><span class="tag">{T("Voorbeeld","Sample")}</span><h3>{T("Loodgieter","Plumber")}</h3><p>{T("Voorbeeldontwerp vir loodgieters en ander noodhulpdienste.","Example design for plumbers and other call-out trades.")}</p><span class="go">{T("Sien voorbeeld","See sample")} &rarr;</span></a>
<a class="wk wl" href="https://lw-sample-painter.pages.dev" rel="noopener"><span class="tag">{T("Voorbeeld","Sample")}</span><h3>{T("Verwer","Painter")}</h3><p>{T("Voorbeeldontwerp vir verwers en dekorateurs, met 'n foto-galery.","Example design for painters and decorators, with a photo gallery.")}</p><span class="go">{T("Sien voorbeeld","See sample")} &rarr;</span></a>
<a class="wk wl" href="https://lw-sample-salon.pages.dev" rel="noopener"><span class="tag">{T("Voorbeeld","Sample")}</span><h3>{T("Haarsalon","Hair salon")}</h3><p>{T("Voorbeeldontwerp vir salonne, met pryslys en bespreking.","Example design for salons, with a price list and booking.")}</p><span class="go">{T("Sien voorbeeld","See sample")} &rarr;</span></a>
</div>
<p style="margin-top:22px">{T("Wil jy een van ons eerste kliënte wees? Praat met ons oor 'n goeie ooreenkoms.","Want to be one of our first clients? Talk to us about a good deal.")} {wa(MSG_AF,MSG_EN,"btn wa sm",T("WhatsApp ons","WhatsApp us"))}</p>
</div></section>

<section><div class="wrap faq" style="max-width:860px">
<h2>{T("Gereelde vrae","Common questions")}</h2><p class="sub">{T("Kort en reguit antwoorde.","Short, straight answers.")}</p>
{faq("Hoe lank neem dit?","How long does it take?","Gewoonlik 'n paar dae nadat ons jou besonderhede en foto's het. Ons wys eers 'n voorskou.","Usually a few days after we have your details and photos. We show you a preview first.")}
{faq("Is daar 'n kontrak?","Is there a contract?","Nee. Die maandelikse fooi kan enige tyd gekanselleer word. Sien ons voorwaardes vir die detail.","No. The monthly fee can be cancelled at any time. See our terms for the detail.")}
{faq("Hoekom R79 per maand?","Why R79 a month?","Dit dek gasheerdiens, die veilige skakel en een klein verandering per maand (soos 'n nuwe foto of foonnommer).","It covers hosting, the secure connection and one small change a month (like a new photo or phone number).")}
{faq("Kry ek my eie domeinnaam?","Do I get my own domain name?","Jou webwerf kry 'n gratis adres. 'n Eie .co.za-domein kan bygevoeg word teen koste (vanaf ongeveer R150 per jaar).","Your site gets a free address. Your own .co.za domain can be added at cost (from about R150 a year).")}
{faq("Hoe betaal ek?","How do I pay?","Per EFT of kaart. Vir die maandelikse fooi stuur ons 'n veilige betaalskakel of ons gee jou ons bankbesonderhede.","By EFT or card. For the monthly fee we send a secure payment link, or give you our bank details.")}
{faq("Wie is LaafWeb?","Who is LaafWeb?","'n Plaaslike diens van BROD Traders (Pty) Ltd in Langebaan. Jy praat direk met die mense wat jou webwerf bou.","A local service of BROD Traders (Pty) Ltd in Langebaan. You talk directly to the people who build your website.")}
</div></section>

<section class="dark-sec"><div class="wrap" style="text-align:center">
<h2 style="color:#fff">{T("Gereed om gevind te word?","Ready to be found?")}</h2>
<p class="sub" style="margin:0 auto 22px">{T("Stuur ons net 'n WhatsApp. Ons antwoord Maandag tot Saterdag, 8:00 tot 18:00.","Just send us a WhatsApp. We reply Monday to Saturday, 8:00 to 18:00.")}</p>
{wa(MSG_AF,MSG_EN,"btn wa",T("WhatsApp ons nou","WhatsApp us now"))}
</div></section>
'''
home+=foot()
open("index.html","w").write(polish(home))

# ---------------- PRICING ----------------
def li(af,en,no=False): return f'<li{" class=\"no\"" if no else ""}>{T(af,en)}</li>'
pr=head("Pryse | LaafWeb","Eenbladsy-webwerf R949 eenmalig plus R79 per maand. Groter webwerwe op aanvraag. Geen kontrak.","pricing","pricing.html")
pr+=f'''<section class="hero" style="padding:48px 0 30px"><div class="wrap"><span class="eyebrow">{T("Pryse","Pricing")}</span><h1>{T("Eenvoudige, <em>eerlike</em> pryse.","Simple, <em>honest</em> pricing.")}</h1><p class="lead">{T("Alle pryse in rand. Geen kontrak, geen versteekte fooie. Ons wys jou 'n voorskou voordat jy betaal.","All prices in rand. No contract, no hidden fees. We show you a preview before you pay.")}</p></div></section>
<section style="padding-top:20px"><div class="wrap"><div class="plans">
<div class="plan hot"><span class="tag">{T("Begin hier","Start here")}</span><h3>{T("Eenbladsy","One-page")}</h3><p class="for">{T("Vir ambagsmanne en klein besighede.","For tradesmen and small businesses.")}</p>
<div class="amt">R949 <small>{T("eenmalig","once-off")}</small></div><div class="once">+ <b>R79</b> {T("per maand","a month")}</div>
<ul>{li("1 netjiese blad, selfoon-eerste ontwerp","1 neat page, mobile-first design")}{li("WhatsApp-, bel- en kwotasie-knoppies","WhatsApp, call and quote buttons")}{li("Afrikaans en Engels met skakelaar","Afrikaans and English with a switch")}{li("Jou dienste, areas en foto's","Your services, areas and photos")}{li("Gratis webadres (jouwenaam.pages.dev)","Free web address (yourname.pages.dev)")}{li("Veilige skakel (SSL) en vinnige gasheerdiens","Secure connection (SSL) and fast hosting")}{li("Een klein verandering per maand","One small change a month")}{li("Eie .co.za-domein","Your own .co.za domain",True)}</ul>
{wa("Hallo LaafWeb, ek stel belang in die Eenbladsy-webwerf (R949 + R79 pm).","Hi LaafWeb, I am interested in the One-page website (R949 + R79 pm).","btn wa",T("Begin op WhatsApp","Start on WhatsApp"))}</div>
<div class="plan"><h3>{T("Besigheid (meer bladsye)","Business (more pages)")}</h3><p class="for">{T("Vir besighede met meer dienste, 'n galery of kaart.","For businesses with more services, a gallery or a map.")}</p>
<div class="amt" style="font-size:1.9rem">{T("Op aanvraag","On request")}</div><div class="once">{T("Ons kwoteer volgens wat jy nodig het","We quote according to what you need")}</div>
<ul>{li("Tot ongeveer 5 bladsye","Up to about 5 pages")}{li("Fotogalery van jou werk","Photo gallery of your work")}{li("Google Maps en Google Besigheidsprofiel","Google Maps and Google Business Profile")}{li("Basiese soekenjin-opstelling (SEO)","Basic search-engine setup (SEO)")}{li("Eie domein en e-pos op aanvraag","Own domain and email on request")}</ul>
{wa("Hallo LaafWeb, ek wil graag 'n kwotasie vir 'n groter webwerf.","Hi LaafWeb, I would like a quote for a larger website.","btn ghost",T("Vra 'n kwotasie","Request a quote"))}</div>
</div></div></section>

<section class="alt"><div class="wrap">
<h2>{T("Byvoegings","Add-ons")}</h2><p class="sub">{T("Net as jy dit nodig het.","Only if you need them.")}</p>
<div class="grid">
{card(ICONS["globe"],"Eie .co.za-domein","Your own .co.za domain","Ons registreer dit vir jou, teen koste (vanaf ongeveer R150 per jaar).","We register it for you, at cost (from about R150 a year).")}
{card(ICONS["plus"],"Ekstra bladsy","Extra page","R350 per bladsy by die Eenbladsy-pakket.","R350 per page added to the One-page package.")}
{card(ICONS["pin"],"Google Besigheidsprofiel","Google Business Profile","Dat jy op Google Maps en in 'naby my'-soektogte wys. Prys op aanvraag.","So you show up on Google Maps and in 'near me' searches. Price on request.")}
{card(ICONS["pen"],"Logo","Logo","Eenvoudige logo vir jou besigheid. Prys op aanvraag.","A simple logo for your business. Price on request.")}
</div></div></section>

<section><div class="wrap" style="max-width:860px">
<h2>{T("Hoe betaling werk","How payment works")}</h2>
<div class="faq">
{faq("Wanneer betaal ek die R949?","When do I pay the R949?","Nadat jy die voorskou goedgekeur het en voordat ons dit publiseer. Per EFT of kaart.","After you approve the preview and before we publish it. By EFT or card.")}
{faq("En die R79 per maand?","And the R79 a month?","Ons stuur jou 'n veilige betaalskakel vir 'n maandelikse betaling, of jy betaal per EFT. Jy kan enige tyd kanselleer.","We send you a secure payment link for a monthly payment, or you pay by EFT. You can cancel at any time.")}
{faq("Wat as ek kanselleer?","What if I cancel?","Die webwerf bly aan tot die einde van die betaalde maand. Jy kan jou teks en foto's kry. Sien ons voorwaardes.","The website stays up until the end of the paid month. You can get your text and photos. See our terms.")}
</div>
<p class="note">{T("Pryse sluit alle toepaslike belasting in. Kyk ons <a href=\"terms.html\">voorwaardes</a> vir die volle detail.","Prices include any applicable tax. See our <a href=\"terms.html\">terms</a> for the full detail.")}</p>
</div></section>
'''
pr+=foot()
open("pricing.html","w").write(polish(pr))

# ---------------- CONTACT ----------------
ct=head("Kontak | LaafWeb","WhatsApp of bel LaafWeb in Langebaan. Maandag tot Saterdag 8:00 tot 18:00.","contact","contact.html")
ct+=f'''<section class="dark-sec" style="padding:56px 0"><div class="wrap"><h1 style="color:#fff;font-size:clamp(1.8rem,4vw,2.6rem)">{T("Kontak ons","Get in touch")}</h1>
<p class="sub">{T("WhatsApp is die vinnigste. Ons antwoord Maandag tot Saterdag, 8:00 tot 18:00.","WhatsApp is fastest. We reply Monday to Saturday, 8:00 to 18:00.")}</p>
<div class="cgrid"><div class="ci">
{wa(MSG_AF,MSG_EN,"",T("WhatsApp","WhatsApp"),' style="display:block;background:rgba(255,255,255,.1);padding:16px 18px;border-radius:14px;margin-bottom:12px;color:#fff;text-decoration:none"')}
<a href="tel:+27636691391" data-tel><small>{T("Bel","Call")}</small><strong data-cfg="waDisplay"></strong></a>
<a href="mailto:laafstylfamily@gmail.com" data-mail><small>E-pos / Email</small><strong data-cfg="email"></strong></a>
<div style="background:rgba(255,255,255,.1);padding:16px 18px;border-radius:14px;margin-bottom:12px"><small style="display:block;color:#bfe0cc;font-size:.8rem">{T("Areas","Areas")}</small><strong style="font-size:1.15rem">Langebaan &middot; Saldanha &middot; Vredenburg &middot; Velddrif</strong></div></div>
<form class="cform" id="qform"><h3 style="margin:0 0 14px">{T("Stuur ons jou besonderhede","Send us your details")}</h3>
<label for="n">{T("Jou naam","Your name")}</label><input id="n" name="name" autocomplete="name" required>
<label for="b">{T("Besigheid","Business")}</label><input id="b" name="business" autocomplete="organization">
<label for="p">{T("Jou nommer","Your number")}</label><input id="p" name="phone" type="tel" inputmode="tel" autocomplete="tel">
<label for="t">{T("Dorp","Town")}</label><input id="t" name="town" autocomplete="address-level2">
<label for="m">{T("Besonderhede","Details")}</label><textarea id="m" name="details" autocomplete="off" data-ph-af="Bv. ek sit PVC-plafonne op in Vredenburg…" data-ph-en="E.g. I fit PVC ceilings in Vredenburg…"></textarea>
<button class="btn wa" type="submit" style="width:100%">{WA_ICON}{T("Stuur op WhatsApp","Send on WhatsApp")}</button>
<p class="note" style="text-align:center;margin:10px 0 0">{T("Dit maak WhatsApp oop met jou boodskap reg om te stuur.","This opens WhatsApp with your message ready to send.")}</p></form></div></div></section>
'''
ct+=foot()
open("contact.html","w").write(polish(ct))

# ---------------- 404 ----------------
nf=head("Nie gevind nie | LaafWeb","Hierdie blad bestaan nie.","404","404.html")
nf+=f'''<section class="hero"><div class="wrap" style="text-align:center"><h1>{T("Hierdie blad is nie hier nie.","This page isn't here.")}</h1><p class="lead" style="margin:0 auto 22px">{T("Dalk is die skakel verouderd. Gaan terug na die tuisblad of WhatsApp ons.","The link may be out of date. Go back to the home page or WhatsApp us.")}</p><div class="cta" style="justify-content:center"><a class="btn dark" href="index.html">{T("Tuisblad","Home")}</a>{wa(MSG_AF,MSG_EN,"btn wa",T("WhatsApp ons","WhatsApp us"))}</div></div></section>'''
nf+=foot()
open("404.html","w").write(polish(nf))
print("built index, pricing, contact, 404")

# ---------------- TERMS ----------------
def sec(h,body): return f'<h2>{h}</h2>{body}'
terms=head("Voorwaardes | Terms | LaafWeb","LaafWeb dienstevoorwaardes: pryse, betaling, kansellasie, inhoud en aanspreeklikheid.","terms","terms.html")
terms+='''<section><div class="wrap legal"><span class="eyebrow">Legal / Wettig</span><h1 style="font-size:2.2rem">Terms of Service / Dienstevoorwaardes</h1>
<p class="note">Last updated: October 2026. These terms are in English. If something is unclear, WhatsApp us and we will explain it in Afrikaans or English.</p>'''
terms+=sec("1. Who we are","<p>LaafWeb is a service of BROD Traders (Pty) Ltd (Reg. 2025/529742/07), Langebaan, Western Cape, South Africa (&ldquo;we&rdquo;, &ldquo;us&rdquo;). By ordering a website or paying any amount to us, you (&ldquo;the client&rdquo;) agree to these terms.</p>")
terms+=sec("2. What we provide and prices","<p><b>One-page website:</b> R949 once-off setup plus R79 per month for hosting, the secure connection (SSL) and one small change a month. Includes a free web address (for example yourname.pages.dev), WhatsApp, call and quote buttons, and Afrikaans and English text where supplied.</p><p><b>Larger websites</b> and <b>add-ons</b> (extra pages, own domain, Google Business Profile, logo) are quoted in writing before we start. An extra page on the One-page package is R350. A .co.za domain is charged at cost.</p><p>All prices are in South African rand and include any applicable tax. We may change the monthly fee with at least 30 days' written notice; you may cancel before the change takes effect.</p>")
terms+=sec("3. Preview and approval","<p>We build a preview from the information, text and photos you give us. You may ask for reasonable changes to the preview. The setup fee is payable after you approve the preview and before we publish the website. If you decide not to proceed before approving and paying, you owe us nothing.</p>")
terms+=sec("4. Payment","<p>You may pay by EFT or card. The monthly fee is payable in advance for each month, either by EFT or by a secure recurring payment link that we send you, which is processed by our payment provider. We do not see or store your card details. If a payment fails, we will notify you and give at least 14 days before taking the website offline. The website will be restored when the amount is paid.</p>")
terms+=sec("5. Cancellation and refunds","<p>You may cancel the monthly service at any time by WhatsApp or email. Cancellation takes effect at the end of the month already paid. There are no cancellation fees or penalties. We do not give partial-month refunds. The setup fee is non-refundable once we have started building after your instruction to proceed. Where the law (including the Consumer Protection Act) gives you a right that these terms cannot limit, that right applies.</p>")
terms+=sec("6. Domains","<p>A domain we register for you is registered in your name. After cancellation, renewal is your responsibility; we will provide transfer instructions on request.</p>")
terms+=sec("7. Content and ownership","<p>You own your business name, logo, text and photos, and you confirm you have the right to use them and that they are lawful and accurate. You grant us permission to publish them on your website. We keep ownership of the design, code and templates we create. While you pay the monthly fee you may use the website. After cancellation you may ask for a copy of your text and photos within 30 days. If you want to own the website code, ask us for a written quote.</p>")
terms+=sec("8. Availability","<p>We aim to keep your website online but we do not guarantee uninterrupted service. We are not liable for downtime caused by hosting, domain, payment, internet or other third-party providers, or by events outside our control.</p>")
terms+=sec("9. Our work as an example","<p>We will only show your website or business name as an example of our work with your permission.</p>")
terms+=sec("10. Referrals","<p>If you introduce a new client and that client pays their setup fee, we will pay you R250 by EFT within 7 business days of receiving the payment. The new client must name you when they first contact us. Self-referrals do not qualify.</p>")
terms+=sec("11. Liability","<p>To the extent the law allows, our total liability to you is limited to the amounts you paid us in the three months before the event. We are not liable for indirect or consequential loss, such as lost profits.</p>")
terms+=sec("12. Privacy","<p>We handle personal information as set out in our <a href=\"privacy.html\">Privacy Policy</a>.</p>")
terms+=sec("13. General","<p>These terms are governed by the laws of the Republic of South Africa. Any dispute will first be discussed in good faith; failing that, the competent court in the Western Cape has jurisdiction. Contact: WhatsApp 063 669 1391, laafstylfamily@gmail.com.</p>")
terms+='</div></section>'
terms+=foot()
open("terms.html","w").write(polish(terms))

# ---------------- PRIVACY ----------------
pv=head("Privaatheid | Privacy | LaafWeb","Hoe LaafWeb persoonlike inligting hanteer (POPIA).","privacy","privacy.html")
pv+='''<section><div class="wrap legal"><span class="eyebrow">Legal / Wettig</span><h1 style="font-size:2.2rem">Privacy Policy / Privaatheidsbeleid</h1>
<p class="note">Last updated: October 2026. This policy is in English. WhatsApp us if you want it explained in Afrikaans.</p>'''
pv+=sec("1. Who we are","<p>LaafWeb is a service of BROD Traders (Pty) Ltd (Reg. 2025/529742/07), Langebaan, South Africa. We are the responsible party under the Protection of Personal Information Act, 4 of 2013 (POPIA).</p>")
pv+=sec("2. What we collect","<p>Only what you give us: your name, business name, phone or WhatsApp number, email address, town, and the text, logo and photos you want on your website. If you pay by EFT we see the payment confirmation; if you pay by card or recurring payment link, the payment provider processes your card details and we do not store them. This website does not use advertising trackers or analytics cookies. Our hosting provider keeps basic server logs (such as IP address and browser type).</p>")
pv+=sec("3. Why we use it","<p>To build, publish and support your website; to contact you about your order; to invoice and receive payment; and to meet legal duties. We only send marketing to people who contacted us or agreed to receive it, and you can opt out at any time by telling us.</p>")
pv+=sec("4. Who we share it with","<p>Only service providers we need: WhatsApp (Meta) and email for messages; our hosting provider (Cloudflare) to publish websites; a payment provider (such as PayFast) if you pay by card or payment link; and a domain registrar if you buy a domain. We do not sell your information.</p>")
pv+=sec("5. Security and retention","<p>We keep your information only as long as needed to provide the service and meet legal and accounting duties. We take reasonable steps to protect it, including secure connections and access controls.</p>")
pv+=sec("6. Your rights","<p>You may ask to see, correct or delete your personal information, or object to its use, by contacting us. You may complain to the Information Regulator: inforeg@justice.gov.za.</p>")
pv+=sec("7. Cookies and local storage","<p>We do not use cookies for tracking. Your browser stores your language choice (Afrikaans or English) locally so the site remembers it.</p>")
pv+=sec("8. Contact","<p>WhatsApp 063 669 1391, laafstylfamily@gmail.com. We may update this policy; the date at the top shows the latest version.</p>")
pv+='</div></section>'
pv+=foot()
open("privacy.html","w").write(polish(pv))
print("built terms, privacy")
