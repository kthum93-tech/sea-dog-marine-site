#!/usr/bin/env python3
"""Sea Dog Marine static site generator.
Edit the CONFIG block, then run:  python3 build.py
Outputs plain .html pages, sitemap.xml, robots.txt and llms.txt into ./site
"""
import json, os, shutil, datetime

# ================= CONFIG (update before going live) =================
SITE_URL = "https://www.seadogmarinefl.com"   # TODO: real domain, no trailing slash
BIZ = "Sea Dog Marine"
TAGLINE = "Dock, Hull and Marine Repair"
PHONE_DISPLAY = "727-699-4920"
PHONE_E164 = "+17276994920"
EMAIL = ""            # TODO: add business email (leave blank to hide)
BASE_CITY = ""        # TODO: city Shea operates from, e.g. "St. Petersburg"
HOURS = [  # TODO: confirm. Must match Google + Apple listings exactly
    ("Mo,Tu,We,Th,Fr", "07:00", "18:00", "Monday to Friday: 7:00 AM to 6:00 PM"),
    ("Sa", "08:00", "14:00", "Saturday: 8:00 AM to 2:00 PM"),
]
SAME_AS = [  # TODO: paste Google Business Profile, Facebook, Instagram, Yelp URLs
]
# ====================================================================

TODAY = datetime.date.today().isoformat()
OUT = "site"

COUNTIES = {
    "pinellas": {
        "name": "Pinellas County",
        "slug": "pinellas-county-dock-seawall-cleaning",
        "cities": ["St. Petersburg", "Clearwater", "Largo", "Seminole", "Dunedin", "Tarpon Springs",
                   "Palm Harbor", "Treasure Island", "St. Pete Beach", "Madeira Beach", "Indian Rocks Beach",
                   "Redington Shores", "Belleair", "Gulfport", "Tierra Verde", "Oldsmar", "Safety Harbor"],
        "intro": "Pinellas County has more private docks and seawalls per mile of shoreline than almost anywhere in Florida. Between the Intracoastal, Boca Ciega Bay, Clearwater Harbor and Old Tampa Bay, warm salt water feeds fast barnacle and oyster growth on every piling, ladder and lift.",
        "local": "Canal homes in Snell Isle, Shore Acres, Isla del Sol, Island Estates and the beach towns see heavy growth on the waterline band of seawall caps and pilings. We clean from the water and the dock so your yard and landscaping stay untouched.",
    },
    "hillsborough": {
        "name": "Hillsborough County",
        "slug": "hillsborough-county-dock-seawall-cleaning",
        "cities": ["Tampa", "Davis Islands", "Harbour Island", "Apollo Beach", "Ruskin", "Gibsonton",
                   "Rocky Point", "Westshore", "South Tampa", "Riverview", "Town 'n' Country"],
        "intro": "From the canals of Apollo Beach to the bayfront homes of South Tampa and Davis Islands, Hillsborough County waterfront owners deal with brackish and salt water growth that shortens the life of docks, lifts and seawalls.",
        "local": "Apollo Beach and Ruskin canal communities see heavy oyster build up on seawalls and lift cradles. Hillsborough River and bay properties fight algae, slime and barnacles that make ladders and walkways dangerous.",
    },
    "manatee": {
        "name": "Manatee County",
        "slug": "manatee-county-dock-seawall-cleaning",
        "cities": ["Bradenton", "Palmetto", "Anna Maria Island", "Holmes Beach", "Bradenton Beach",
                   "Anna Maria", "Cortez", "Longboat Key", "Ellenton", "Terra Ceia", "Snead Island"],
        "intro": "Manatee County waterfront, from the Manatee River to Anna Maria Island and Longboat Key, combines strong tidal flow with warm Gulf water. That mix carries constant barnacle, oyster and algae growth onto docks, pilings and boat lifts.",
        "local": "Island homes on Anna Maria and Holmes Beach and river homes in Bradenton and Palmetto all benefit from a regular cleaning schedule, especially before and after storm season.",
    },
}

SERVICES = [
    {
        "slug": "dock-cleaning", "name": "Dock Cleaning", "img": "dock.jpg",
        "title": "Dock Cleaning in Tampa Bay | Sea Dog Marine",
        "desc": "Professional dock cleaning in Pinellas, Hillsborough and Manatee counties. We remove algae, mold, barnacles and marine growth from decking and framing. Free video inspection.",
        "h1": "Dock Cleaning in Pinellas, Hillsborough and Manatee Counties",
        "lead": "Slick, green dock boards are a fall hazard and a sign that wood and fasteners are breaking down. Sea Dog Marine deep cleans wood and composite docks, removing algae, mold, mildew, bird droppings and marine growth so your dock is safe, clean and ready to use.",
        "includes": ["Deck boards, walkways and stairs", "Fingers, T heads and platforms", "Cleats, bumpers and hardware", "Framing and stringers at the waterline", "Removal of algae, mold, mildew and growth", "Before and after photos of the work"],
        "why": "Growth holds moisture against wood and metal. Over time that means soft boards, rusted fasteners and a dock that has to be rebuilt years early. Regular cleaning lets you spot problems while they are still cheap to fix.",
        "faqs": [
            ("How often should a dock be cleaned in Tampa Bay?", "Most docks in Pinellas, Hillsborough and Manatee counties do best with a cleaning every 6 to 12 months. Shaded docks and docks in canals with low water flow may need it more often."),
            ("Will dock cleaning damage my wood or composite decking?", "No. We match the method to the material, using the right pressure and cleaning approach for pressure treated wood, hardwood and composite boards."),
            ("Do you clean under the dock too?", "Yes. We clean the framing and structure at the waterline, where barnacles and oysters attach, not just the walking surface."),
        ],
    },
    {
        "slug": "seawall-cleaning", "name": "Seawall Cleaning", "img": "seawall.jpg",
        "title": "Seawall Cleaning in Tampa Bay | Sea Dog Marine",
        "desc": "Seawall cleaning in Pinellas, Hillsborough and Manatee counties. We remove barnacles, oysters and algae from seawall faces and caps so you can see cracks before they spread.",
        "h1": "Seawall Cleaning in Pinellas, Hillsborough and Manatee Counties",
        "lead": "Your seawall protects your yard, your pool and your home. When it is covered in barnacles, oysters and algae, you cannot see the cracks, spalling or seepage that lead to costly failures. Sea Dog Marine strips marine growth from the wall face and cap so the wall looks right and you can see its true condition.",
        "includes": ["Seawall face cleaning down to the low tide line", "Seawall cap cleaning", "Barnacle and oyster removal", "Algae, slime and stain removal", "Visual condition check during cleaning", "Photo and video documentation"],
        "why": "Heavy oyster and barnacle growth hides cracks and joint failures. Cleaning the wall gives you, your insurer and your contractor a clear look at its condition before a small repair turns into a full replacement.",
        "faqs": [
            ("Is seawall cleaning worth it?", "Yes. A clean wall looks better, adds curb appeal to waterfront homes and, more importantly, lets you catch cracks and seepage early when repairs cost far less."),
            ("Can you clean a seawall below the water?", "We clean as far down the face as conditions allow and time our work with the tides to reach the band where most growth attaches."),
            ("Do you repair seawalls?", "We document what we see during cleaning and let you know if anything looks like it needs attention, so you can plan repairs with confidence."),
        ],
    },
    {
        "slug": "piling-cleaning", "name": "Piling Cleaning", "img": "after.jpg",
        "title": "Dock Piling Cleaning and Barnacle Removal | Sea Dog Marine",
        "desc": "Dock piling cleaning and barnacle removal across Tampa Bay. Sea Dog Marine removes oysters, barnacles and algae from wood and concrete pilings. Call or text 727-699-4920.",
        "h1": "Dock Piling Cleaning and Barnacle Removal",
        "lead": "Pilings carry the full weight of your dock and lift. Barnacles and oysters add weight, trap moisture and hide rot and marine borer damage. We clean pilings from the cap down through the tidal zone so they look new and you can see what condition they are really in.",
        "includes": ["Wood and concrete pilings", "Barnacle, oyster and algae removal", "Tidal zone cleaning", "Piling caps and tops", "Condition notes on soft spots or damage", "Ready for piling wraps if you choose"],
        "why": "The tidal zone is where pilings fail first. Cleaning it regularly, and wrapping pilings once they are clean, is the most affordable way to extend the life of a dock.",
        "faqs": [
            ("Why do pilings get so much barnacle growth?", "Tampa Bay water is warm and full of nutrients year round, so barnacle and oyster larvae settle on any hard surface in the tidal zone, especially pilings."),
            ("Should I wrap my pilings after cleaning?", "Wrapping clean pilings is one of the best ways to slow marine borers and rot. We can clean and wrap in the same visit."),
            ("Can you clean pilings without a boat?", "Yes. We work from the dock, the shoreline or the water depending on what your property needs."),
        ],
    },
    {
        "slug": "boat-lift-cleaning", "name": "Boat Lift Cleaning", "img": "lift.jpg",
        "title": "Boat Lift Cleaning in Tampa Bay | Sea Dog Marine",
        "desc": "Boat lift cleaning in Pinellas, Hillsborough and Manatee counties. We remove barnacles and growth from cradles, bunks, beams and cables so your lift runs smoothly.",
        "h1": "Boat Lift Cleaning in Pinellas, Hillsborough and Manatee Counties",
        "lead": "Marine growth on a boat lift adds weight, chews up bunk carpet, scratches hulls and stresses motors, cables and gearboxes. Sea Dog Marine cleans the whole lift so it works the way it should and protects your boat instead of damaging it.",
        "includes": ["Cradles, bunks and guide posts", "Beams, I beams and platforms", "Lift pilings", "Barnacle and oyster removal", "Visual check of cables and hardware", "Photos of any wear we notice"],
        "why": "A clean lift lowers wear on motors and cables, keeps bunks from scratching your hull and makes it easier to spot corrosion before something fails under load.",
        "faqs": [
            ("How often should a boat lift be cleaned?", "For most Tampa Bay lifts, every 6 to 12 months keeps growth under control. Lifts that sit lowered in the water grow faster and may need more frequent service."),
            ("Do you service lift motors or cables?", "We focus on cleaning and will point out worn cables, bunks or hardware we see so you can have them serviced."),
            ("Can you clean my lift with the boat on it?", "In many cases yes, depending on the lift type. We will confirm during your free video inspection."),
        ],
    },
    {
        "slug": "ladder-cleaning", "name": "Dock Ladder Cleaning", "img": "ladder.jpg",
        "title": "Dock Ladder Cleaning and Degrowth | Sea Dog Marine",
        "desc": "Dock ladder cleaning and degrowth across Tampa Bay. We remove barnacles, oysters and slime from swim and dock ladders so they are safe to use again.",
        "h1": "Dock Ladder Cleaning and Degrowth",
        "lead": "A ladder covered in barnacles and slime is dangerous. Sharp shells cut hands and feet and slippery rungs cause falls. Sea Dog Marine strips growth from aluminum, stainless and wood ladders so they are safe for swimming, diving and getting on and off your boat.",
        "includes": ["Aluminum, stainless and wood ladders", "Rungs, rails and mounting brackets", "Barnacle and oyster removal", "Slime and algae removal", "Check of mounts and fasteners"],
        "why": "Ladders are often the first thing kids and guests use at the dock. Keeping them clean is a quick, low cost way to make your waterfront safer.",
        "faqs": [
            ("Can a ladder cleaning be added to another service?", "Yes. Most customers add ladder cleaning to a dock, seawall or lift cleaning visit."),
            ("Will cleaning damage the ladder finish?", "No. We use methods suited to aluminum, stainless steel and wood to remove growth without harming the ladder."),
        ],
    },
    {
        "slug": "piling-wraps", "name": "Piling and Dock Protection Wraps", "img": "after.jpg",
        "title": "Piling Wraps and Dock Protection | Sea Dog Marine",
        "desc": "Piling wraps and dock protection in Pinellas, Hillsborough and Manatee counties. Protect wood pilings from marine borers, rot and growth. Free video inspection.",
        "h1": "Piling Wraps and Dock Protection",
        "lead": "Piling wraps seal wood pilings in the tidal zone, where marine borers, rot and growth do the most damage. Sea Dog Marine cleans each piling first, then installs protective wraps that help your dock last years longer.",
        "includes": ["Full cleaning before wrapping", "Protective wrap installation through the tidal zone", "Wraps for dock and boat lift pilings", "Neat, secure, finished look", "Recommendations on which pilings need it most"],
        "why": "Replacing a piling is expensive and disruptive. Wrapping is a fraction of that cost and is one of the best investments a waterfront owner can make in dock longevity.",
        "faqs": [
            ("Do piling wraps really work?", "Wraps create a barrier that blocks marine borers and slows rot in the tidal zone, which is where wood pilings usually fail first."),
            ("Can you wrap pilings that already have damage?", "We will assess each piling during the inspection. Sound pilings are great candidates. Pilings with heavy damage may need repair or replacement first."),
        ],
    },
    {
        "slug": "maintenance-plans", "name": "Maintenance Plans and Storm Prep", "img": "dock.jpg",
        "title": "Waterfront Maintenance Plans and Storm Prep | Sea Dog Marine",
        "desc": "Recurring dock, seawall, piling and boat lift maintenance plans plus storm prep and seasonal cleaning for Tampa Bay waterfront homes. Call or text 727-699-4920.",
        "h1": "Waterfront Maintenance Plans and Storm Prep",
        "lead": "The easiest way to keep a waterfront property looking great is to never let growth get out of hand. Sea Dog Marine maintenance plans put your dock, seawall, pilings, ladders and lift on a regular schedule, with storm prep and post storm cleanup built in.",
        "includes": ["Scheduled cleanings on a set interval", "Pre hurricane season inspection and cleaning", "Post storm debris and growth cleanup", "Photo report after every visit", "Priority scheduling for plan members", "Great for rentals, HOAs and part time owners"],
        "why": "Regular service costs less than heavy cleanups and catches damage early. For seasonal residents and rental owners, it means coming back to a clean, safe dock every time.",
        "faqs": [
            ("What does a waterfront maintenance plan include?", "Plans are built around your property and can include dock, seawall, piling, ladder and boat lift cleaning on a set schedule, plus storm prep and photo reports."),
            ("Do you work with HOAs and property managers?", "Yes. We service community docks, marinas and multi home seawalls across Pinellas, Hillsborough and Manatee counties."),
            ("What is included in storm prep?", "We clean and inspect your dock, pilings, lift and seawall before storm season and document their condition with photos, which can help with insurance claims later."),
        ],
    },
]

FAQ_HOME = [
    ("What areas does Sea Dog Marine serve?", "Sea Dog Marine serves waterfront homes and businesses in Pinellas, Hillsborough and Manatee counties, including St. Petersburg, Clearwater, Tampa, Apollo Beach, Bradenton and Anna Maria Island."),
    ("What marine growth do you remove?", "We remove algae, barnacles, oysters, mold, slime and other marine growth from docks, seawalls, pilings, ladders and boat lifts."),
    ("How does the free video inspection work?", "Text a short video or photos of your dock, seawall or lift to 727-699-4920. We review it and send back a recommendation and price, often the same day, with no site visit needed to get started."),
    ("How much does dock or seawall cleaning cost?", "Price depends on size, amount of growth and access. Send a free video inspection by text to 727-699-4920 for a fast, accurate quote."),
    ("Do you offer recurring maintenance?", "Yes. We offer maintenance plans with scheduled cleanings, storm prep and photo reports for homeowners, HOAs, rentals and marinas."),
]

# ------------------------------------------------------------------ helpers
def url(page):
    return SITE_URL + "/" + ("" if page == "index.html" else page)

def org_ref():
    return {"@id": SITE_URL + "/#business"}

def business_schema():
    areas = []
    for c in COUNTIES.values():
        areas.append({"@type": "AdministrativeArea", "name": c["name"] + ", FL"})
        for city in c["cities"]:
            areas.append({"@type": "City", "name": city + ", FL"})
    d = {
        "@context": "https://schema.org",
        "@type": ["HomeAndConstructionBusiness", "LocalBusiness"],
        "@id": SITE_URL + "/#business",
        "name": BIZ,
        "alternateName": "Sea Dog Marine Cleaning",
        "slogan": "Remove Growth. Restore. Protect.",
        "description": "Sea Dog Marine provides professional dock cleaning, seawall cleaning, piling cleaning and barnacle removal, boat lift cleaning, ladder degrowth, piling wraps and waterfront maintenance plans in Pinellas, Hillsborough and Manatee counties, Florida.",
        "url": SITE_URL + "/",
        "telephone": PHONE_E164,
        "image": SITE_URL + "/assets/og-flyer.jpg",
        "logo": SITE_URL + "/assets/logo.jpg",
        "priceRange": "$$",
        "address": {"@type": "PostalAddress", "addressRegion": "FL", "addressCountry": "US"},
        "areaServed": areas,
        "knowsAbout": ["dock cleaning", "seawall cleaning", "barnacle removal", "oyster removal", "piling cleaning", "piling wraps", "boat lift cleaning", "marine growth removal", "storm preparation for docks"],
        "openingHoursSpecification": [{"@type": "OpeningHoursSpecification", "dayOfWeek": [ {"Mo":"Monday","Tu":"Tuesday","We":"Wednesday","Th":"Thursday","Fr":"Friday","Sa":"Saturday","Su":"Sunday"}[x] for x in h[0].split(",")], "opens": h[1], "closes": h[2]} for h in HOURS],
        "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Marine Cleaning and Maintenance Services",
            "itemListElement": [{"@type": "Offer", "itemOffered": {"@type": "Service", "name": s["name"], "url": url(s["slug"] + ".html")}} for s in SERVICES]
            + [{"@type": "Offer", "price": "0", "priceCurrency": "USD", "itemOffered": {"@type": "Service", "name": "Free Video Inspection"}}]},
        "contactPoint": {"@type": "ContactPoint", "telephone": PHONE_E164, "contactType": "customer service", "areaServed": "US-FL", "availableLanguage": "English"},
    }
    if BASE_CITY:
        d["address"]["addressLocality"] = BASE_CITY
    if EMAIL:
        d["email"] = EMAIL
    if SAME_AS:
        d["sameAs"] = SAME_AS
    return d

def faq_schema(faqs):
    return {"@context": "https://schema.org", "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]}

def crumbs(items):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList",
            "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": url(p)} for i, (n, p) in enumerate(items)]}

def ld(obj):
    return '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False) + "</script>"

def faq_html(faqs):
    out = '<section class="faq"><h2>Frequently Asked Questions</h2>'
    for q, a in faqs:
        out += f"<details><summary>{q}</summary><p>{a}</p></details>"
    return out + "</section>"

NAV = [("Dock Cleaning", "dock-cleaning.html"), ("Seawalls", "seawall-cleaning.html"), ("Pilings", "piling-cleaning.html"),
       ("Boat Lifts", "boat-lift-cleaning.html"), ("Service Areas", "service-areas.html"), ("Blog", "blog.html"), ("Free Inspection", "free-video-inspection.html")]

def cta_block():
    return f"""<section class="cta"><div class="wrap cta-in">
<div><h2>Free Video Inspection</h2><p>Text a short video or a few photos of your dock, seawall, pilings or lift. We send back a recommendation and price, usually the same day.</p></div>
<div class="cta-btns"><a class="btn red" href="sms:{PHONE_E164}">Text {PHONE_DISPLAY}</a><a class="btn outline" href="tel:{PHONE_E164}">Call {PHONE_DISPLAY}</a></div>
</div></section>"""

def page(fname, title, desc, body, schemas, og_img="assets/og-flyer.jpg"):
    canonical = url(fname)
    svc_links = "".join(f'<li><a href="{s["slug"]}.html">{s["name"]}</a></li>' for s in SERVICES)
    area_links = "".join(f'<li><a href="{c["slug"]}.html">{c["name"]}</a></li>' for c in COUNTIES.values())
    hours = "<br>".join(h[3] for h in HOURS)
    nav = "".join(f'<a href="{p}">{n}</a>' for n, p in NAV)
    return f"""<!DOCTYPE html>
<html lang="en-US">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{canonical}">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta name="geo.region" content="US-FL">
<meta name="geo.placename" content="Tampa Bay">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{BIZ}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{SITE_URL}/{og_img}">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#0b2a4a">
<link rel="icon" href="assets/logo.jpg">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@700;800&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/style.css">
{''.join(ld(s) for s in schemas)}
</head>
<body>
<div class="topbar"><div class="wrap">Serving Pinellas, Hillsborough and Manatee Counties &nbsp;|&nbsp; <a href="tel:{PHONE_E164}">Call or Text {PHONE_DISPLAY}</a></div></div>
<header class="hdr"><div class="wrap hdr-in">
<a class="brand" href="index.html" aria-label="{BIZ} home"><img src="assets/logo.jpg" alt="{BIZ} logo" width="92" height="66"><span><b>{BIZ}</b><small>{TAGLINE}</small></span></a>
<nav>{nav}</nav>
<a class="btn red sm" href="sms:{PHONE_E164}">Text Us</a>
</div></header>
<main>
{body}
{cta_block()}
</main>
<footer class="ftr"><div class="wrap ftr-grid">
<div><h3>{BIZ}</h3><p>Professional marine cleaning and maintenance for docks, seawalls, pilings, ladders and boat lifts across Tampa Bay.</p>
<p><b>Phone:</b> <a href="tel:{PHONE_E164}">{PHONE_DISPLAY}</a> (call or text){'<br><b>Email:</b> <a href="mailto:'+EMAIL+'">'+EMAIL+'</a>' if EMAIL else ''}</p><p><b>Hours:</b><br>{hours}</p></div>
<div><h3>Services</h3><ul>{svc_links}<li><a href="free-video-inspection.html">Free Video Inspection</a></li></ul></div>
<div><h3>Service Areas</h3><ul>{area_links}<li><a href="service-areas.html">All cities we serve</a></li><li><a href="blog.html">Waterfront Maintenance Blog</a></li></ul></div>
</div><div class="wrap copy">&copy; {datetime.date.today().year} {BIZ}. All rights reserved.</div></footer>
<a class="float" href="sms:{PHONE_E164}">Text for a Free Video Inspection</a>
</body></html>"""

# ------------------------------------------------------------------ pages
pages = {}

# Home
svc_cards = "".join(f"""<a class="card" href="{s['slug']}.html"><img src="assets/{s['img']}" alt="{s['name']} by {BIZ} in Tampa Bay" loading="lazy" width="560" height="360"><div><h3>{s['name']}</h3><p>{s['desc'].split('. ')[1] if '. ' in s['desc'] else s['desc']}</p><span class="more">Learn more</span></div></a>""" for s in SERVICES)
county_cards = "".join(f"""<a class="area" href="{c['slug']}.html"><h3>{c['name']}</h3><p>{', '.join(c['cities'][:6])} and more</p></a>""" for c in COUNTIES.values())
home_body = f"""
<section class="hero"><div class="wrap hero-in">
<div class="hero-txt">
<p class="eyebrow">Tampa Bay Marine Cleaning and Maintenance</p>
<h1>Dock, Seawall and Piling Cleaning in Pinellas, Hillsborough and Manatee Counties</h1>
<p class="lead"><b>{BIZ}</b> removes algae, barnacles, oysters, mold and marine growth from docks, seawalls, pilings, ladders and boat lifts. We restore your waterfront and protect it so it lasts.</p>
<div class="hero-btns"><a class="btn red" href="sms:{PHONE_E164}">Text for a Free Video Inspection</a><a class="btn outline" href="tel:{PHONE_E164}">Call {PHONE_DISPLAY}</a></div>
<ul class="checks"><li>Free video inspections</li><li>Before and after photos</li><li>Maintenance plans</li></ul>
</div>
<div class="ba"><figure><img src="assets/before.jpg" alt="Dock piling covered in barnacles and oysters before cleaning" width="430" height="1000"><figcaption>Before</figcaption></figure><figure><img src="assets/after.jpg" alt="Dock piling after professional barnacle removal by {BIZ}" width="540" height="460"><figcaption>After</figcaption></figure></div>
</div></section>

<section class="wrap answer">
<h2>What does {BIZ} do?</h2>
<p>{BIZ} is a marine cleaning and maintenance company serving waterfront property owners in Pinellas, Hillsborough and Manatee counties, Florida. Services include dock cleaning, seawall cleaning, dock piling cleaning and barnacle removal, boat lift cleaning, dock ladder degrowth, piling and dock protection wraps, storm prep and seasonal cleaning, and recurring maintenance plans. Customers can get a free video inspection by calling or texting {PHONE_DISPLAY}.</p>
</section>

<section class="wrap"><h2 class="sec">Our Services</h2><div class="cards">{svc_cards}</div></section>

<section class="band"><div class="wrap steps">
<h2 class="sec">How It Works</h2>
<ol><li><b>Send a video.</b> Text a short video or photos of your dock, seawall or lift to {PHONE_DISPLAY}.</li>
<li><b>Get a price.</b> We review it and send a clear recommendation and quote, usually the same day.</li>
<li><b>We clean and restore.</b> Our crew removes growth and documents the work with before and after photos.</li>
<li><b>We protect it.</b> Add piling wraps or a maintenance plan to keep growth from coming back.</li></ol>
</div></section>

<section class="wrap"><h2 class="sec">Service Areas</h2><div class="areas">{county_cards}</div></section>

<div class="wrap">{faq_html(FAQ_HOME)}</div>
"""
pages["index.html"] = page("index.html",
    f"Dock and Seawall Cleaning Tampa Bay | {BIZ} | Pinellas, Hillsborough, Manatee",
    f"{BIZ} cleans docks, seawalls, pilings, ladders and boat lifts in Pinellas, Hillsborough and Manatee counties. Barnacle, oyster and algae removal. Free video inspections. Call or text {PHONE_DISPLAY}.",
    home_body, [business_schema(), faq_schema(FAQ_HOME),
                {"@context": "https://schema.org", "@type": "WebSite", "@id": SITE_URL + "/#website", "url": SITE_URL + "/", "name": BIZ, "publisher": org_ref()}])

# Service pages
for s in SERVICES:
    others = "".join(f'<li><a href="{o["slug"]}.html">{o["name"]}</a></li>' for o in SERVICES if o is not s)
    areas = "".join(f'<li><a href="{c["slug"]}.html">{s["name"]} in {c["name"]}</a><br><small>{", ".join(c["cities"][:5])}</small></li>' for c in COUNTIES.values())
    body = f"""
<div class="wrap crumbs"><a href="index.html">Home</a> / <span>{s['name']}</span></div>
<section class="wrap svc">
<div class="svc-main">
<h1>{s['h1']}</h1>
<p class="lead">{s['lead']}</p>
<img class="svc-img" src="assets/{s['img']}" alt="{s['name']} by {BIZ} in Tampa Bay, Florida" width="600" height="360">
<h2>What is included</h2><ul class="checks col">{''.join('<li>'+i+'</li>' for i in s['includes'])}</ul>
<h2>Why it matters</h2><p>{s['why']}</p>
<h2>Where we provide {s['name'].lower()}</h2><ul class="arealist">{areas}</ul>
{faq_html(s['faqs'])}
</div>
<aside class="side"><div class="box"><h3>Get a Free Video Inspection</h3><p>Text a video or photos and get a price fast.</p><a class="btn red block" href="sms:{PHONE_E164}">Text {PHONE_DISPLAY}</a><a class="btn outline block" href="tel:{PHONE_E164}">Call {PHONE_DISPLAY}</a></div>
<div class="box"><h3>Other Services</h3><ul>{others}</ul></div></aside>
</section>"""
    service_ld = {"@context": "https://schema.org", "@type": "Service", "name": s["name"], "serviceType": s["name"],
                  "description": s["lead"], "provider": org_ref(), "url": url(s["slug"] + ".html"),
                  "areaServed": [{"@type": "AdministrativeArea", "name": c["name"] + ", FL"} for c in COUNTIES.values()],
                  "offers": {"@type": "Offer", "description": "Free video inspection and quote", "price": "0", "priceCurrency": "USD"}}
    pages[s["slug"] + ".html"] = page(s["slug"] + ".html", s["title"], s["desc"], body,
        [business_schema(), service_ld, faq_schema(s["faqs"]), crumbs([("Home", "index.html"), (s["name"], s["slug"] + ".html")])],
        og_img="assets/" + s["img"])

# County pages
for key, c in COUNTIES.items():
    city_list = "".join(f"<li>{x}</li>" for x in c["cities"])
    svcs = "".join(f'<li><a href="{s["slug"]}.html">{s["name"]}</a></li>' for s in SERVICES)
    faqs = [
        (f"Do you offer dock and seawall cleaning in {c['name']}?", f"Yes. {BIZ} cleans docks, seawalls, pilings, ladders and boat lifts throughout {c['name']}, including {', '.join(c['cities'][:4])}."),
        (f"How do I get a quote in {c['name']}?", f"Text a short video or photos of your waterfront to {PHONE_DISPLAY}. We send back a recommendation and price, usually the same day."),
        (f"Which cities in {c['name']} do you serve?", f"We serve {', '.join(c['cities'])} and surrounding waterfront neighborhoods."),
    ]
    body = f"""
<div class="wrap crumbs"><a href="index.html">Home</a> / <a href="service-areas.html">Service Areas</a> / <span>{c['name']}</span></div>
<section class="wrap svc"><div class="svc-main">
<h1>Dock, Seawall and Piling Cleaning in {c['name']}, FL</h1>
<p class="lead">{c['intro']}</p>
<p>{c['local']}</p>
<h2>Services in {c['name']}</h2><ul class="checks col">{svcs}</ul>
<h2>Cities and communities we serve in {c['name']}</h2><ul class="cities">{city_list}</ul>
{faq_html(faqs)}
</div>
<aside class="side"><div class="box"><h3>Free Video Inspection</h3><p>Serving all of {c['name']}.</p><a class="btn red block" href="sms:{PHONE_E164}">Text {PHONE_DISPLAY}</a><a class="btn outline block" href="tel:{PHONE_E164}">Call {PHONE_DISPLAY}</a></div></aside>
</section>"""
    area_ld = {"@context": "https://schema.org", "@type": "Service", "name": f"Marine cleaning in {c['name']}",
               "serviceType": "Dock, seawall, piling and boat lift cleaning", "provider": org_ref(),
               "areaServed": [{"@type": "AdministrativeArea", "name": c["name"] + ", FL"}] + [{"@type": "City", "name": x + ", FL"} for x in c["cities"]]}
    pages[c["slug"] + ".html"] = page(c["slug"] + ".html",
        f"Dock and Seawall Cleaning {c['name']} FL | {BIZ}",
        f"Dock, seawall, piling and boat lift cleaning in {c['name']}, FL: {', '.join(c['cities'][:4])} and more. Barnacle and oyster removal. Free video inspection, call or text {PHONE_DISPLAY}.",
        body, [business_schema(), area_ld, faq_schema(faqs),
               crumbs([("Home", "index.html"), ("Service Areas", "service-areas.html"), (c["name"], c["slug"] + ".html")])])

# Service areas hub
hub = "".join(f"""<div class="area big"><h2><a href="{c['slug']}.html">{c['name']}</a></h2><ul class="cities">{''.join('<li>'+x+'</li>' for x in c['cities'])}</ul></div>""" for c in COUNTIES.values())
pages["service-areas.html"] = page("service-areas.html", f"Service Areas | Tampa Bay Marine Cleaning | {BIZ}",
    f"{BIZ} serves waterfront homes, HOAs and marinas across Pinellas, Hillsborough and Manatee counties. See every city we serve.",
    f"""<div class="wrap crumbs"><a href="index.html">Home</a> / <span>Service Areas</span></div>
<section class="wrap"><h1>Tampa Bay Service Areas</h1><p class="lead">{BIZ} provides dock, seawall, piling, ladder and boat lift cleaning for waterfront properties across three counties.</p><div class="areas">{hub}</div></section>""",
    [business_schema(), crumbs([("Home", "index.html"), ("Service Areas", "service-areas.html")])])

# Free inspection / contact
insp_faq = [FAQ_HOME[2], FAQ_HOME[3]]
pages["free-video-inspection.html"] = page("free-video-inspection.html", f"Free Video Inspection | Dock and Seawall Quotes | {BIZ}",
    f"Get a free video inspection and quote for dock, seawall, piling or boat lift cleaning in Tampa Bay. Text a video to {PHONE_DISPLAY}.",
    f"""<div class="wrap crumbs"><a href="index.html">Home</a> / <span>Free Video Inspection</span></div>
<section class="wrap svc"><div class="svc-main">
<h1>Free Video Inspection and Quote</h1>
<p class="lead">No waiting around for a site visit. Text us a short video and we will tell you exactly what your dock, seawall, pilings or lift need and what it will cost.</p>
<h2>What to send</h2><ul class="checks col"><li>A 30 to 60 second video walking the dock or seawall</li><li>Close ups of pilings, ladders and lift cradles</li><li>Your address or nearest city</li><li>Your name and the best time to reach you</li></ul>
<div class="hero-btns"><a class="btn red" href="sms:{PHONE_E164}">Text {PHONE_DISPLAY}</a><a class="btn outline" href="tel:{PHONE_E164}">Call {PHONE_DISPLAY}</a></div>
{faq_html(insp_faq)}
</div></section>""",
    [business_schema(), faq_schema(insp_faq), crumbs([("Home", "index.html"), ("Free Video Inspection", "free-video-inspection.html")])])

# ------------------------------------------------------------------ blog
from blog_posts import POSTS
SVC_BY_SLUG = {s["slug"]: s for s in SERVICES}

def md(body):
    out, ul = [], False
    for line in body.strip().split("\n"):
        line = line.strip()
        if not line:
            continue
        if line.startswith("- "):
            if not ul:
                out.append("<ul>"); ul = True
            out.append("<li>" + line[2:] + "</li>")
            continue
        if ul:
            out.append("</ul>"); ul = False
        if line.startswith("## "):
            out.append("<h2>" + line[3:] + "</h2>")
        else:
            out.append("<p>" + line + "</p>")
    if ul:
        out.append("</ul>")
    return "\n".join(out)

for i, p in enumerate(POSTS):
    fn = "blog-" + p["slug"] + ".html"
    related_svc = "".join(f'<li><a href="{SVC_BY_SLUG[l]["slug"]}.html">{SVC_BY_SLUG[l]["name"]}</a></li>' for l in p["links"])
    nxt = [POSTS[(i + k) % len(POSTS)] for k in (1, 2, 3)]
    more = "".join(f'<li><a href="blog-{q["slug"]}.html">{q["title"]}</a></li>' for q in nxt)
    words = len(p["body"].split())
    body = f"""
<div class="wrap crumbs"><a href="index.html">Home</a> / <a href="blog.html">Blog</a> / <span>{p['title']}</span></div>
<section class="wrap svc"><article class="svc-main post">
<h1>{p['title']}</h1>
<p class="meta">By {BIZ} &middot; Serving Pinellas, Hillsborough and Manatee Counties &middot; {max(2, words // 200)} min read</p>
<img class="svc-img" src="assets/{p['img']}" alt="{p['title']}" width="600" height="360">
{md(p['body'])}
<div class="inline-cta"><b>Free video inspection:</b> text a short video of your dock, seawall or lift to <a href="sms:{PHONE_E164}">{PHONE_DISPLAY}</a> for a same day recommendation and price.</div>
{faq_html(p['faqs'])}
</article>
<aside class="side"><div class="box"><h3>Get a Free Video Inspection</h3><a class="btn red block" href="sms:{PHONE_E164}">Text {PHONE_DISPLAY}</a><a class="btn outline block" href="tel:{PHONE_E164}">Call {PHONE_DISPLAY}</a></div>
<div class="box"><h3>Related Services</h3><ul>{related_svc}</ul></div>
<div class="box"><h3>More Articles</h3><ul>{more}</ul></div></aside>
</section>"""
    art = {"@context": "https://schema.org", "@type": "BlogPosting", "headline": p["title"], "description": p["desc"],
           "image": SITE_URL + "/assets/" + p["img"], "datePublished": TODAY, "dateModified": TODAY,
           "author": org_ref(), "publisher": org_ref(), "mainEntityOfPage": url(fn), "wordCount": words,
           "about": ["waterfront home maintenance", "Tampa Bay"],
           "spatialCoverage": [{"@type": "AdministrativeArea", "name": c["name"] + ", FL"} for c in COUNTIES.values()]}
    pages[fn] = page(fn, p["title"] + " | " + BIZ, p["desc"], body,
        [business_schema(), art, faq_schema(p["faqs"]), crumbs([("Home", "index.html"), ("Blog", "blog.html"), (p["title"], fn)])],
        og_img="assets/" + p["img"])

blog_cards = "".join(f"""<a class="card" href="blog-{p['slug']}.html"><img src="assets/{p['img']}" alt="{p['title']}" loading="lazy" width="560" height="360"><div><h3>{p['title']}</h3><p>{p['desc']}</p><span class="more">Read article</span></div></a>""" for p in POSTS)
pages["blog.html"] = page("blog.html", f"Waterfront Home Maintenance Blog | Tampa Bay | {BIZ}",
    "Tips for Tampa Bay waterfront homeowners on dock cleaning, seawall care, piling wraps, boat lifts and hurricane prep in Pinellas, Hillsborough and Manatee counties.",
    f"""<div class="wrap crumbs"><a href="index.html">Home</a> / <span>Blog</span></div>
<section class="wrap"><h1>Waterfront Home Maintenance Blog</h1><p class="lead">Straight answers for Tampa Bay waterfront homeowners on keeping docks, seawalls, pilings and lifts clean, safe and built to last.</p><div class="cards">{blog_cards}</div></section>""",
    [business_schema(), {"@context": "https://schema.org", "@type": "Blog", "name": f"{BIZ} Blog", "url": url("blog.html"), "publisher": org_ref(),
      "blogPost": [{"@type": "BlogPosting", "headline": p["title"], "url": url("blog-" + p["slug"] + ".html")} for p in POSTS]},
     crumbs([("Home", "index.html"), ("Blog", "blog.html")])])

# ------------------------------------------------------------------ write
if os.path.exists(OUT):
    shutil.rmtree(OUT)
os.makedirs(OUT + "/assets")
for f in os.listdir("assets"):
    shutil.copy("assets/" + f, OUT + "/assets/" + f)
for fn, html in pages.items():
    open(f"{OUT}/{fn}", "w").write(html)

prio = {"index.html": "1.0", "free-video-inspection.html": "0.9"}
sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
for fn in pages:
    sm += f"  <url><loc>{url(fn)}</loc><lastmod>{TODAY}</lastmod><priority>{prio.get(fn, '0.8')}</priority></url>\n"
open(f"{OUT}/sitemap.xml", "w").write(sm + "</urlset>\n")

open(f"{OUT}/robots.txt", "w").write(f"""User-agent: *
Allow: /

# AI search and answer engines are welcome
User-agent: GPTBot
Allow: /
User-agent: OAI-SearchBot
Allow: /
User-agent: ChatGPT-User
Allow: /
User-agent: ClaudeBot
Allow: /
User-agent: Claude-SearchBot
Allow: /
User-agent: PerplexityBot
Allow: /
User-agent: Google-Extended
Allow: /
User-agent: Applebot
Allow: /
User-agent: Applebot-Extended
Allow: /
User-agent: Bingbot
Allow: /

Sitemap: {SITE_URL}/sitemap.xml
""")

llms = f"""# {BIZ}

> {BIZ} is a marine cleaning and maintenance company serving waterfront property owners in Pinellas, Hillsborough and Manatee counties, Florida (Tampa Bay). Call or text {PHONE_DISPLAY} for a free video inspection.

## Key facts
- Business name: {BIZ}
- Phone (call or text): {PHONE_DISPLAY}
- Service area: Pinellas County, Hillsborough County and Manatee County, Florida
- Cities: {', '.join(sum([c['cities'] for c in COUNTIES.values()], []))}
- Removes: algae, barnacles, oysters, mold and marine growth
- Free video inspections: text a video or photos for a same day quote
- Hours: {'; '.join(h[3] for h in HOURS)}

## Services
""" + "\n".join(f"- [{s['name']}]({url(s['slug'] + '.html')}): {s['desc']}" for s in SERVICES) + """

## Service areas
""" + "\n".join(f"- [{c['name']}]({url(c['slug'] + '.html')})" for c in COUNTIES.values()) + f"""

## Contact
- [Free Video Inspection]({url('free-video-inspection.html')})

## Guides for waterfront homeowners
""" + "\n".join(f"- [{p['title']}]({url('blog-' + p['slug'] + '.html')}): {p['desc']}" for p in POSTS) + "\n"
open(f"{OUT}/llms.txt", "w").write(llms)
print("Built", len(pages), "pages")
