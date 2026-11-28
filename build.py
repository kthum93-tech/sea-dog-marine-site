#!/usr/bin/env python3
"""Sea Dog Marine static site generator.
Edit the CONFIG block, then run:  python3 build.py
Outputs plain .html pages, sitemap.xml, robots.txt and llms.txt into ./site
"""
import html, json, os, shutil, datetime

# ================= CONFIG (update before going live) =================
SITE_URL = "https://www.seadogmarinefl.com"   # TODO: real domain, no trailing slash
BIZ = "Sea Dog Marine"
TAGLINE = "Dock, Hull and Marine Repair"
PHONE_DISPLAY = "727-699-4920"
PHONE_E164 = "+17276994920"
EMAIL = ""            # TODO: public business email. Leave blank. Do not publish the form inbox here.
BASE_CITY = "Indian Rocks Beach"
POSTAL_CODE = "33785"
# TODO: street address omitted. Service-area business. Do not add address.streetAddress.
GEO = None            # TODO: dict with real "latitude" and "longitude" floats from a map pin. Leave None. Do not guess.
HAS_MAP = ""          # TODO: Google Business Profile map URL. Leave blank. Do not invent a URL.
HOURS = [  # Confirmed by Shea. Monday to Friday 7:00 to 18:00, Saturday 8:00 to 14:00.
    ("Mo,Tu,We,Th,Fr", "07:00", "18:00", "Monday to Friday: 7:00 AM to 6:00 PM"),
    ("Sa", "08:00", "14:00", "Saturday: 8:00 AM to 2:00 PM"),
]
SAME_AS = [  # TODO: paste Google Business Profile, Facebook, Instagram URLs. Leave empty. Do not invent URLs.
]
WEB3FORMS_KEY = ""  # TODO: Web3Forms access key. Leave blank. Do not invent a key.
FORM_ENDPOINT = "https://formsubmit.co/ajax/swgan7o7@gmail.com"
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
        "title": "Dock Cleaning in Tampa Bay, Florida | Sea Dog Marine",
        "desc": "Dock cleaning in Pinellas, Hillsborough and Manatee counties. Barnacle and oyster removal from decking and framing. Text for a free video inspection.",
        "card": "We remove algae, mold, barnacles and marine growth from decking and framing",
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
        "title": "Seawall Cleaning in Tampa Bay, Florida | Sea Dog Marine",
        "desc": "Seawall cleaning in Tampa Bay, Florida. Barnacle and oyster removal from the wall face and cap so cracks show. Text for a free video inspection.",
        "card": "We remove barnacles, oysters and algae from seawall faces and caps so you can see cracks before they spread.",
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
        "title": "Piling Cleaning in Tampa Bay, Florida | Sea Dog Marine",
        "desc": "Piling cleaning in Pinellas, Hillsborough and Manatee counties. Barnacle and oyster removal from wood and concrete pilings. Text for a free inspection.",
        "card": "Sea Dog Marine removes oysters, barnacles and algae from wood and concrete pilings",
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
        "title": "Boat Lift Cleaning in Tampa Bay, FL | Sea Dog Marine",
        "desc": "Boat lift cleaning in Tampa Bay, FL. Barnacle and oyster removal from cradles, bunks and beams so the lift runs smoothly. Text for a free video inspection.",
        "card": "We remove barnacles and growth from cradles, bunks, beams and cables so your lift runs smoothly.",
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
        "title": "Dock Ladder Cleaning in Tampa Bay, FL | Sea Dog Marine",
        "desc": "Dock ladder cleaning in Pinellas, Hillsborough and Manatee. Barnacle, oyster and slime removal so ladders are safe. Text for a free video inspection.",
        "card": "We remove barnacles, oysters and slime from swim and dock ladders so they are safe to use again.",
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
        "title": "Piling Wraps in Tampa Bay, Florida | Sea Dog Marine",
        "desc": "Piling wraps in Tampa Bay, FL. Clean wood pilings first, then protect them from marine borers and rot. Text 727-699-4920 for a free video inspection.",
        "card": "Protect wood pilings from marine borers, rot and growth",
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
        "title": "Maintenance Plans in Tampa Bay, FL | Sea Dog Marine",
        "desc": "Waterfront maintenance plans in Pinellas, Hillsborough and Manatee counties. Scheduled cleaning plus storm prep. Text for a free video inspection today.",
        "card": "Scheduled dock, seawall, piling and lift cleaning with storm prep and a photo report after every visit.",
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

# Dive services: in-water work done by a diver at the customer's dock or slip.
# TODO for Shea: confirm dive certifications, pricing, anode brands stocked, and recommended
# service intervals before publishing any of them. Do not invent certifications, prices, or schedules.
# TODO: replace the reused images (lift.jpg, after.jpg, ladder.jpg) with real underwater job photos.
DIVE_SERVICES = [
    {
        "slug": "hull-cleaning", "name": "Hull and Boat Bottom Cleaning", "img": "lift.jpg", "dive": True,
        "title": "Hull and Boat Bottom Cleaning Tampa Bay | Sea Dog Marine",
        "desc": "In-water hull and boat bottom cleaning in Pinellas, Hillsborough and Manatee. A diver removes barnacles and slime at your dock. Text 727-699-4920.",
        "card": "A diver cleans barnacles, slime and growth off your hull and running gear at your dock or slip.",
        "h1": "Hull and Boat Bottom Cleaning in Tampa Bay",
        "lead": "Barnacles, grass and slime on a boat bottom slow you down, burn more fuel and make the engine work harder. Sea Dog Marine sends a diver to your dock or slip to clean the hull in the water, so your boat stays put and you do not pay for a haul out just to clean the bottom.",
        "what": "Hull and boat bottom cleaning is in-water work. A diver removes barnacles, slime and grass from the bottom while the boat stays at your dock, lift or slip. It is routine underwater care. It is not a haul out, and it is not a bottom paint job.",
        "saltwater": "Tampa Bay stays warm most of the year, and the salt water in Pinellas, Hillsborough and Manatee counties grows barnacles and algae on a hull that sits still. Boats kept in canals and harbors often grow faster than boats that run often. Wiping growth off on a regular visit keeps hard shell from building into a layer that has to wait for a haul out. A cleaner bottom means less drag, so the boat moves more easily and the engine works less hard.",
        "process": [
            "Text 727-699-4920 with the boat length, a photo of the boat, and the dock, lift or slip where it sits.",
            "We confirm the bottom can be cleaned in the water and send a price. The price depends on length and how much growth is on it.",
            "A diver cleans the bottom, running gear, strainers and trim tabs at the boat.",
            "Zinc anodes are checked on the same dive. Worn zincs can be replaced on that visit if you want that done.",
            "You get notes on anything that looks damaged. Photos or video are available if you ask for them.",
        ],
        "includes": ["Hull bottom cleaning in the water", "Barnacle, slime and grass removal", "Running gear, strainers and trim tabs", "Check of zinc anodes while we are down there", "Notes on anything that looks damaged", "Photos or video on request"],
        "why": "A clean bottom means better speed, better fuel economy and less strain on the engine. Regular cleaning also keeps hard growth from building up to the point where it takes a haul out to remove.",
        "faqs": [
            ("Do I need to haul my boat out for bottom cleaning?", "No. A diver cleans the hull in the water at your dock, lift or slip, so there is no haul out needed just to clean the bottom."),
            ("How often should a boat bottom be cleaned in Tampa Bay?", "It depends on your bottom paint, how often you run the boat and how fast growth comes back where it is kept. Text a photo or video and we will recommend a schedule for your boat."),
            ("Can you check my zincs at the same time?", "Yes. We look at your zinc anodes during every hull cleaning and let you know when they need replacing. Zinc anode replacement can be added on the same dive."),
            ("Will hull cleaning strip my bottom paint?", "The job is to remove growth, not to sand the paint off. Soft growth comes off with less work than hard barnacles. If the paint is already failing, we will tell you what we see. We do not repaint bottoms in the water."),
        ],
    },
    {
        "slug": "zinc-anode-replacement", "name": "Zinc Anode Replacement", "img": "after.jpg", "dive": True,
        "title": "Zinc Anode Replacement in Tampa Bay | Sea Dog Marine",
        "desc": "Underwater zinc anode replacement in Pinellas, Hillsborough and Manatee. A diver swaps worn zincs on shafts, props and trim tabs. Text 727-699-4920.",
        "card": "A diver replaces worn zinc anodes on shafts, props and trim tabs without a haul out.",
        "h1": "Zinc Anode Replacement in Tampa Bay",
        "lead": "Zinc anodes are sacrificial metal that corrodes so your props, shafts, outdrives and trim tabs do not. Once the zincs are worn away, salt water starts eating the parts that cost real money. Sea Dog Marine replaces worn zincs in the water at your dock or slip.",
        "what": "A zinc anode is a small block of sacrificial metal bolted to a shaft, propeller, trim tab or outdrive. It is meant to corrode first, so the more expensive underwater metal is less likely to be eaten by galvanic corrosion. Replacement means a diver takes off the worn anode and installs a new one against a clean contact, while the boat stays in the water.",
        "saltwater": "Salt water conducts the small electrical currents that drive galvanic corrosion. A boat that lives in Tampa Bay, whether it sits in a Pinellas harbor, a Hillsborough canal or a Manatee river slip, keeps metal in that water. The zinc gets smaller as it does its job. When it is mostly gone, shafts, props, trim tabs and outdrives are the parts that can start to pit. Changing the zinc at the dock is a small job compared with waiting on a haul out.",
        "process": [
            "Text 727-699-4920 with the boat type and where it is kept. A photo of the transom or drive helps.",
            "A diver inspects the underwater zincs on the shaft, propeller, trim tabs and outdrive where they can be reached.",
            "Worn anodes are replaced. The contact surface is cleaned before the new zinc goes on, so it can actually protect the metal.",
            "You get a report of what was replaced. Anodes we cannot reach in the water are noted so you can plan a haul out for those.",
        ],
        "includes": ["Inspection of all underwater zincs", "Replacement of worn shaft, prop and trim tab zincs", "Outdrive and engine leg anodes where reachable", "Clean contact surfaces before installing new zincs", "Report of what was replaced"],
        "why": "Galvanic corrosion works quietly under the waterline. Fresh zincs are cheap compared with replacing a prop, shaft or outdrive that corroded because the anodes ran out.",
        "faqs": [
            ("What do zinc anodes do on a boat?", "Zinc anodes are sacrificial. They corrode first so the more valuable underwater metal, like props, shafts, trim tabs and outdrives, is protected from galvanic corrosion."),
            ("How do I know when my zincs need replacing?", "Zincs wear down over time in salt water. We inspect them in the water and replace them when they are worn. Text a photo of your boat and we will set up a check."),
            ("Can zincs be replaced without hauling the boat?", "Yes. Most shaft, prop and trim tab zincs can be replaced by a diver in the water at your dock or slip."),
            ("Can zinc replacement be done with a hull cleaning?", "Yes. We check zincs during hull and boat bottom cleaning and can replace the worn ones on the same dive."),
        ],
    },
    {
        "slug": "prop-cleaning", "name": "Propeller Cleaning", "img": "ladder.jpg", "dive": True,
        "title": "Propeller Cleaning in Tampa Bay, Florida | Sea Dog Marine",
        "desc": "Underwater propeller cleaning in Pinellas, Hillsborough and Manatee. A diver removes barnacles from props, shafts and struts. Text 727-699-4920.",
        "card": "A diver removes barnacles and growth from props, shafts and struts so the boat runs smooth.",
        "h1": "Propeller and Running Gear Cleaning in Tampa Bay",
        "lead": "Even a thin layer of barnacles on a propeller can cost you speed and add vibration. Sea Dog Marine cleans props, shafts, struts and rudders in the water so your boat runs the way it should.",
        "what": "Propeller cleaning is a diver removing barnacles and other hard growth from the blades. The same dive usually covers the shaft, strut and rudder. The boat stays in the water at your dock, lift or slip. This is cleaning, not propeller repair or balancing.",
        "saltwater": "A propeller is a small surface that the engine depends on. In Tampa Bay salt water, barnacles settle on blades that sit still, on canal lifts in Hillsborough as much as on bay docks in Pinellas and Manatee. Even a light crust changes how the prop bites the water. Owners usually notice it as lost speed or a vibration that was not there before. Cleaning the prop is separate from cleaning the whole hull, and most boats have both done on one dive.",
        "process": [
            "Text a photo of the boat and where it is kept to 727-699-4920, along with the boat length.",
            "The diver cleans the blades, then the shaft, strut and rudder.",
            "Hard growth comes off. The diver looks for obvious dings or a bent blade and tells you what is visible. Bent blades need a prop shop, which is a different job.",
            "Shaft and prop zincs are checked. Replacement is available on the same visit if they are worn.",
            "The propeller can be cleaned on the same dive as the hull if you want both done.",
        ],
        "includes": ["Propeller blade cleaning", "Shaft, strut and rudder cleaning", "Barnacle and hard growth removal", "Visual check for dings or damage", "Zinc check on the shaft and prop"],
        "why": "Props are precision parts. Growth on the blades hurts performance and fuel economy, and cleaning them is one of the fastest ways to get a sluggish boat running right again.",
        "faqs": [
            ("Why does my boat feel slow or vibrate?", "Barnacles and growth on the propeller and running gear are a common cause. Cleaning the prop often brings back lost speed and smooths out vibration."),
            ("Can prop cleaning be added to a hull cleaning?", "Yes. Most customers have the prop and running gear cleaned on the same dive as the hull and boat bottom cleaning."),
            ("Do you repair bent propellers?", "No. We clean growth off the prop and tell you if a blade looks dinged or bent. Straightening, welding and balancing are a prop shop job, not an in-water cleaning."),
        ],
    },
]
SERVICES.extend(DIVE_SERVICES)
DOCK_SERVICES = [s for s in SERVICES if not s.get("dive")]

FAQ_DIVE = [
    ("What dive services does Sea Dog Marine offer?", "Sea Dog Marine offers in-water hull and boat bottom cleaning, zinc anode replacement and propeller and running gear cleaning at your dock, lift or slip in Pinellas, Hillsborough and Manatee counties."),
    ("Do I have to bring my boat anywhere?", "No. A diver comes to your dock, lift or marina slip and does the work in the water."),
    ("How do I get a price for dive work?", "Text a photo or video of your boat, its length and where it is kept to 727-699-4920. We send back a recommendation and a price."),
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

def served_places(counties):
    areas = []
    for c in counties:
        areas.append({"@type": "AdministrativeArea", "name": c["name"] + ", FL"})
        for city in c["cities"]:
            areas.append({"@type": "City", "name": city + ", FL"})
    return areas

def city_by_name(name):
    for city in CITIES:
        if city["name"] == name:
            return city
    return None

def city_items(names):
    out = ""
    for name in names:
        city = city_by_name(name)
        if city:
            out += f'<li><a href="{city["slug"]}.html">{html.escape(name)}</a></li>'
        else:
            out += f"<li>{html.escape(name)}</li>"
    return out

def real_text(value):
    value = (value or "").strip()
    if not value or "TODO" in value.upper():
        return ""
    return value

def business_schema():
    areas = served_places(COUNTIES.values())
    d = {
        "@context": "https://schema.org",
        "@type": ["HomeAndConstructionBusiness", "LocalBusiness"],
        "@id": SITE_URL + "/#business",
        "name": BIZ,
        "alternateName": "Sea Dog Marine Cleaning",
        "slogan": "Remove Growth. Restore. Protect.",
        "description": "Sea Dog Marine, based in Indian Rocks Beach, provides professional dock cleaning, seawall cleaning, piling cleaning and barnacle removal, boat lift cleaning, ladder degrowth, piling wraps, waterfront maintenance plans and dive services (in-water hull cleaning, zinc anode replacement and propeller cleaning) in Pinellas, Hillsborough and Manatee counties, Florida.",
        "url": SITE_URL + "/",
        "telephone": PHONE_E164,
        "image": SITE_URL + "/assets/og-flyer.jpg",
        "logo": SITE_URL + "/assets/logo.jpg",
        "priceRange": "$$",
        "address": {"@type": "PostalAddress", "addressRegion": "FL", "addressCountry": "US"},
        "areaServed": areas,
        "knowsAbout": ["dock cleaning", "seawall cleaning", "barnacle removal", "oyster removal", "piling cleaning", "piling wraps", "boat lift cleaning", "marine growth removal", "storm preparation for docks", "hull cleaning", "boat bottom cleaning", "zinc anode replacement", "propeller cleaning"],
        "openingHoursSpecification": [{"@type": "OpeningHoursSpecification", "dayOfWeek": [ {"Mo":"Monday","Tu":"Tuesday","We":"Wednesday","Th":"Thursday","Fr":"Friday","Sa":"Saturday","Su":"Sunday"}[x] for x in h[0].split(",")], "opens": h[1], "closes": h[2]} for h in HOURS],
        "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Marine Cleaning and Maintenance Services",
            "itemListElement": [{"@type": "Offer", "itemOffered": {"@type": "Service", "name": s["name"], "url": url(s["slug"] + ".html")}} for s in SERVICES]
            + [{"@type": "Offer", "price": "0", "priceCurrency": "USD", "itemOffered": {"@type": "Service", "name": "Free Video Inspection"}}]},
        "contactPoint": {"@type": "ContactPoint", "telephone": PHONE_E164, "contactType": "customer service", "areaServed": "US-FL", "availableLanguage": "English"},
    }
    city = real_text(BASE_CITY)
    postal = real_text(POSTAL_CODE)
    email = real_text(EMAIL)
    has_map = real_text(HAS_MAP)
    if city:
        d["address"]["addressLocality"] = city
    if postal:
        d["address"]["postalCode"] = postal
    if email and "@" in email:
        d["email"] = email
    same_as = [u for u in SAME_AS if isinstance(u, str) and u.startswith("https://")]
    if same_as:
        d["sameAs"] = same_as
    if has_map.startswith("https://"):
        d["hasMap"] = has_map
    if isinstance(GEO, dict):
        lat, lng = GEO.get("latitude"), GEO.get("longitude")
        if isinstance(lat, (int, float)) and isinstance(lng, (int, float)) and not isinstance(lat, bool) and not isinstance(lng, bool):
            d["geo"] = {"@type": "GeoCoordinates", "latitude": lat, "longitude": lng}
    d["founder"] = {
        "@type": "Person",
        "name": "Shea Ganison",
        "jobTitle": "Owner, Sea Dog Marine",
        "worksFor": org_ref(),
    }
    return d

def local_todo_comment():
    missing = []
    if not real_text(BASE_CITY):
        missing.append("address.addressLocality (set BASE_CITY)")
    if not real_text(POSTAL_CODE):
        missing.append("address.postalCode (set POSTAL_CODE)")
    missing.append("address.streetAddress omitted (service-area business). Do not invent a street.")
    if not (isinstance(GEO, dict) and isinstance(GEO.get("latitude"), (int, float)) and not isinstance(GEO.get("latitude"), bool)):
        missing.append("geo GeoCoordinates (set GEO latitude and longitude from a real pin)")
    if not (real_text(EMAIL) and "@" in EMAIL):
        missing.append("email (set EMAIL). Do not publish the quote-form inbox as the public email.")
    if not any(isinstance(u, str) and u.startswith("https://") for u in SAME_AS):
        missing.append("sameAs URLs for Google Business Profile, Facebook and Instagram (set SAME_AS)")
    if not real_text(HAS_MAP).startswith("https://"):
        missing.append("hasMap Google Business Profile map URL (set HAS_MAP)")
    lines = "\n".join("- " + item for item in missing)
    return (
        "<!-- TODO for Kyle/Shea: LocalBusiness fields below are omitted so the JSON-LD stays valid. "
        "Fill the real values in the CONFIG block of build.py. Do not guess coordinates, URLs, a street, or a public email.\n"
        + lines
        + "\nDo not add aggregateRating or review without real review data. -->"
    )

def business_ld():
    return (local_todo_comment(), business_schema())

def faq_schema(faqs):
    return {"@context": "https://schema.org", "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]}

def crumbs(items):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList",
            "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": url(p)} for i, (n, p) in enumerate(items)]}

def ld(obj):
    return '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False) + "</script>"

def render_schemas(schemas):
    parts = []
    for item in schemas:
        if isinstance(item, tuple):
            comment, obj = item
            if comment:
                parts.append(comment)
            parts.append(ld(obj))
        else:
            parts.append(ld(item))
    return "".join(parts)

def faq_html(faqs):
    out = '<section class="faq"><h2>Frequently Asked Questions</h2>'
    for q, a in faqs:
        out += f"<details><summary>{q}</summary><p>{a}</p></details>"
    return out + "</section>"

NAV = [("Docks", "dock-cleaning.html"), ("Seawalls", "seawall-cleaning.html"), ("Pilings", "piling-cleaning.html"),
       ("Boat Lifts", "boat-lift-cleaning.html"), ("Dive Services", "dive-services.html"), ("Areas", "service-areas.html"), ("Blog", "blog.html"), ("Free Inspection", "free-video-inspection.html")]

def cta_block():
    return f"""<section class="cta"><div class="wrap cta-in">
<div><h2>Free Video Inspection</h2><p>Text a short video or a few photos of your dock, seawall, pilings or lift. We send back a recommendation and price, usually the same day.</p></div>
<div class="cta-btns"><a class="btn red" href="sms:{PHONE_E164}">Text {PHONE_DISPLAY}</a><a class="btn outline" href="tel:{PHONE_E164}">Call {PHONE_DISPLAY}</a></div>
</div></section>"""

def page(fname, title, desc, body, schemas, og_img="assets/og-flyer.jpg", og_type="website", extra_head="", robots="index, follow, max-image-preview:large"):
    canonical = url(fname)
    safe_title = html.escape(title, quote=True)
    safe_desc = html.escape(desc, quote=True)
    svc_links = "".join(f'<li><a href="{s["slug"]}.html">{s["name"]}</a></li>' for s in SERVICES)
    area_links = "".join(f'<li><a href="{c["slug"]}.html">{c["name"]}</a></li>' for c in COUNTIES.values())
    area_links += '<li><a href="service-areas.html">All cities we serve</a></li>'
    area_links += "".join(f'<li><a href="{c["slug"]}.html">{c["name"]}</a></li>' for c in CITIES)
    hours = "<br>".join(h[3] for h in HOURS)
    nav = "".join(f'<a href="{p}">{n}</a>' for n, p in NAV)
    return f"""<!DOCTYPE html>
<html lang="en-US">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{safe_title}</title>
<meta name="description" content="{safe_desc}">
<link rel="canonical" href="{canonical}">
<meta name="robots" content="{html.escape(robots, quote=True)}">
<meta name="geo.region" content="US-FL">
<meta name="geo.placename" content="Tampa Bay">
<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="{BIZ}">
<meta property="og:title" content="{safe_title}">
<meta property="og:description" content="{safe_desc}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{SITE_URL}/{og_img}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{safe_title}">
<meta name="twitter:description" content="{safe_desc}">
<meta name="theme-color" content="#0b2a4a">
<link rel="icon" href="assets/logo.jpg">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@700;800&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/style.css">
{extra_head}{render_schemas(schemas)}
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
<div><h3>{BIZ}</h3><p>Based in Indian Rocks Beach, serving Pinellas, Hillsborough and Manatee. Professional marine cleaning and maintenance for docks, seawalls, pilings, ladders and boat lifts.</p>
<p><b>Phone:</b> <a href="tel:{PHONE_E164}">{PHONE_DISPLAY}</a> (call or text){'<br><b>Email:</b> <a href="mailto:'+EMAIL+'">'+EMAIL+'</a>' if EMAIL else ''}</p><p><b>Hours:</b><br>{hours}</p></div>
<div><h3>Services</h3><ul>{svc_links}<li><a href="free-video-inspection.html">Free Video Inspection</a></li></ul></div>
<div><h3>Service Areas</h3><ul>{area_links}<li><a href="blog.html">Waterfront Maintenance Blog</a></li></ul></div>
</div><div class="wrap copy">&copy; {datetime.date.today().year} {BIZ}. All rights reserved. <a href="privacy-policy.html">Privacy Policy</a> &middot; <a href="sms-terms.html">SMS Terms</a></div></footer>
<a class="float" href="sms:{PHONE_E164}">Text for a Free Video Inspection</a>
</body></html>"""

# ------------------------------------------------------------------ pages
# City pages. Copy is local waterfront context only: no stats, reviews, marina deals, prices, or names.
# Titles are 50-60 characters. Descriptions are 140-155. Do not invent a street address.
CITIES = [
    {
        "name": "St. Petersburg", "slug": "st-petersburg-dock-seawall-cleaning", "county": "pinellas",
        "title": "Dock and Seawall Cleaning in St. Petersburg | Sea Dog Marine",
        "desc": "Dock, seawall and hull cleaning in St. Petersburg, FL. Barnacle and oyster removal on bay and canal docks. Text 727-699-4920 for a free video inspection.",
        "intro": "St. Petersburg waterfront sits on Tampa Bay, Boca Ciega Bay and a long run of saltwater canals. Warm bay water and tidal canals put barnacles, oysters and algae on docks, seawalls, pilings, ladders and boat lifts.",
        "detail": "Canal lots and open bay lots both stay in salt water year round. Growth along the waterline hides the condition of a seawall cap and adds weight to pilings. Sea Dog Marine cleans those surfaces from the dock and from the water. A diver can also clean a hull, replace zincs or clean a propeller while the boat stays at the property.",
        "nearby": ["St. Pete Beach", "Treasure Island", "Clearwater"],
        "faqs": [
            ("Do you clean canal seawalls in St. Petersburg?", "Yes. Canal docks and open bay docks in St. Petersburg get the same dock, seawall, piling, ladder and lift cleaning. Text a short video to 727-699-4920."),
            ("Can you clean a hull at a St. Petersburg dock?", "Yes. A diver cleans the boat bottom, checks zincs and can clean the propeller in the water at the dock, lift or slip."),
        ],
    },
    {
        "name": "Clearwater", "slug": "clearwater-dock-seawall-cleaning", "county": "pinellas",
        "title": "Dock and Seawall Cleaning in Clearwater, FL | Sea Dog Marine",
        "desc": "Dock, seawall and hull cleaning in Clearwater, FL. Barnacle removal on harbor and Intracoastal docks. Text 727-699-4920 for a free video inspection.",
        "intro": "Clearwater waterfront includes Clearwater Harbor, Island Estates and docks along the Intracoastal, with the Gulf just west of the beach. Harbor water and the Intracoastal both grow barnacles and slime on lifts, ladders and seawalls.",
        "detail": "Harbor docks often sit in calmer water than the Gulf side, so shells and algae collect in a band at the waterline. Cleaning the dock, seawall and pilings shows the real condition of the structure. Hull, zinc and propeller work is done in the water at the dock or slip, so the boat does not have to be trailered for a routine cleaning.",
        "nearby": ["Dunedin", "Largo", "Seminole"],
        "faqs": [
            ("Do you clean docks on Clearwater Harbor and the Intracoastal?", "Yes. We clean docks, seawalls, pilings, ladders and lifts on harbor and Intracoastal waterfront in Clearwater."),
            ("Do I need to trailer the boat for a bottom cleaning in Clearwater?", "No. The diver comes to the dock, lift or slip. Text the boat length and a photo to 727-699-4920."),
        ],
    },
    {
        "name": "Tampa", "slug": "tampa-dock-seawall-cleaning", "county": "hillsborough",
        "title": "Tampa Dock, Seawall and Hull Cleaning, FL | Sea Dog Marine",
        "desc": "Dock, seawall and hull cleaning in Tampa, FL. Barnacle and oyster removal on bay, canal and river docks. Text 727-699-4920 for a free video inspection.",
        "intro": "Tampa waterfront runs from the Hillsborough River out to Hillsborough Bay and Old Tampa Bay, including bayfront homes and canal lots. Salt water and brackish river water both leave algae, barnacles and oysters on docks, seawalls and lifts.",
        "detail": "River docks see more freshwater influence. Bay docks and canal docks sit in saltier water, where shell growth is usually heavier. Sea Dog Marine cleans the dock, seawall, pilings, ladder and boat lift, and can send a diver for the hull, zincs and propeller without a haul out.",
        "nearby": ["Apollo Beach", "St. Petersburg", "Bradenton"],
        "faqs": [
            ("Do you work on river docks and bay docks in Tampa?", "Yes. Hillsborough River docks and docks on Hillsborough Bay or Old Tampa Bay are both in the service area. Shell growth is often heavier on the saltier bay and canal lots."),
            ("How do I get a price in Tampa?", "Text a short video of the dock, seawall, lift or boat to 727-699-4920. We send a recommendation and a price, usually the same day."),
        ],
    },
    {
        "name": "Largo", "slug": "largo-dock-seawall-cleaning", "county": "pinellas",
        "title": "Dock and Seawall Cleaning in Largo, Florida | Sea Dog Marine",
        "desc": "Dock, seawall and hull cleaning in Largo, FL. Barnacle and oyster removal on canal and Intracoastal docks. Text 727-699-4920 for a free video inspection.",
        "intro": "Largo sits inland of the beach towns, and its saltwater docks are mostly on canals and the Intracoastal rather than the open Gulf. Still canal water lets barnacles and oysters settle on pilings, seawall caps and lift bunks.",
        "detail": "Canal seawalls collect a band of shell at the waterline, and ladders get slick. Cleaning from the dock and the water keeps the work off the yard. The same property can add a diver for hull, zinc and propeller cleaning if the boat stays at the dock.",
        "nearby": ["Seminole", "Clearwater", "Dunedin"],
        "faqs": [
            ("Does Largo have saltwater docks you can clean?", "Yes. We clean canal and Intracoastal docks and seawalls in Largo, where quiet salt water grows barnacles and oysters."),
            ("Can a diver clean the boat at a Largo dock?", "Yes, when the boat is in the water at the dock, lift or slip. Text 727-699-4920 with the boat length and a photo."),
        ],
    },
    {
        "name": "Seminole", "slug": "seminole-dock-seawall-cleaning", "county": "pinellas",
        "title": "Dock and Seawall Cleaning in Seminole, FL | Sea Dog Marine",
        "desc": "Dock, seawall and hull cleaning in Seminole, FL. Barnacle removal on Boca Ciega Bay and canal docks. Text 727-699-4920 for a free video inspection.",
        "intro": "Seminole has saltwater docks along Boca Ciega Bay and the canals that connect toward the Intracoastal, plus homes on Lake Seminole. Barnacles and oysters attach on the saltwater docks and seawalls. The lake is a separate freshwater shoreline.",
        "detail": "Bay and canal pilings grow the same shell band seen across Pinellas. Sea Dog Marine cleans docks, seawalls, pilings, ladders and lifts on that saltwater shoreline, and a diver handles hull, zinc and propeller work at the dock. If a video shows the lake instead of the bay, we will say so, because freshwater growth is a different job from barnacles and oysters.",
        "nearby": ["Largo", "St. Petersburg", "Madeira Beach"],
        "faqs": [
            ("Do you clean Boca Ciega Bay docks in Seminole?", "Yes. Saltwater docks and seawalls on the bay and the connecting canals are the marine cleaning work. Lake Seminole is freshwater, and the video shows us which shoreline you have."),
            ("What should I send for a Seminole quote?", "Text a short video or a few photos of the dock, seawall or boat to 727-699-4920."),
        ],
    },
    {
        "name": "Dunedin", "slug": "dunedin-dock-seawall-cleaning", "county": "pinellas",
        "title": "Dunedin Dock and Seawall Cleaning, FL | Sea Dog Marine",
        "desc": "Dock, seawall and hull cleaning in Dunedin, FL. Barnacle removal on St. Joseph Sound docks and seawalls. Text 727-699-4920 for a free video inspection.",
        "intro": "Dunedin waterfront faces St. Joseph Sound, with docks and seawalls along the Intracoastal and the shoreline near the causeway to Honeymoon Island. The sound is shallow salt water, and barnacles and algae grow readily on anything that stays wet.",
        "detail": "Sound-side docks and seawalls pick up growth through the tidal band. Lift bunks and ladders get the same coating. Cleaning on a schedule keeps the walking surfaces usable and lets you see the wood and concrete underneath. Hull cleaning, zinc replacement and propeller cleaning are done in the water at the dock.",
        "nearby": ["Clearwater", "Tarpon Springs", "Largo"],
        "faqs": [
            ("Do you clean docks on St. Joseph Sound?", "Yes. Dunedin docks and seawalls on the sound and the Intracoastal are part of the Pinellas service area."),
            ("Can zincs be replaced at a Dunedin dock?", "Yes. A diver can inspect and replace reachable underwater zincs without a haul out. Text 727-699-4920 to set it up."),
        ],
    },
    {
        "name": "Tarpon Springs", "slug": "tarpon-springs-dock-seawall-cleaning", "county": "pinellas",
        "title": "Dock and Seawall Cleaning in Tarpon Springs | Sea Dog Marine",
        "desc": "Dock, seawall and hull cleaning in Tarpon Springs, FL. Barnacle removal on Anclote River and bayou docks. Text 727-699-4920 for a free video inspection.",
        "intro": "Tarpon Springs waterfront includes the Anclote River, the bayous and docks that open toward the Gulf. River and bayou water is salt and brackish, and hard growth still settles on pilings, seawalls and lift hardware.",
        "detail": "Residential docks along the river and the bayous see the same saltwater growth as the rest of northern Pinellas. Boats kept there grow slime and barnacles on the hull and propeller as well as on the dock. Sea Dog Marine cleans the dock, seawall, pilings, ladder and lift, and a diver can clean the bottom, swap worn zincs and clean the prop at the slip.",
        "nearby": ["Dunedin", "Clearwater"],
        "faqs": [
            ("Do you clean Anclote River docks?", "Yes. River and bayou docks and seawalls in Tarpon Springs are served, along with the rest of northern Pinellas."),
            ("Will you clean a propeller in Tarpon Springs?", "Yes. Propeller and running gear cleaning is done in the water at the dock or slip. Call or text 727-699-4920."),
        ],
    },
    {
        "name": "Treasure Island", "slug": "treasure-island-dock-seawall-cleaning", "county": "pinellas",
        "title": "Treasure Island Dock and Seawall Cleaning | Sea Dog Marine",
        "desc": "Dock, seawall and hull cleaning in Treasure Island, FL. Barnacle removal on bay-side docks and seawalls. Text 727-699-4920 for a free video inspection.",
        "intro": "Treasure Island is a barrier island with the Gulf on the west and Boca Ciega Bay and the Intracoastal on the east. Most private docks and seawalls are on the bay side, where calmer salt water grows barnacles and oysters on pilings and caps.",
        "detail": "Bay-side lifts and ladders pick up shell because the water is warm and sheltered. John's Pass, the inlet at the south end, sits between Treasure Island and Madeira Beach. Cleaning usually covers the dock, seawall, pilings and ladder. A diver can clean the hull and propeller and check zincs while the boat is at the dock.",
        "nearby": ["St. Pete Beach", "Madeira Beach", "St. Petersburg"],
        "faqs": [
            ("Which side of Treasure Island do you clean?", "Private docks and seawalls are mostly on the bay and Intracoastal side, and that is the usual job. Text a video if the access looks different."),
            ("Do you clean ladders and lifts on Treasure Island?", "Yes. Ladder, lift, dock, seawall and piling cleaning are all available, plus in-water hull work. Text 727-699-4920."),
        ],
    },
    {
        "name": "St. Pete Beach", "slug": "st-pete-beach-dock-seawall-cleaning", "county": "pinellas",
        "title": "Dock and Seawall Cleaning in St. Pete Beach | Sea Dog Marine",
        "desc": "Dock, seawall and hull cleaning in St. Pete Beach, FL. Barnacle removal on Intracoastal docks and seawalls. Text 727-699-4920 for a free video inspection.",
        "intro": "St. Pete Beach is a barrier island between the Gulf and Boca Ciega Bay. Docks and seawalls line the bay and the Intracoastal, including narrower canals and the Pass-a-Grille shoreline at the south end.",
        "detail": "Beach-town docks here include year round homes and places that sit between visits, so growth can get ahead of the owner. Sea Dog Marine cleans docks, seawalls, pilings, ladders and lifts, and can put the property on a maintenance schedule. Hull, zinc and propeller work is done in the water, so the boat does not have to leave the dock for a routine bottom cleaning.",
        "nearby": ["Treasure Island", "St. Petersburg", "Madeira Beach"],
        "faqs": [
            ("Do you clean Intracoastal docks in St. Pete Beach?", "Yes, including bay-side docks and seawalls down toward Pass-a-Grille. Text a video of the dock or wall to 727-699-4920."),
            ("Can a seasonal home in St. Pete Beach be put on a schedule?", "Yes. Maintenance plans set the cleaning visits so the dock is not left to grow between stays. The plan is built around that property."),
        ],
    },
    {
        "name": "Madeira Beach", "slug": "madeira-beach-dock-seawall-cleaning", "county": "pinellas",
        "title": "Madeira Beach Dock and Seawall Cleaning, FL | Sea Dog Marine",
        "desc": "Dock, seawall and hull cleaning in Madeira Beach, FL. Barnacle removal on Intracoastal docks near John's Pass. Text 727-699-4920 for a free inspection.",
        "intro": "Madeira Beach sits on the Intracoastal, with John's Pass at the north end and Boca Ciega Bay behind the Gulf beach. Residential docks and seawalls on the bay side carry barnacles, oysters and algae through the tidal zone.",
        "detail": "Water near the pass moves, but pilings and seawall caps still hold a shell band. Ladders and lift bunks get slick and sharp. Sea Dog Marine cleans those surfaces and can send a diver for the hull, zinc anodes and propeller at the same dock.",
        "nearby": ["Treasure Island", "St. Pete Beach", "Seminole"],
        "faqs": [
            ("Do you clean docks near John's Pass?", "Yes. Madeira Beach docks and seawalls on the Intracoastal and Boca Ciega Bay are in the service area, including properties near the pass."),
            ("Can the hull and propeller be cleaned on the same visit in Madeira Beach?", "Yes. Most boats have the propeller cleaned on the same dive as the hull. Text 727-699-4920 with the boat length."),
        ],
    },
    {
        "name": "Apollo Beach", "slug": "apollo-beach-dock-seawall-cleaning", "county": "hillsborough",
        "title": "Apollo Beach Dock and Seawall Cleaning, FL | Sea Dog Marine",
        "desc": "Dock, seawall and hull cleaning in Apollo Beach, FL. Oyster and barnacle removal on canal seawalls. Text 727-699-4920 for a free video inspection.",
        "intro": "Apollo Beach is a canal community on Tampa Bay in southern Hillsborough County. The canals are salt water with limited flow, and oyster buildup on seawalls and lift cradles is a regular sight on this shoreline.",
        "detail": "Oysters on a seawall cap and barnacles on lift bunks are the usual find. Cleaning the wall, dock, pilings and ladder shows the concrete and hardware again. Boats kept on canal lifts grow a bottom and a dirty propeller in the same water, and a diver can handle that at the dock.",
        "nearby": ["Tampa", "Bradenton"],
        "faqs": [
            ("Do you remove oysters from Apollo Beach canal seawalls?", "Yes. Canal seawalls and lift cradles in Apollo Beach are a common oyster and barnacle cleaning job."),
            ("How do I start an Apollo Beach quote?", "Text a video of the seawall, dock or lift to 727-699-4920. Include the nearest cross street or community name if you have it."),
        ],
    },
    {
        "name": "Bradenton", "slug": "bradenton-dock-seawall-cleaning", "county": "manatee",
        "title": "Dock and Seawall Cleaning in Bradenton, FL | Sea Dog Marine",
        "desc": "Dock, seawall and hull cleaning in Bradenton, FL. Barnacle and oyster removal on the river and Palma Sola Bay. Text 727-699-4920 for a free inspection.",
        "intro": "Bradenton waterfront includes the Manatee River, the Braden River and Palma Sola Bay out toward the island. River docks and bay docks both sit in warm water that puts barnacles, oysters and algae on pilings and seawalls.",
        "detail": "River lots and bayfront lots do not grow at the same speed, but both need the waterline cleaned so the structure can be seen. Sea Dog Marine covers docks, seawalls, pilings, ladders and boat lifts in Bradenton, plus in-water hull, zinc and propeller work at the dock.",
        "nearby": ["Palmetto", "Anna Maria Island", "Apollo Beach"],
        "faqs": [
            ("Do you clean Manatee River docks and Palma Sola Bay docks?", "Yes. Both are in Bradenton, and both are in the Manatee County service area. Text 727-699-4920 with a short video."),
            ("Can you clean a boat bottom in Bradenton without a haul out?", "Yes. A diver works at the dock, lift or slip and can clean the hull, check zincs and clean the propeller."),
        ],
    },
    {
        "name": "Palmetto", "slug": "palmetto-dock-seawall-cleaning", "county": "manatee",
        "title": "Palmetto Dock and Seawall Cleaning, FL | Sea Dog Marine",
        "desc": "Dock, seawall and hull cleaning in Palmetto, FL. Barnacle removal on Manatee River docks and seawalls. Text 727-699-4920 for a free video inspection.",
        "intro": "Palmetto faces Bradenton across the Manatee River, with riverfront docks and seawalls and more shoreline toward Terra Ceia Bay to the north. Tidal river water carries barnacles and algae onto pilings, ladders and lift beams.",
        "detail": "A river seawall hides cracks under oysters the same way a bay wall does. Cleaning the face and cap, the dock and the pilings is how you see the real condition. Hull cleaning and zinc replacement are available in the water for boats kept at these docks.",
        "nearby": ["Bradenton", "Anna Maria Island"],
        "faqs": [
            ("Do you clean Palmetto docks on the Manatee River?", "Yes. River docks and seawalls in Palmetto are part of the Manatee County service area, including waterfront toward Terra Ceia Bay."),
            ("Can a diver replace zincs at a Palmetto dock?", "Yes. Reachable shaft, prop and trim tab zincs can be replaced in the water. Text 727-699-4920 with the boat type and where it is kept."),
        ],
    },
    {
        "name": "Anna Maria Island", "slug": "anna-maria-island-dock-seawall-cleaning", "county": "manatee",
        "title": "Anna Maria Island Dock and Seawall Cleaning | Sea Dog Marine",
        "desc": "Dock, seawall and hull cleaning on Anna Maria Island, FL. Barnacle removal on bay-side docks and seawalls. Text 727-699-4920 for a free video inspection.",
        "intro": "Anna Maria Island is the barrier island at the mouth of Tampa Bay, with Anna Maria, Holmes Beach and Bradenton Beach along it. The Gulf is on the west. Private docks and seawalls are mostly on the bay side, along Anna Maria Sound and the canals.",
        "detail": "Bay-side pilings and seawalls take barnacles and oysters. Homes that are empty between visits can go a long stretch with nobody looking at the ladder or the lift. Sea Dog Marine cleans the dock, seawall, pilings, ladder and lift, and a diver can clean the hull and propeller and replace zincs without taking the boat off the island.",
        "nearby": ["Bradenton", "Longboat Key", "Palmetto"],
        "faqs": [
            ("Do you clean bay-side docks on Anna Maria Island?", "Yes. Docks and seawalls on Anna Maria Sound and the island canals are served, in Anna Maria, Holmes Beach and Bradenton Beach."),
            ("Do I have to bring the boat to the mainland for a bottom cleaning?", "No. The diver comes to the dock, lift or slip on the island. Call or text 727-699-4920."),
        ],
    },
    {
        "name": "Longboat Key", "slug": "longboat-key-dock-seawall-cleaning", "county": "manatee",
        "title": "Longboat Key Dock and Seawall Cleaning, FL | Sea Dog Marine",
        "desc": "Dock, seawall and hull cleaning on Longboat Key in Manatee County, FL. Barnacle removal on bay docks and seawalls. Text 727-699-4920 for a free inspection.",
        "intro": "Longboat Key is a barrier island south of Anna Maria, and the town continues into Sarasota County. Sea Dog Marine serves the Manatee County waterfront on the key, where docks face Sarasota Bay and the passes rather than the Gulf.",
        "detail": "Those bay docks and seawalls grow barnacles and oysters in the tidal band, and lift bunks pick up shell that can scratch a hull. Cleaning covers the dock, seawall, pilings, ladder and boat lift. A diver cleans the hull and propeller and replaces zincs in the water at the dock. The Sarasota County end of the key is outside this service area.",
        "nearby": ["Anna Maria Island", "Bradenton"],
        "faqs": [
            ("Do you serve all of Longboat Key?", "Sea Dog Marine serves Longboat Key waterfront in Manatee County. The key continues into Sarasota County, which is outside this service area."),
            ("What shows up on Longboat Key bay docks?", "Barnacles, oysters and algae on docks, seawalls, pilings and lifts. A diver also cleans hulls and propellers in the water. Text 727-699-4920 for a look at your dock."),
        ],
    },
]



def configured_form():
    key = WEB3FORMS_KEY.strip() if isinstance(WEB3FORMS_KEY, str) else ""
    endpoint = FORM_ENDPOINT.strip() if isinstance(FORM_ENDPOINT, str) else ""
    if not key or "TODO" in key.upper():
        key = ""
    if not endpoint.startswith("https://") or "TODO" in endpoint.upper():
        endpoint = ""
    return key, endpoint

def quote_section():
    key, endpoint = configured_form()
    configured = bool(key or endpoint)
    options = "".join(
        f'<option value="{html.escape(s["name"], quote=True)}">{html.escape(s["name"])}</option>'
        for s in SERVICES
    )
    form_hidden = "" if configured else " hidden"
    fallback_hidden = " hidden" if configured else ""
    script = """
<script>
(function () {
  var form = document.getElementById("quote-form");
  var fallback = document.getElementById("quote-fallback");
  var status = document.getElementById("quote-status");
  var key = __KEY__;
  var endpoint = __ENDPOINT__;
  if (!form) return;
  if (!key && !endpoint) {
    form.hidden = true;
    if (fallback) fallback.hidden = false;
    return;
  }
  form.hidden = false;
  if (fallback) fallback.hidden = true;
  form.addEventListener("submit", function (event) {
    event.preventDefault();
    var data = {
      name: form.name.value.trim(),
      phone: form.phone.value.trim(),
      city: form.city.value.trim(),
      service: form.service.value,
      message: form.message.value.trim(),
      sms_consent: form.sms_consent.checked ? "yes" : "no"
    };
    var email = form.email.value.trim();
    if (email) data.email = email;
    var honey = form._honey ? form._honey.value : "";
    if (honey) {
      status.textContent = "Please call or text 727-699-4920";
      return;
    }
    var url = key ? "https://api.web3forms.com/submit" : endpoint;
    var body = key
      ? Object.assign({access_key: key, subject: "Sea Dog Marine quote request"}, data)
      : Object.assign({
          _subject: "New quote request - Sea Dog Marine",
          _template: "table",
          _captcha: "false",
          _honey: honey
        }, data);
    var button = form.querySelector("button[type='submit']");
    button.disabled = true;
    status.textContent = "Sending.";
    fetch(url, {
      method: "POST",
      headers: {"Content-Type": "application/json", "Accept": "application/json"},
      body: JSON.stringify(body)
    }).then(function (response) {
      return response.json().then(function (payload) {
        return {ok: response.ok, payload: payload};
      }).catch(function () {
        return {ok: response.ok, payload: {}};
      });
    }).then(function (result) {
      var flag = result.payload ? result.payload.success : false;
      var success = result.ok && (flag === true || flag === "true");
      if (success) {
        status.textContent = "Thank you. We received your quote request.";
        form.reset();
      } else {
        status.textContent = "Please call or text 727-699-4920";
      }
    }).catch(function () {
      status.textContent = "Please call or text 727-699-4920";
    }).then(function () {
      button.disabled = false;
    });
  });
})();
</script>
""".replace("__KEY__", json.dumps(key)).replace("__ENDPOINT__", json.dumps(endpoint))
    return f"""<section class="quote" id="quote">
<h2>Request a quote</h2>
<p id="quote-fallback"{fallback_hidden}>Please call or text <a href="tel:{PHONE_E164}">{PHONE_DISPLAY}</a>. <a href="privacy-policy.html">Privacy policy</a>. <a href="sms-terms.html">SMS terms</a>.</p>
<form id="quote-form"{form_hidden} action="#quote">
<input class="hp" name="_honey" type="text" value="" tabindex="-1" autocomplete="off" aria-hidden="true">
<label for="quote-name">Name</label>
<input id="quote-name" name="name" type="text" autocomplete="name" required>
<div class="row">
<div><label for="quote-phone">Phone</label>
<input id="quote-phone" name="phone" type="tel" autocomplete="tel" required></div>
<div><label for="quote-email">Email <span class="opt">(optional)</span></label>
<input id="quote-email" name="email" type="email" autocomplete="email"></div>
</div>
<div class="row">
<div><label for="quote-city">City</label>
<input id="quote-city" name="city" type="text" autocomplete="address-level2" required></div>
<div><label for="quote-service">Service</label>
<select id="quote-service" name="service" required>
<option value="">Select a service</option>
{options}
</select></div>
</div>
<label for="quote-message">Message</label>
<textarea id="quote-message" name="message" required></textarea>
<label class="agree"><input name="sms_consent" type="checkbox" value="yes"> <span>You may text me about this request. This is optional and is not required to get a quote. Message frequency varies. Message and data rates may apply. See the <a href="sms-terms.html">SMS terms</a>.</span></label>
<p>We use this to reply to you. Read the <a href="privacy-policy.html">privacy policy</a>.</p>
<button class="btn red" type="submit">Send request</button>
<p class="status" id="quote-status" role="status"></p>
</form>
<noscript><p>Please call or text <a href="tel:{PHONE_E164}">{PHONE_DISPLAY}</a></p></noscript>
{script}
</section>"""

pages = {}

# Home
svc_cards = "".join(f"""<a class="card" href="{s['slug']}.html"><img src="assets/{s['img']}" alt="{s['name']} by {BIZ} in Tampa Bay" loading="lazy" width="560" height="360"><div><h3>{s['name']}</h3><p>{s['card']}</p><span class="more">Learn more</span></div></a>""" for s in DOCK_SERVICES)
dive_cards = "".join(f"""<a class="card" href="{s['slug']}.html"><img src="assets/{s['img']}" alt="{s['name']} by {BIZ} in Tampa Bay" loading="lazy" width="560" height="360"><div><h3>{s['name']}</h3><p>{s['card']}</p><span class="more">Learn more</span></div></a>""" for s in DIVE_SERVICES)
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
<p>Based in Indian Rocks Beach, serving Pinellas, Hillsborough and Manatee. {BIZ} is a marine cleaning and maintenance company for waterfront property owners in those counties. Services include dock cleaning, seawall cleaning, dock piling cleaning and barnacle removal, boat lift cleaning, dock ladder degrowth, piling and dock protection wraps, storm prep and seasonal cleaning, recurring maintenance plans, and dive services including in-water hull and boat bottom cleaning, zinc anode replacement and propeller cleaning. Customers can get a free video inspection by calling or texting {PHONE_DISPLAY}.</p>
</section>

<section class="wrap"><h2 class="sec">Our Services</h2><div class="cards">{svc_cards}</div></section>

<section class="wrap"><h2 class="sec">Dive Services</h2><p class="lead" style="text-align:center">A diver comes to your dock, lift or slip and works on your boat in the water. <a href="dive-services.html">See all dive services</a>.</p><div class="cards">{dive_cards}</div></section>

<section class="band"><div class="wrap steps">
<h2 class="sec">How It Works</h2>
<ol><li><b>Send a video.</b> Text a short video or photos of your dock, seawall or lift to {PHONE_DISPLAY}.</li>
<li><b>Get a price.</b> We review it and send a clear recommendation and quote, usually the same day.</li>
<li><b>We clean and restore.</b> Our crew removes growth and documents the work with before and after photos.</li>
<li><b>We protect it.</b> Add piling wraps or a maintenance plan to keep growth from coming back.</li></ol>
</div></section>

<section class="wrap"><h2 class="sec">Service Areas</h2><div class="areas">{county_cards}</div></section>

<div class="wrap">{faq_html(FAQ_HOME)}
{quote_section()}
</div>
"""
pages["index.html"] = page("index.html",
    "Dock & Seawall Cleaning Tampa Bay | Sea Dog Marine",
    "Dock and seawall cleaning in Tampa Bay, Florida. Barnacle and oyster removal with a free video inspection. Text or call 727-699-4920 for a quote.",
    home_body, [business_ld(), faq_schema(FAQ_HOME),
                {"@context": "https://schema.org", "@type": "WebSite", "@id": SITE_URL + "/#website", "url": SITE_URL + "/", "name": BIZ, "publisher": org_ref()}])

# Service pages
for s in SERVICES:
    others = "".join(f'<li><a href="{o["slug"]}.html">{o["name"]}</a></li>' for o in SERVICES if o is not s)
    areas = "".join(f'<li><a href="{c["slug"]}.html">{s["name"]} in {c["name"]}</a><br><small>{", ".join(c["cities"][:5])}</small></li>' for c in COUNTIES.values())
    if s.get("dive"):
        process = "".join(f"<li>{step}</li>" for step in s["process"])
        related = "".join(f'<li><a href="{o["slug"]}.html">{o["name"]}</a></li>' for o in DIVE_SERVICES if o is not s)
        related += '<li><a href="dive-services.html">All dive services</a></li><li><a href="boat-lift-cleaning.html">Boat lift cleaning</a></li><li><a href="service-areas.html">Service areas</a></li><li><a href="free-video-inspection.html">Free video inspection</a></li>'
        city_links = "".join(f'<li><a href="{c["slug"]}.html">{s["name"]} in {c["name"]}</a></li>' for c in CITIES)
        crumb = f'<div class="wrap crumbs"><a href="index.html">Home</a> / <a href="dive-services.html">Dive Services</a> / <span>{s["name"]}</span></div>'
        crumb_ld = [("Home", "index.html"), ("Dive Services", "dive-services.html"), (s["name"], s["slug"] + ".html")]
        middle = f"""
<h2>What it is</h2><p>{s['what']}</p>
<h2>Why it matters in Tampa Bay saltwater</h2><p>{s['saltwater']}</p>
<h2>The process</h2><ol>{process}</ol>
<h2>What is included</h2><ul class="checks col">{''.join('<li>'+i+'</li>' for i in s['includes'])}</ul>
<p>{s['why']}</p>
<h2>Related services</h2><ul class="arealist">{related}</ul>
<h2>Where we provide {s['name'].lower()}</h2><ul class="arealist">{areas}</ul>
<h2>City pages</h2><ul class="arealist">{city_links}</ul>"""
    else:
        crumb = f'<div class="wrap crumbs"><a href="index.html">Home</a> / <span>{s["name"]}</span></div>'
        crumb_ld = [("Home", "index.html"), (s["name"], s["slug"] + ".html")]
        middle = f"""
<h2>What is included</h2><ul class="checks col">{''.join('<li>'+i+'</li>' for i in s['includes'])}</ul>
<h2>Why it matters</h2><p>{s['why']}</p>
<h2>Where we provide {s['name'].lower()}</h2><ul class="arealist">{areas}</ul>"""
    body = f"""
{crumb}
<section class="wrap svc">
<div class="svc-main">
<h1>{s['h1']}</h1>
<p class="lead">{s['lead']}</p>
<img class="svc-img" src="assets/{s['img']}" alt="{s['name']} by {BIZ} in Tampa Bay, Florida" width="600" height="360">
{middle}
{faq_html(s['faqs'])}
</div>
<aside class="side"><div class="box"><h3>Get a Free Video Inspection</h3><p>Text a video or photos and get a price fast.</p><a class="btn red block" href="sms:{PHONE_E164}">Text {PHONE_DISPLAY}</a><a class="btn outline block" href="tel:{PHONE_E164}">Call {PHONE_DISPLAY}</a></div>
<div class="box"><h3>Other Services</h3><ul>{others}</ul></div></aside>
</section>"""
    # TODO: add Service.offers only when real prices are provided. Do not invent prices.
    service_ld = {"@context": "https://schema.org", "@type": "Service", "name": s["name"], "serviceType": s["name"],
                  "description": s["desc"], "provider": org_ref(), "url": url(s["slug"] + ".html"),
                  "areaServed": served_places(COUNTIES.values())}
    pages[s["slug"] + ".html"] = page(s["slug"] + ".html", s["title"], s["desc"], body,
        [business_ld(), ("<!-- TODO: Service.offers omitted until real prices are provided. Do not invent prices. -->", service_ld), faq_schema(s["faqs"]), crumbs(crumb_ld)],
        og_img="assets/" + s["img"])

# County pages. Titles and descriptions are hand-counted to 50-60 and 140-155 characters.
COUNTY_META = {
    "pinellas": (
        "Pinellas Dock Cleaning in Tampa Bay | Sea Dog Marine",
        "Dock and seawall cleaning in Pinellas County, FL, from St. Petersburg to Clearwater. Barnacle and oyster removal. Text for a free video inspection.",
    ),
    "hillsborough": (
        "Hillsborough Dock Cleaning, Tampa Bay | Sea Dog Marine",
        "Dock and seawall cleaning in Hillsborough County, FL, including Tampa and Apollo Beach. Barnacle and oyster removal. Text for a free video inspection.",
    ),
    "manatee": (
        "Manatee Dock Cleaning in Tampa Bay | Sea Dog Marine",
        "Dock and seawall cleaning in Manatee County, FL, from Bradenton to Anna Maria. Barnacle and oyster removal. Text for a free video inspection today.",
    ),
}

for key, c in COUNTIES.items():
    city_list = city_items(c["cities"])
    svcs = "".join(f'<li><a href="{s["slug"]}.html">{s["name"]}</a></li>' for s in DOCK_SERVICES)
    dive_svcs = "".join(f'<li><a href="{s["slug"]}.html">{s["name"]}</a></li>' for s in DIVE_SERVICES)
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
<h2>Dive services in {c['name']}</h2><p>A diver comes to your dock, lift or slip anywhere in {c['name']}. <a href="dive-services.html">About our dive services</a>.</p><ul class="checks col">{dive_svcs}</ul>
<h2>Cities and communities we serve in {c['name']}</h2><ul class="cities">{city_list}</ul>
{faq_html(faqs)}
</div>
<aside class="side"><div class="box"><h3>Free Video Inspection</h3><p>Serving all of {c['name']}.</p><a class="btn red block" href="sms:{PHONE_E164}">Text {PHONE_DISPLAY}</a><a class="btn outline block" href="tel:{PHONE_E164}">Call {PHONE_DISPLAY}</a></div></aside>
</section>"""
    area_ld = {"@context": "https://schema.org", "@type": "Service", "name": f"Marine cleaning in {c['name']}",
               "serviceType": "Dock, seawall, piling and boat lift cleaning",
               "description": COUNTY_META[key][1], "provider": org_ref(), "url": url(c["slug"] + ".html"),
               "areaServed": served_places([c])}
    pages[c["slug"] + ".html"] = page(c["slug"] + ".html",
        COUNTY_META[key][0],
        COUNTY_META[key][1],
        body, [business_ld(), ("<!-- TODO: Service.offers omitted until real prices are provided. Do not invent prices. -->", area_ld), faq_schema(faqs),
               crumbs([("Home", "index.html"), ("Service Areas", "service-areas.html"), (c["name"], c["slug"] + ".html")])])

# Service areas hub. County blurbs reuse the copy already published on each county page.
hub = "".join(
    f"""<div class="area big"><h2><a href="{c['slug']}.html">{c['name']}</a></h2>
<p>{c['intro']}</p>
<p>{c['local']}</p>
<p><a href="{c['slug']}.html">Dock, seawall and piling cleaning in {c['name']}</a>. Cities and communities we serve there:</p>
<ul class="cities">{city_items(c['cities'])}</ul></div>"""
    for c in COUNTIES.values()
)
pages["service-areas.html"] = page("service-areas.html", "Tampa Bay Dock Cleaning Service Areas | Sea Dog Marine",
    "Dock and seawall cleaning service areas across Pinellas, Hillsborough and Manatee counties. Barnacle and oyster removal. Text for a free video inspection.",
    f"""<div class="wrap crumbs"><a href="index.html">Home</a> / <span>Service Areas</span></div>
<section class="wrap"><h1>Tampa Bay Service Areas</h1><p class="lead">{BIZ} provides dock, seawall, piling, ladder, boat lift and hull cleaning for waterfront properties across Pinellas, Hillsborough and Manatee counties. Pick a county below, or open a city page for dock, seawall and hull cleaning in that city. Call or text {PHONE_DISPLAY}.</p><div class="areas">{hub}</div></section>""",
    [business_ld(), crumbs([("Home", "index.html"), ("Service Areas", "service-areas.html")])])

# City pages. Each intro is written for that waterfront. H1s follow one pattern on purpose.
for city in CITIES:
    county = COUNTIES[city["county"]]
    svcs = "".join(f'<li><a href="{s["slug"]}.html">{s["name"]}</a></li>' for s in SERVICES)
    nearby = "".join(
        f'<li><a href="{city_by_name(name)["slug"]}.html">{html.escape(name)}</a></li>'
        for name in city["nearby"]
    )
    body = f"""
<div class="wrap crumbs"><a href="index.html">Home</a> / <a href="service-areas.html">Service Areas</a> / <a href="{county['slug']}.html">{county['name']}</a> / <span>{html.escape(city['name'])}</span></div>
<section class="wrap svc"><div class="svc-main">
<h1>Dock, Seawall and Hull Cleaning in {html.escape(city['name'])}, FL</h1>
<p class="lead">{city['intro']}</p>
<p>{city['detail']}</p>
<p>Call or text <a href="tel:{PHONE_E164}">{PHONE_DISPLAY}</a> and we will look at a short video of the dock, seawall or boat. You can also <a href="free-video-inspection.html">send a free video inspection</a>.</p>
<h2>Services in {html.escape(city['name'])}</h2>
<ul class="checks col">{svcs}</ul>
<h2>Nearby areas</h2>
<ul class="arealist">{nearby}<li><a href="{county['slug']}.html">Dock and seawall cleaning in {county['name']}</a></li><li><a href="service-areas.html">All service areas</a></li></ul>
{faq_html(city['faqs'])}
</div>
<aside class="side"><div class="box"><h3>Free Video Inspection</h3><p>Serving {html.escape(city['name'])}. Call or text {PHONE_DISPLAY}.</p><a class="btn red block" href="sms:{PHONE_E164}">Text {PHONE_DISPLAY}</a><a class="btn outline block" href="tel:{PHONE_E164}">Call {PHONE_DISPLAY}</a></div></aside>
</section>"""
    area_served = [
        {"@type": "City", "name": city["name"] + ", FL"},
        {"@type": "AdministrativeArea", "name": county["name"] + ", FL"},
    ]
    service_ld = {
        "@context": "https://schema.org", "@type": "Service",
        "name": f"Dock, seawall and hull cleaning in {city['name']}",
        "serviceType": "Dock, seawall, piling and hull cleaning",
        "description": city["desc"], "provider": org_ref(), "url": url(city["slug"] + ".html"),
        "areaServed": area_served,
    }
    pages[city["slug"] + ".html"] = page(
        city["slug"] + ".html", city["title"], city["desc"], body,
        [business_ld(), ("<!-- TODO: Service.offers omitted until real prices are provided. Do not invent prices. -->", service_ld),
         faq_schema(city["faqs"]),
         crumbs([("Home", "index.html"), ("Service Areas", "service-areas.html"), (county["name"], county["slug"] + ".html"), (city["name"], city["slug"] + ".html")])],
    )

# Free inspection / contact
insp_faq = [FAQ_HOME[2], FAQ_HOME[3]]
pages["free-video-inspection.html"] = page("free-video-inspection.html", "Free Video Inspection in Tampa Bay | Sea Dog Marine",
    "Free video inspection for dock and seawall cleaning in Tampa Bay. See barnacle and oyster removal needs and get a price. Text 727-699-4920 to start.",
    f"""<div class="wrap crumbs"><a href="index.html">Home</a> / <span>Free Video Inspection</span></div>
<section class="wrap svc"><div class="svc-main">
<h1>Free Video Inspection and Quote</h1>
<p class="lead">No waiting around for a site visit. Text us a short video and we will tell you exactly what your dock, seawall, pilings or lift need and what it will cost.</p>
<h2>What you get</h2>
<p>Text a short video or photos of your dock, seawall or lift to {PHONE_DISPLAY}. We review it and send back a recommendation and a price, often the same day, with no site visit needed to get started. The recommendation says what the dock, seawall, pilings or lift needs. Price depends on size, amount of growth and access.</p>
<h2>How it works</h2>
<ol>
<li><b>Send a video.</b> Text a short video or photos to {PHONE_DISPLAY}. A 30 to 60 second video walking the dock or seawall is enough, with close ups of pilings, ladders and lift cradles. Include your address or nearest city, your name and the best time to reach you.</li>
<li><b>Get a price.</b> We review it and send a clear recommendation and quote, usually the same day.</li>
<li><b>We clean and restore.</b> The crew removes algae, barnacles, oysters, mold and marine growth, then documents the work with before and after photos.</li>
<li><b>We protect it.</b> Add piling wraps or a maintenance plan to keep growth from coming back. Plans can include scheduled cleanings, storm prep and a photo report after every visit.</li>
</ol>
<h2>What to send</h2><ul class="checks col"><li>A 30 to 60 second video walking the dock or seawall</li><li>Close ups of pilings, ladders and lift cradles</li><li>Your address or nearest city</li><li>Your name and the best time to reach you</li></ul>
<div class="hero-btns"><a class="btn red" href="sms:{PHONE_E164}">Text {PHONE_DISPLAY}</a><a class="btn outline" href="tel:{PHONE_E164}">Call {PHONE_DISPLAY}</a></div>
{quote_section()}
{faq_html(insp_faq)}
</div></section>""",
    [business_ld(), faq_schema(insp_faq), crumbs([("Home", "index.html"), ("Free Video Inspection", "free-video-inspection.html")])])

# Dive services hub
dive_list = "".join(f'<li><a href="{s["slug"]}.html"><b>{s["name"]}</b></a>: {s["card"]}</li>' for s in DIVE_SERVICES)
pages["dive-services.html"] = page("dive-services.html", "Boat Dive Services in Tampa Bay, Florida | Sea Dog Marine",
    "Boat dive services in Pinellas, Hillsborough and Manatee: hull cleaning, zinc anode replacement and prop cleaning at your dock. Text 727-699-4920.",
    f"""<div class="wrap crumbs"><a href="index.html">Home</a> / <span>Dive Services</span></div>
<section class="wrap svc"><div class="svc-main">
<h1>Boat Dive Services in Tampa Bay</h1>
<p class="lead">{BIZ} does more than docks and seawalls. Our diver works on your boat in the water at your dock, lift or marina slip across Pinellas, Hillsborough and Manatee counties, so you can skip the haul out for routine underwater care.</p>
<h2>Our dive services</h2><ul class="arealist">{dive_list}</ul>
<h2>Why in-water service</h2><p>Growth on a hull and running gear costs speed and fuel, and worn zinc anodes leave props, shafts and outdrives open to corrosion. Handling this in the water at your dock keeps the boat ready to use and avoids the cost and downtime of hauling it out for routine work.</p>
<div class="cards">{dive_cards}</div>
{faq_html(FAQ_DIVE)}
</div>
<aside class="side"><div class="box"><h3>Get a Price</h3><p>Text a photo or video of your boat, its length and where it is kept.</p><a class="btn red block" href="sms:{PHONE_E164}">Text {PHONE_DISPLAY}</a><a class="btn outline block" href="tel:{PHONE_E164}">Call {PHONE_DISPLAY}</a></div></aside>
</section>""",
    [business_ld(), faq_schema(FAQ_DIVE), crumbs([("Home", "index.html"), ("Dive Services", "dive-services.html")])])

# Privacy and SMS terms. City and ZIP only. No street. Email stays a TODO.
LEGAL_EFFECTIVE = "November 28, 2026"
HOME_BASE = "Indian Rocks Beach, FL 33785"
privacy_body = f"""
<div class="wrap crumbs"><a href="index.html">Home</a> / <span>Privacy Policy</span></div>
<section class="wrap"><div class="svc-main">
<h1>Privacy Policy</h1>
<p class="lead">This policy describes how {BIZ} handles information you send when you ask for a quote or call or text us. Effective {LEGAL_EFFECTIVE}.</p>
<p>{BIZ} is owned by Shea Ganison. Phone: <a href="tel:{PHONE_E164}">{PHONE_DISPLAY}</a> (call or text).</p>
<p>Home base: {HOME_BASE}. No street address is published. This is a service-area business.</p>
<!-- TODO: add the business email. Do not guess. Do not publish the quote-form inbox here. -->
<p>A public email address is not listed on this page yet.</p>
<h2>What we collect</h2>
<p>If you use the quote form, we receive your name, phone number, city, the service you ask about, and your message. Email is optional. The SMS consent box is optional and starts unchecked. If you call or text {PHONE_DISPLAY}, we receive that number and what you send.</p>
<h2>How we use it</h2>
<p>We use this information to reply to your request and to do the work you ask us to do. We do not sell your information. If the quote form is turned on, the form is delivered through the service named in the site settings so we can read it.</p>
<h2>Texts</h2>
<p>We text you only if you check the optional consent box on the form. Consent is not required to ask for a quote by phone. Details are in the <a href="sms-terms.html">SMS terms</a>.</p>
<h2>How long we keep it</h2>
<p>We keep quote requests long enough to answer them and to keep a record of work you asked us to do. You can ask us to delete a request by calling or texting {PHONE_DISPLAY}.</p>
</div></section>"""
pages["privacy-policy.html"] = page(
    "privacy-policy.html",
    "Sea Dog Marine Privacy Policy | Tampa Bay, Florida",
    "Sea Dog Marine privacy policy for Tampa Bay quote requests. Phone 727-699-4920. Owner Shea Ganison. Home base is Indian Rocks Beach, FL 33785.",
    privacy_body,
    [business_ld(), crumbs([("Home", "index.html"), ("Privacy Policy", "privacy-policy.html")])],
)

sms_body = f"""
<div class="wrap crumbs"><a href="index.html">Home</a> / <span>SMS Terms</span></div>
<section class="wrap"><div class="svc-main">
<h1>SMS Terms</h1>
<p class="lead">These terms cover optional text messages from {BIZ}. Effective {LEGAL_EFFECTIVE}.</p>
<p>{BIZ} is owned by Shea Ganison. Texts come from <a href="tel:{PHONE_E164}">{PHONE_DISPLAY}</a>.</p>
<p>Home base: {HOME_BASE}. No street address is published. This is a service-area business.</p>
<!-- TODO: add the business email. Do not guess. Do not publish the quote-form inbox here. -->
<p>A public email address is not listed on this page yet.</p>
<h2>Optional consent</h2>
<p>The quote form has an SMS consent checkbox. It is unchecked unless you check it. Checking it is optional. You can still ask for a quote by calling or texting {PHONE_DISPLAY} without checking the box.</p>
<h2>What the texts are about</h2>
<p>If you opt in, we may text you about the quote or the job you asked about. Message frequency varies with that request. This is not a standing promotional list.</p>
<h2>Cost</h2>
<p>Message and data rates may apply. That depends on your mobile plan. {BIZ} does not charge a separate fee for the texts.</p>
<h2>Opt out and help</h2>
<p>Reply STOP to end texts. Reply HELP for help, or call or text {PHONE_DISPLAY}.</p>
<p>How we handle the information is in the <a href="privacy-policy.html">privacy policy</a>.</p>
</div></section>"""
pages["sms-terms.html"] = page(
    "sms-terms.html",
    "SMS Terms and Consent for Sea Dog Marine, Tampa Bay",
    "SMS terms for Sea Dog Marine texts in Tampa Bay. The consent box is optional and is not required to request a quote. Call or text 727-699-4920.",
    sms_body,
    [business_ld(), crumbs([("Home", "index.html"), ("SMS Terms", "sms-terms.html")])],
)

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

# Title tags stay 50-60 characters. H1s in blog_posts.py stay the full headline.
BLOG_META = {
    "how-often-clean-dock-tampa-bay": (
        "How Often to Clean a Dock in Tampa Bay | Sea Dog Marine",
        "Dock cleaning schedule in Pinellas, Hillsborough and Manatee. Most docks need barnacle removal every 6 to 12 months. Text for a free inspection.",
    ),
    "barnacles-vs-oysters-seawall": (
        "Barnacles vs Oysters on a Tampa Bay Seawall | Sea Dog Marine",
        "Seawall growth in Tampa Bay: how barnacles, oysters and algae differ on Pinellas, Hillsborough and Manatee walls. Text for a free video inspection.",
    ),
    "signs-seawall-failing": (
        "7 Seawall Warning Signs in Tampa Bay | Sea Dog Marine",
        "Seawall warning signs in Pinellas, Hillsborough and Manatee. Cleaning removes barnacles and oysters so cracks show. Text for a free video inspection.",
    ),
    "are-piling-wraps-worth-it": (
        "Are Piling Wraps Worth It in Tampa Bay? | Sea Dog Marine",
        "Piling wraps in Tampa Bay protect sound wood pilings from marine borers after barnacle and oyster removal. Text 727-699-4920 for a free video inspection.",
    ),
    "hurricane-prep-dock-seawall-checklist": (
        "Hurricane Prep Checklist for Tampa Bay | Sea Dog Marine",
        "Hurricane prep for docks and seawalls in Pinellas, Hillsborough and Manatee. Remove barnacles, then photograph the wall. Text for a free video inspection.",
    ),
    "after-storm-dock-seawall-inspection": (
        "After a Tampa Bay Storm: Dock Checklist | Sea Dog Marine",
        "After a Tampa Bay storm, check the dock, seawall and lift before cleaning. Document damage, then remove growth. Text for a free video inspection.",
    ),
    "barnacles-boat-lift-damage": (
        "How Barnacles Damage a Tampa Bay Boat Lift | Sea Dog Marine",
        "Boat lift cleaning in Tampa Bay stops barnacles and oysters from straining cables and scratching hulls. Text 727-699-4920 for a free video inspection.",
    ),
    "dock-ladder-safety": (
        "Tampa Bay Dock Ladder Safety for Guests | Sea Dog Marine",
        "Dock ladder cleaning in Tampa Bay removes sharp barnacles and slick slime so kids and guests can climb safely. Text for a free video inspection today.",
    ),
    "seawall-dock-cleaning-home-value": (
        "Clean a Tampa Bay Dock Before You Sell | Sea Dog Marine",
        "Dock and seawall cleaning before you sell a Tampa Bay home. Barnacle and oyster removal shows the real condition. Text for a free video inspection.",
    ),
    "wood-vs-composite-dock-florida": (
        "Wood vs Composite Docks in Tampa Bay | Sea Dog Marine",
        "Dock cleaning for wood and composite boards in Tampa Bay salt water, plus barnacle removal on pilings. Text 727-699-4920 for a free video inspection.",
    ),
    "marine-borers-dock-piling-rot": (
        "Marine Borers and Piling Rot in Tampa Bay | Sea Dog Marine",
        "Piling cleaning in Tampa Bay exposes marine borer damage and rot hidden by barnacles and oysters. Text 727-699-4920 for a free video inspection.",
    ),
    "vacation-rental-seasonal-dock-maintenance": (
        "Dock Care for Tampa Bay Vacation Rentals | Sea Dog Marine",
        "Dock and seawall care for Tampa Bay vacation rentals and seasonal homes. Barnacle removal and scheduled cleaning. Text for a free video inspection.",
    ),
    "canal-community-hoa-seawall-maintenance": (
        "Tampa Bay Seawall Care for Canal HOAs | Sea Dog Marine",
        "Seawall cleaning for canal HOAs in Apollo Beach, Ruskin and Bradenton. Barnacle and oyster removal on a shared schedule. Text for a free inspection.",
    ),
    "buying-waterfront-home-dock-seawall-inspection": (
        "What to Check on a Tampa Bay Dock | Sea Dog Marine",
        "Dock and seawall checks before buying a Tampa Bay waterfront home. Barnacle and oyster growth can hide damage. Text for a free video inspection.",
    ),
    "marine-growth-seasons-tampa-bay": (
        "Why Marine Growth Explodes in Tampa Bay | Sea Dog Marine",
        "Marine growth on Tampa Bay docks peaks in summer. Time barnacle and oyster removal for late spring and fall. Text for a free video inspection.",
    ),
    "diy-vs-professional-dock-cleaning": (
        "DIY vs Pro Dock Cleaning in Tampa Bay | Sea Dog Marine",
        "DIY vs professional dock and seawall cleaning in Tampa Bay. Barnacle and oyster removal is safer with the right method. Text for a free video inspection.",
    ),
}

def real_date(value):
    # TODO: posts keep published and modified blank until real YYYY-MM-DD dates are known. Do not invent dates.
    value = (value or "").strip()
    if not value or "TODO" in value.upper():
        return ""
    try:
        return datetime.date.fromisoformat(value).isoformat()
    except ValueError:
        return ""

def date_words(iso):
    parsed = datetime.date.fromisoformat(iso)
    months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    return f"{months[parsed.month - 1]} {parsed.day}, {parsed.year}"

for i, p in enumerate(POSTS):
    fn = "blog-" + p["slug"] + ".html"
    related_svc = "".join(f'<li><a href="{SVC_BY_SLUG[l]["slug"]}.html">{SVC_BY_SLUG[l]["name"]}</a></li>' for l in p["links"])
    nxt = [POSTS[(i + k) % len(POSTS)] for k in (1, 2, 3)]
    more = "".join(f'<li><a href="blog-{q["slug"]}.html">{q["title"]}</a></li>' for q in nxt)
    words = len(p["body"].split())
    published = real_date(p.get("published"))
    modified = real_date(p.get("modified"))
    quick = p.get("quick", "").strip()
    if not quick:
        raise SystemExit(f"missing quick answer for {p['slug']}")
    meta_bits = [f"By Shea Ganison, Owner, {BIZ}"]
    if published:
        meta_bits.append("Published: " + html.escape(date_words(published)))
    if modified:
        meta_bits.append("Updated: " + html.escape(date_words(modified)))
    meta_bits.append("Serving Pinellas, Hillsborough and Manatee Counties")
    meta_bits.append(f"{max(2, words // 200)} min read")
    date_note = ""
    if not published or not modified:
        date_note = "<!-- TODO: replace Published and Updated with the real dates for this post. datePublished and dateModified must use those same dates. Missing dates are omitted from the byline and from BlogPosting rather than shown as TODO or invented. -->"
    body = f"""
<div class="wrap crumbs"><a href="index.html">Home</a> / <a href="blog.html">Blog</a> / <span>{p['title']}</span></div>
<section class="wrap svc"><article class="svc-main post">
<h1>{p['title']}</h1>
<p><b>Quick answer.</b> {html.escape(quick)}</p>
<p class="meta">{' &middot; '.join(meta_bits)}</p>
{date_note}
<img class="svc-img" src="assets/{p['img']}" alt="{p['title']}" width="600" height="360">
{md(p['body'])}
<div class="inline-cta"><b>Free video inspection:</b> text a short video of your dock, seawall or lift to <a href="sms:{PHONE_E164}">{PHONE_DISPLAY}</a> for a same day recommendation and price.</div>
{faq_html(p['faqs'])}
</article>
<aside class="side"><div class="box"><h3>Get a Free Video Inspection</h3><a class="btn red block" href="sms:{PHONE_E164}">Text {PHONE_DISPLAY}</a><a class="btn outline block" href="tel:{PHONE_E164}">Call {PHONE_DISPLAY}</a></div>
<div class="box"><h3>Related Services</h3><ul>{related_svc}</ul></div>
<div class="box"><h3>More Articles</h3><ul>{more}</ul></div></aside>
</section>"""
    meta_title, meta_desc = BLOG_META[p["slug"]]
    art = {"@context": "https://schema.org", "@type": "BlogPosting", "headline": p["title"], "description": meta_desc,
           "image": SITE_URL + "/assets/" + p["img"],
           "author": {"@type": "Person", "name": "Shea Ganison", "jobTitle": "Owner, Sea Dog Marine", "worksFor": org_ref()},
           "publisher": org_ref(), "mainEntityOfPage": url(fn), "wordCount": words,
           "articleSection": "Waterfront Maintenance",
           "about": ["waterfront home maintenance", "Tampa Bay"],
           "spatialCoverage": [{"@type": "AdministrativeArea", "name": c["name"] + ", FL"} for c in COUNTIES.values()]}
    # Dates stay off the schema until they are real ISO dates. A TODO string would be invalid.
    article_meta = []
    if not (published and modified):
        article_meta.append('<!-- TODO: add article:published_time and article:modified_time when real dates are set on this post. Do not invent dates. -->')
    if published:
        art["datePublished"] = published
        article_meta.append(f'<meta property="article:published_time" content="{html.escape(published, quote=True)}">')
    if modified:
        art["dateModified"] = modified
        article_meta.append(f'<meta property="article:modified_time" content="{html.escape(modified, quote=True)}">')
    article_meta.append('<meta property="article:author" content="Shea Ganison">')
    article_meta.append('<meta property="article:section" content="Waterfront Maintenance">')
    date_comment = "<!-- TODO: BlogPosting datePublished and dateModified omitted until real dates are known. -->" if not (published and modified) else ""
    pages[fn] = page(fn, meta_title, meta_desc, body,
        [business_ld(), (date_comment, art), faq_schema(p["faqs"]), crumbs([("Home", "index.html"), ("Blog", "blog.html"), (p["title"], fn)])],
        og_img="assets/" + p["img"], og_type="article", extra_head="\n".join(article_meta) + "\n")

blog_cards = "".join(f"""<a class="card" href="blog-{p['slug']}.html"><img src="assets/{p['img']}" alt="{p['title']}" loading="lazy" width="560" height="360"><div><h3>{p['title']}</h3><p>{p['desc']}</p><span class="more">Read article</span></div></a>""" for p in POSTS)
pages["blog.html"] = page("blog.html", "Tampa Bay Dock and Seawall Care Blog | Sea Dog Marine",
    "Dock and seawall guides for Tampa Bay homeowners in Pinellas, Hillsborough and Manatee. Barnacle and oyster tips. Text for a free video inspection.",
    f"""<div class="wrap crumbs"><a href="index.html">Home</a> / <span>Blog</span></div>
<section class="wrap"><h1>Waterfront Home Maintenance Blog</h1><p class="lead">Straight answers for Tampa Bay waterfront homeowners on keeping docks, seawalls, pilings and lifts clean, safe and built to last.</p><div class="cards">{blog_cards}</div></section>""",
    [business_ld(), {"@context": "https://schema.org", "@type": "Blog", "name": f"{BIZ} Blog", "url": url("blog.html"), "publisher": org_ref(),
      "blogPost": [{"@type": "BlogPosting", "headline": p["title"], "url": url("blog-" + p["slug"] + ".html")} for p in POSTS]},
     crumbs([("Home", "index.html"), ("Blog", "blog.html")])])

# ------------------------------------------------------------------ write
def prior_site(out_dir):
    import re
    old_html, old_lastmod = {}, {}
    if not os.path.isdir(out_dir):
        return old_html, old_lastmod
    sm_path = os.path.join(out_dir, "sitemap.xml")
    if os.path.exists(sm_path):
        old_lastmod = dict(re.findall(r"<loc>(.*?)</loc><lastmod>(.*?)</lastmod>", open(sm_path).read()))
    for name in os.listdir(out_dir):
        if name.endswith(".html"):
            old_html[name] = open(os.path.join(out_dir, name), encoding="utf-8").read()
    return old_html, old_lastmod

old_html, old_lastmod = prior_site(OUT)
if os.path.exists(OUT):
    shutil.rmtree(OUT)
os.makedirs(OUT + "/assets")
for f in os.listdir("assets"):
    shutil.copy("assets/" + f, OUT + "/assets/" + f)
for fn, doc in pages.items():
    open(f"{OUT}/{fn}", "w").write(doc)

not_found = page(
    "404.html",
    "Page Not Found in Tampa Bay | Sea Dog Marine",
    "That page is not on the Sea Dog Marine site. Call or text 727-699-4920 for dock and seawall cleaning in Pinellas, Hillsborough and Manatee counties.",
    f"""<div class="wrap crumbs"><a href="index.html">Home</a> / <span>Page not found</span></div>
<section class="wrap"><h1>Page not found</h1>
<p class="lead">That page is not on the {BIZ} site. Go back to the home page, or call or text {PHONE_DISPLAY} for dock, seawall, piling, ladder, boat lift and hull cleaning in Pinellas, Hillsborough and Manatee counties.</p>
<ul class="checks col"><li><a href="index.html">Home</a></li><li><a href="dock-cleaning.html">Dock cleaning</a></li><li><a href="seawall-cleaning.html">Seawall cleaning</a></li><li><a href="hull-cleaning.html">Hull and boat bottom cleaning</a></li><li><a href="dive-services.html">Dive services</a></li><li><a href="service-areas.html">Service areas</a></li><li><a href="free-video-inspection.html">Free video inspection</a></li></ul>
<p><a class="btn red" href="index.html">Back to home</a></p>
</section>""",
    [],
    robots="noindex, follow",
)
open(f"{OUT}/404.html", "w").write(not_found)

prio = {"index.html": "1.0", "free-video-inspection.html": "0.9"}
sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
blog_locs = []
for fn, doc in pages.items():
    loc = url(fn)
    # Keep the previous lastmod when the HTML did not change. 404 is not a sitemap URL.
    if old_html.get(fn) == doc and loc in old_lastmod:
        lastmod = old_lastmod[loc]
    else:
        lastmod = TODAY
    if fn == "blog.html":
        blog_locs.append(loc)
    sm += f"  <url><loc>{loc}</loc><lastmod>{lastmod}</lastmod><priority>{prio.get(fn, '0.8')}</priority></url>\n"
if len(blog_locs) != 1:
    raise SystemExit("blog.html must appear exactly once in the sitemap")
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

def page_meta(fn):
    import re
    doc = pages[fn]
    title = html.unescape(re.search(r"<title>(.*?)</title>", doc).group(1))
    desc = html.unescape(re.search(r'<meta name="description" content="(.*?)">', doc).group(1))
    return title, desc

def llms_link(fn):
    title, desc = page_meta(fn)
    return f"- [{title}]({url(fn)}): {desc}"

llms = f"""# {BIZ}

> {BIZ} is a marine cleaning and maintenance company serving waterfront property owners in Pinellas, Hillsborough and Manatee counties, Florida (Tampa Bay). Call or text {PHONE_DISPLAY} for a free video inspection.

## Key facts
- Business name: {BIZ}
- Phone (call or text): {PHONE_DISPLAY}
- Based in Indian Rocks Beach, serving Pinellas, Hillsborough and Manatee. No public street address.
- Service area: Pinellas County, Hillsborough County and Manatee County, Florida
- Cities: {', '.join(sum([c['cities'] for c in COUNTIES.values()], []))}
- Removes: algae, barnacles, oysters, mold and marine growth
- Dive services: in-water hull and boat bottom cleaning, zinc anode replacement and propeller cleaning at the customer's dock, lift or slip
- Free video inspections: text a video or photos for a same day quote
- Hours: {'; '.join(h[3] for h in HOURS)}

## Services
""" + "\n".join(llms_link(s["slug"] + ".html") for s in SERVICES) + "\n" + llms_link("dive-services.html") + """

## Service areas
""" + "\n".join(llms_link(c["slug"] + ".html") for c in COUNTIES.values()) + "\n" + llms_link("service-areas.html") + "\n" + "\n".join(llms_link(c["slug"] + ".html") for c in CITIES) + f"""

## Contact
""" + llms_link("free-video-inspection.html") + """

## Policies
""" + llms_link("privacy-policy.html") + "\n" + llms_link("sms-terms.html") + """

## Guides for waterfront homeowners
""" + llms_link("blog.html") + "\n" + "\n".join(llms_link("blog-" + p["slug"] + ".html") for p in POSTS) + "\n"
if PHONE_DISPLAY not in llms or "Pinellas County, Hillsborough County and Manatee County" not in llms:
    raise SystemExit("llms.txt is missing the phone number or service area")
if "\u2014" in llms:
    raise SystemExit("em dash in llms.txt")
for s in SERVICES:
    if url(s["slug"] + ".html") not in llms:
        raise SystemExit(f"llms.txt missing {s['slug']}")
for c in COUNTIES.values():
    if url(c["slug"] + ".html") not in llms:
        raise SystemExit(f"llms.txt missing {c['slug']}")
for city in CITIES:
    if url(city["slug"] + ".html") not in llms:
        raise SystemExit(f"llms.txt missing {city['slug']}")
    if city["intro"] in [other["intro"] for other in CITIES if other is not city]:
        raise SystemExit(f"duplicate city intro for {city['name']}")
for p in POSTS:
    if url("blog-" + p["slug"] + ".html") not in llms:
        raise SystemExit(f"llms.txt missing {p['slug']}")
for legal in ("privacy-policy.html", "sms-terms.html"):
    if url(legal) not in llms:
        raise SystemExit(f"llms.txt missing {legal}")
open(f"{OUT}/llms.txt", "w").write(llms)

def assert_meta(pages):
    import re
    titles, descs = [], []
    for fn, doc in pages.items():
        raw_title = re.search(r"<title>(.*?)</title>", doc).group(1)
        raw_desc = re.search(r'<meta name="description" content="(.*?)">', doc).group(1)
        title = html.unescape(raw_title)
        desc = html.unescape(raw_desc)
        if not (50 <= len(title) <= 60):
            raise SystemExit(f"title length {len(title)} for {fn}: {title}")
        if "Tampa Bay" not in title and not any(city["name"] in title for city in CITIES):
            raise SystemExit(f"title needs a city or Tampa Bay: {fn}: {title}")
        if not (140 <= len(desc) <= 155):
            raise SystemExit(f"description length {len(desc)} for {fn}: {desc}")
        if "\u2014" in doc:
            raise SystemExit(f"em dash in {fn}")
        og_title = re.search(r'<meta property="og:title" content="(.*?)">', doc).group(1)
        tw_title = re.search(r'<meta name="twitter:title" content="(.*?)">', doc).group(1)
        og_desc = re.search(r'<meta property="og:description" content="(.*?)">', doc).group(1)
        tw_desc = re.search(r'<meta name="twitter:description" content="(.*?)">', doc).group(1)
        if og_title != raw_title or tw_title != raw_title:
            raise SystemExit(f"title mismatch on {fn}")
        if og_desc != raw_desc or tw_desc != raw_desc:
            raise SystemExit(f"description mismatch on {fn}")
        titles.append(title)
        descs.append(desc)
        if fn.startswith("blog-"):
            if 'property="og:type" content="article"' not in doc:
                raise SystemExit(f"blog og:type is not article on {fn}")
            if "<b>Quick answer.</b>" not in doc:
                raise SystemExit(f"missing quick answer on {fn}")
            if 'property="article:author" content="Shea Ganison"' not in doc:
                raise SystemExit(f"missing article:author on {fn}")
            if "Published: TODO" in doc or "Updated: TODO" in doc:
                raise SystemExit(f"visible TODO date on {fn}")
            if not real_date(next(p.get("published") for p in POSTS if fn == "blog-" + p["slug"] + ".html")):
                if '"datePublished"' in doc:
                    raise SystemExit(f"datePublished set without a real date on {fn}")
            if not real_date(next(p.get("modified") for p in POSTS if fn == "blog-" + p["slug"] + ".html")):
                if '"dateModified"' in doc:
                    raise SystemExit(f"dateModified set without a real date on {fn}")
            if 'property="article:section" content="Waterfront Maintenance"' not in doc:
                raise SystemExit(f"missing article:section on {fn}")
            if '"@type": "Person"' not in doc or '"jobTitle": "Owner, Sea Dog Marine"' not in doc:
                raise SystemExit(f"BlogPosting author is not the owner Person on {fn}")
            if '"worksFor": {"@id": "' + SITE_URL + '/#business"}' not in doc:
                raise SystemExit(f"author worksFor @id mismatch on {fn}")
    if len(set(titles)) != len(titles):
        raise SystemExit("duplicate title tags")
    if len(set(descs)) != len(descs):
        raise SystemExit("duplicate meta descriptions")
    if set(BLOG_META) != {p["slug"] for p in POSTS}:
        raise SystemExit("BLOG_META slugs do not match posts")

def assert_schema(pages):
    import re
    service_pages = {s["slug"] + ".html": s for s in SERVICES}
    county_pages = {c["slug"] + ".html": (key, c) for key, c in COUNTIES.items()}
    city_pages = {c["slug"] + ".html": c for c in CITIES}
    seen_business = False
    for fn, doc in pages.items():
        for raw in re.findall(r'<script type="application/ld\+json">(.*?)</script>', doc):
            data = json.loads(raw)
            if "aggregateRating" in raw or re.search(r'"review"\s*:', raw):
                raise SystemExit(f"review or rating schema on {fn}")
            if data.get("@id") == SITE_URL + "/#business":
                seen_business = True
                if data.get("@type") != ["HomeAndConstructionBusiness", "LocalBusiness"]:
                    raise SystemExit(f"business @type changed on {fn}")
                founder = data.get("founder") or {}
                if founder.get("@type") != "Person" or founder.get("name") != "Shea Ganison":
                    raise SystemExit(f"founder missing on {fn}")
                if founder.get("worksFor", {}).get("@id") != SITE_URL + "/#business":
                    raise SystemExit(f"founder worksFor @id mismatch on {fn}")
                for key in ("email", "sameAs", "hasMap", "geo"):
                    if key in data:
                        raise SystemExit(f"{key} shipped without real data on {fn}")
                addr = data.get("address") or {}
                if "streetAddress" in addr:
                    raise SystemExit(f"street address shipped on {fn}")
                if addr.get("addressRegion") != "FL" or addr.get("addressCountry") != "US":
                    raise SystemExit(f"address region changed on {fn}")
                if addr.get("addressLocality") != real_text(BASE_CITY) or addr.get("postalCode") != real_text(POSTAL_CODE):
                    raise SystemExit(f"address locality or ZIP mismatch on {fn}")
            if data.get("@type") == "Service":
                for key in ("serviceType", "description", "areaServed", "provider"):
                    if not data.get(key):
                        raise SystemExit(f"Service missing {key} on {fn}")
                if data["provider"].get("@id") != SITE_URL + "/#business":
                    raise SystemExit(f"Service provider @id mismatch on {fn}")
                if "offers" in data:
                    raise SystemExit(f"Service.offers present without real prices on {fn}")
                names = [a.get("name") for a in data["areaServed"]]
                desc = html.unescape(re.search(r'<meta name="description" content="(.*?)">', doc).group(1))
                if data["description"] != desc:
                    raise SystemExit(f"Service description does not match meta description on {fn}")
                if fn in service_pages:
                    for county in COUNTIES.values():
                        if county["name"] + ", FL" not in names:
                            raise SystemExit(f"{fn} missing {county['name']}")
                        for city in county["cities"]:
                            if city + ", FL" not in names:
                                raise SystemExit(f"{fn} missing {city}")
                if fn in county_pages:
                    key, county = county_pages[fn]
                    if county["name"] + ", FL" not in names:
                        raise SystemExit(f"{fn} missing its county")
                    for city in county["cities"]:
                        if city + ", FL" not in names:
                            raise SystemExit(f"{fn} missing {city}")
                    for other in COUNTIES.values():
                        if other["name"] != county["name"] and other["name"] + ", FL" in names:
                            raise SystemExit(f"{fn} includes another county")
                if fn in city_pages:
                    city = city_pages[fn]
                    county_name = COUNTIES[city["county"]]["name"] + ", FL"
                    expected = {city["name"] + ", FL", county_name}
                    if set(names) != expected:
                        raise SystemExit(f"{fn} areaServed should be the city and its county, got {names}")
            def walk(obj):
                if isinstance(obj, dict):
                    ref = obj.get("@id")
                    if isinstance(ref, str) and ref.endswith("#business") and ref != SITE_URL + "/#business":
                        raise SystemExit(f"inconsistent business @id on {fn}: {ref}")
                    for value in obj.values():
                        walk(value)
                elif isinstance(obj, list):
                    for value in obj:
                        walk(value)
            walk(data)
        if fn != "404.html" and 'id="https://www.seadogmarinefl.com/#business"' not in doc and '"@id": "https://www.seadogmarinefl.com/#business"' not in doc:
            raise SystemExit(f"missing business @id on {fn}")
    if not seen_business:
        raise SystemExit("no LocalBusiness schema")

assert_meta(pages)
assert_schema(pages)
not_found_html = open(f"{OUT}/404.html").read()
if "<title>Page Not Found in Tampa Bay | Sea Dog Marine</title>" not in not_found_html:
    raise SystemExit("404 title is wrong")
if 'name="robots" content="noindex, follow"' not in not_found_html:
    raise SystemExit("404 robots must be noindex, follow")
if "application/ld+json" in not_found_html:
    raise SystemExit("404 must not repeat homepage schema")
if "404.html" in open(f"{OUT}/sitemap.xml").read():
    raise SystemExit("404 must stay out of the sitemap")
sitemap_text = open(f"{OUT}/sitemap.xml").read()
for legal in ("privacy-policy.html", "sms-terms.html"):
    if url(legal) not in sitemap_text:
        raise SystemExit(f"sitemap missing {legal}")
    if f'href="{legal}"' not in pages["index.html"]:
        raise SystemExit(f"footer missing {legal}")
for form_page in ("index.html", "free-video-inspection.html"):
    doc = pages[form_page]
    if 'id="quote-form"' not in doc or 'name="sms_consent"' not in doc:
        raise SystemExit(f"quote form missing on {form_page}")
    if 'href="sms-terms.html"' not in doc:
        raise SystemExit(f"form missing SMS terms link on {form_page}")
    key, endpoint = configured_form()
    if not key and not endpoint and "Please call or text 727-699-4920" not in doc:
        raise SystemExit(f"missing call fallback on {form_page}")
    if endpoint or key:
        if 'id="quote-form" hidden' in doc:
            raise SystemExit(f"quote form should be visible on {form_page}")
        for token in ('_subject: "New quote request - Sea Dog Marine"', '_template: "table"', '_captcha: "false"', 'name="_honey"'):
            if token not in doc:
                raise SystemExit(f"quote form missing {token} on {form_page}")
        if "Thank you. We received your quote request." not in doc:
            raise SystemExit(f"missing thank-you message on {form_page}")
for city in CITIES:
    doc = pages[city["slug"] + ".html"]
    h1 = f"Dock, Seawall and Hull Cleaning in {city['name']}, FL"
    if f"<h1>{h1}</h1>" not in doc:
        raise SystemExit(f"missing H1 on {city['slug']}")
    if PHONE_DISPLAY not in doc:
        raise SystemExit(f"missing phone on {city['slug']}")
    if f'href="{city["slug"]}.html"' not in pages["service-areas.html"]:
        raise SystemExit(f"hub missing {city['name']}")
    if f'href="{city["slug"]}.html"' not in pages["index.html"]:
        raise SystemExit(f"footer missing {city['name']}")
    if url(city["slug"] + ".html") not in open(f"{OUT}/sitemap.xml").read():
        raise SystemExit(f"sitemap missing {city['slug']}")
for s in DIVE_SERVICES:
    doc = pages[s["slug"] + ".html"]
    for heading in ("What it is", "Why it matters in Tampa Bay saltwater", "The process"):
        if f"<h2>{heading}</h2>" not in doc:
            raise SystemExit(f"{s['slug']} missing {heading}")
    if '"@type": "FAQPage"' not in doc or '"@type": "Service"' not in doc:
        raise SystemExit(f"{s['slug']} missing FAQ or Service schema")
    if 'href="dive-services.html"' not in pages["index.html"]:
        raise SystemExit("homepage nav missing dive services")
print("Built", len(pages), "pages")
