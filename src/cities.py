# -*- coding: utf-8 -*-
"""
Batch 1 city dataset — California Central Coast.

Every field below is either (a) researched public data (2020 U.S. Census
population, utility water-quality reports, USPS ZIP codes, city/county
program pages) or (b) generic, hedged plumbing guidance that makes no
unverifiable claim.

RULES OBSERVED:
  * No invented testimonials, ratings, review counts or response times.
  * No invented founding years, addresses or owner names.
  * No claim about how many plumbers are "in our network".
  * Water-hardness numbers are attributed to the publishing utility, and each
    page says readings vary by zone, blend and season.
  * `issue` is written fresh for every city — different facts, different
    sentence order, different length. Do not normalise these into a template.

Adding a city = append a dict here + re-run `python3 src/build.py`.
"""

CITIES = [

# --------------------------------------------------------------------------- 1
dict(
    slug="salinas", name="Salinas", county="Monterey County",
    population="163,542", pop_note="2020 U.S. Census",
    zips=["93901", "93905", "93906", "93907"],
    neighborhoods=["East Salinas (Alisal District)", "North Salinas", "Creekbridge",
                   "Palma Vista", "Natividad", "Downtown / Main Street", "Harden Ranch",
                   "Los Pueblos"],
    nearby=["Prunedale", "Boronda", "Spreckels", "Castroville", "Marina", "Seaside",
            "Chualar", "San Juan Bautista"],
    landmarks=["Monterey County Courthouse", "the National Steinbeck Center",
               "Salinas River"],
    fact=("Salinas is the county seat of Monterey County and its largest city, with 163,542 "
          "residents at the 2020 Census, sitting roughly ten miles southeast of the mouth of "
          "the Salinas River."),
    sources=("Water hardness figures are from Cal Water's published water quality reports for the Salinas and Salinas Hills systems; softener setting guidance is published by Monterey One Water, the regional wastewater agency."),
    issue=("Salinas has some of the hardest municipal water on the Central Coast. Cal Water's "
           "published quality reports put the average in the Salinas system near 254 parts per "
           "million — about 15 grains per gallon — and the Salinas Hills system closer to 320 ppm, "
           "which the utility itself classifies as very hard. That mineral load shows up as crusted "
           "aerators, scale-choked water heater tanks and failing fill valves, and it is the reason "
           "Monterey One Water, the regional wastewater agency, publishes guidance that softeners in "
           "Monterey County be set between 15 and 30 grains per gallon rather than at the factory "
           "maximum. A large share of Salinas housing is also post-war single-family stock built "
           "between 1950 and 2000, so galvanized supply lines that have never been replaced are "
           "common in older pockets of the city."),
    services=["Drain and sewer cleaning", "Water heater repair and replacement",
              "Water softener installation and service", "Slab and under-sink leak repair",
              "Fixture and faucet replacement", "Gas line and shutoff valve work",
              "Repiping of galvanized supply lines", "Sewer camera inspection"],
    faq=[
        ("Is the water in Salinas hard enough to damage my plumbing?",
         "Salinas water is hard by any published measure — Cal Water's reports average near "
         "254 ppm in town and higher in the Salinas Hills area. Hard water is not a health "
         "problem, but it does scale up water heaters, aerators and valves over time. Ask a "
         "plumber to check the anode rod and tank sediment if your water heater is more than a "
         "few years old."),
        ("Do I need a permit or special settings to install a water softener here?",
         "Softener sizing, drain access and brine discharge are all regulated locally, and "
         "Monterey One Water publishes recommended hardness settings for Monterey County. A "
         "licensed plumber will know what the local agency requires before the unit is set in "
         "place — that conversation is worth having before you buy equipment."),
        ("My water pressure dropped in one bathroom. What is usually behind that in Salinas?",
         "Two things dominate: scale narrowing a valve or aerator, and corrosion inside older "
         "galvanized supply pipe. Both are diagnosable in a short visit, and both are cheaper to "
         "catch before a fitting lets go."),
    ],
),

# --------------------------------------------------------------------------- 2
dict(
    slug="monterey", name="Monterey", county="Monterey County",
    population="30,218", pop_note="2020 U.S. Census",
    zips=["93940", "93942", "93943", "93944"],
    neighborhoods=["New Monterey", "Old Monterey / State Historic Park area", "Del Monte",
                   "Skyline Forest", "Casanova-Oak Knoll", "North Fremont"],
    nearby=["Pacific Grove", "Carmel-by-the-Sea", "Del Rey Oaks", "Sand City", "Seaside",
            "Pebble Beach", "Carmel Valley Village", "Big Sur"],
    landmarks=["Cannery Row", "the Monterey Bay Aquarium", "the Custom House"],
    fact=("Monterey was the capital of both Spanish and Mexican California, and the Royal Presidio "
          "Chapel, founded in 1770, is the oldest continuously operating parish in the state — the "
          "city recorded 30,218 residents at the 2020 Census."),
    sources=("Hardness figures are from the Monterey Water System's annual drinking water quality report (PWS ID CA2710004). Neighborhood and historic-housing detail reflects the City of Monterey's historic context statements."),
    issue=("Two things age plumbing in Monterey faster than in most inland California cities: salt "
           "air and old buildings. Coastal salt accelerates corrosion on exposed brass, copper and "
           "steel fittings, on water heater flues and on outdoor hose bibs, and Old Monterey and "
           "New Monterey both carry housing stock that runs from Victorian and Craftsman bungalow "
           "through mid-century cottages and converted cannery-era commercial space. In practice "
           "that means a lot of pre-1970 supply pipe, older cast iron drains, and remodels where a "
           "historic fabric constraint makes access harder. The Monterey Water System's annual "
           "report lists total hardness averaging about 169 ppm, with a reported range from "
           "non-detect to 233 ppm, so scale is a moderate rather than extreme concern here."),
    services=["Sewer camera inspection and lateral repair", "Corroded fitting and hose bib replacement",
              "Water heater service", "Bathroom and kitchen remodel plumbing",
              "Cast iron drain replacement", "Leak detection", "Gas line repair",
              "Tankless water heater installation"],
    faq=[
        ("Do older Monterey homes still have the original plumbing?",
         "Plenty do, particularly in the Victorian, Craftsman and mid-century pockets around Old "
         "Monterey and New Monterey. A camera inspection of the sewer lateral and a look at the "
         "supply pipe material will tell you what you are actually dealing with, and both are "
         "routine requests."),
        ("Does the ocean air really affect plumbing?",
         "It affects anything metal and exposed: outdoor faucets, water heater vents and flues, "
         "brass valves in exterior walls, fasteners on tank straps. Corrosion shows up as green or "
         "white crusting at joints long before it becomes a leak."),
        ("I am buying a home in Monterey — what should the plumber check?",
         "Supply pipe material, water heater age and strapping, the condition of the sewer lateral "
         "from house to street, and whether any unpermitted remodel moved a fixture without "
         "reventing it. Those four items cover most of what surprises a new owner."),
    ],
),

# --------------------------------------------------------------------------- 3
dict(
    slug="watsonville", name="Watsonville", county="Santa Cruz County",
    population="52,590", pop_note="2020 U.S. Census",
    zips=["95075", "95076", "95077"],
    neighborhoods=["Downtown Watsonville", "Rio Del Mar area", "Pajaro (across the river)",
                   "Freedom / Amesti area", "Corralitos", "La Selva Beach area"],
    nearby=["Pajaro", "Freedom", "Amesti", "Corralitos", "La Selva Beach", "Watsonville Slough",
            "Aromas", "Salinas"],
    landmarks=["Watsonville Slough", "the Pajaro River", "Pinto Lake"],
    fact=("Watsonville sits at the mouth of the Pajaro River on the northern edge of Monterey Bay, "
          "and recorded 52,590 residents at the 2020 Census, making it the second-largest city in "
          "Santa Cruz County."),
    sources=('Flood history refers to the January 2023 Pajaro River levee failure. Point-of-sale well and septic testing rules are administered by Santa Cruz County.'),
    issue=("Watsonville's plumbing conversation is shaped by water in the wrong place. The Pajaro "
           "River levee system failed during the January 2023 atmospheric-river storms and flooded "
           "the neighboring community of Pajaro, and any home that took water needs its electrical, "
           "water heater and drain lines inspected by a licensed professional before it is put back "
           "into service — flooded water heaters and submerged supply lines are not a dry-out-and-"
           "continue situation. Away from flood risk, the Pajaro Valley's mix of older housing and "
           "agricultural properties means private wells, irrigation tie-ins and aging laterals come "
           "up often, and heavy clay soils in the valley floor shift pipe joints seasonally."),
    services=["Flood-damage plumbing inspection", "Sump and drain service", "Water heater replacement",
              "Sewer lateral repair", "Private well pump and pressure tank service",
              "Backflow prevention testing", "Leak detection", "Gas line repair"],
    faq=[
        ("My property took on water during a storm. What should a plumber look at first?",
         "The water heater, any submerged supply or drain line, and every electrical connection "
         "near plumbing equipment. Water heaters that have been flooded are generally replaced "
         "rather than repaired, and controls and gas valves that got wet are not reliable. Do not "
         "re-energize submerged equipment until it has been inspected."),
        ("Are private wells common in the Watsonville area?",
         "On the agricultural and unincorporated edges of the Pajaro Valley, yes. Well systems add "
         "pressure tanks, switches and treatment equipment to the plumbing picture, and Santa Cruz "
         "County has a point-of-sale well testing rule for properties on private wells or springs."),
        ("How do I stop a sewer backup during heavy rain?",
         "You often cannot stop it once the main is surcharged, but you can reduce the damage: know "
         "where your main cleanout is, keep it accessible, and ask a plumber whether a backwater "
         "valve is appropriate for your lateral. That is a code and site-specific question, not a "
         "one-size answer."),
    ],
),

# --------------------------------------------------------------------------- 4
dict(
    slug="santa-cruz", name="Santa Cruz", county="Santa Cruz County",
    population="62,956", pop_note="2020 U.S. Census",
    zips=["95060", "95062", "95064", "95067"],
    neighborhoods=["Westside", "Eastside / Branciforte", "Beach Hill", "Seabright", "Downtown",
                   "River Street", "Mission Hill", "UCSC / lower campus area", "Bonny Doon"],
    nearby=["Capitola", "Soquel", "Live Oak", "Aptos", "Scotts Valley", "Felton", "Ben Lomond",
            "Boulder Creek", "Bonny Doon"],
    landmarks=["the Santa Cruz Beach Boardwalk", "the San Lorenzo River", "Natural Bridges State Beach"],
    fact=("Santa Cruz is the county seat and largest city in Santa Cruz County, with 62,956 residents "
          "at the 2020 Census, and it sits on the northern edge of Monterey Bay at the mouth of the "
          "San Lorenzo River."),
    sources=('Pipe material and sewer lateral detail reflect the City of Santa Cruz sewer lateral ordinance (effective June 26, 2018) and City Public Works reporting; county point-of-sale septic and well programs are administered by Santa Cruz County.'),
    issue=("Santa Cruz's plumbing problems are overwhelmingly a function of how old the house is. "
           "Homes built before 1970 here were commonly plumbed with clay tile, cast iron or "
           "Orangeburg — a tar-and-paper composite that was standard mid-century material and "
           "simply was not built to last. All three fail the same way: joints separate, sections "
           "shift with soil movement, and tree roots find the hairline cracks. That is why the City "
           "adopted a sewer lateral ordinance that took effect June 26, 2018, requiring a video "
           "inspection of the private line from house to street at point of sale, and why the city "
           "counts roughly 16,000 private laterals against about 160 miles of public sewer main. "
           "In the coastal neighborhoods, salt air does its usual slow work on exposed brass and "
           "water heater flues."),
    services=["Sewer lateral video inspection", "Trenchless and open-cut lateral replacement",
              "Root cutting and hydro jetting", "Orangeburg and cast iron replacement",
              "Water heater replacement", "Leak detection", "Fixture and remodel plumbing",
              "Gas line and shutoff service"],
    faq=[
        ("Does Santa Cruz really require a sewer lateral inspection when I sell?",
         "Yes. The City of Santa Cruz sewer lateral ordinance took effect June 26, 2018 and applies "
         "to properties inside city limits that are on public sewer. Exemptions exist — for example "
         "a lateral built or completely replaced after 2010 and less than 20 years old, or one "
         "inspected and cleared within the past five years with documentation. Confirm your status "
         "with the City before escrow, because a kitchen remodel that never touched the sewer line "
         "does not reset the lateral's age."),
        ("What does a lateral inspection actually involve?",
         "A licensed plumber runs a camera from a cleanout through the private line to the connection "
         "at the public main, records the footage and submits the paperwork. City guidance has put "
         "inspection costs in the low hundreds and replacement from roughly a thousand dollars for a "
         "spot repair up to tens of thousands for a full lateral including work in the street."),
        ("I am on a well and septic outside city limits. Does the same rule apply?",
         "No, and this is a common mix-up. Santa Cruz County runs separate point-of-sale programs: "
         "one for septic systems and one for private wells and springs. Each has its own inspector "
         "list, forms and timeline, so check which jurisdiction your address is actually in."),
    ],
),

# --------------------------------------------------------------------------- 5
dict(
    slug="gilroy", name="Gilroy", county="Santa Clara County",
    population="59,520", pop_note="2020 U.S. Census",
    zips=["95020", "95021"],
    neighborhoods=["Downtown Gilroy", "Eagle Ridge", "Northeast Gilroy",
                   "South Gilroy / Morgan Hill Road corridor", "Gavilan District"],
    nearby=["Morgan Hill", "San Martin", "Aromas", "Hollister", "San Juan Bautista", "Coyote Valley"],
    landmarks=["the Gilroy Gardens area", "Mount Madonna County Park", "downtown Gilroy"],
    fact=("Gilroy is the southernmost city in Santa Clara County, home to Gilroy Gardens and the "
          "annual garlic festival that earned it the nickname Garlic Capital of the World, with "
          "59,520 residents at the 2020 Census."),
    sources=('Groundwater hardness context is from Santa Clara Valley Water District (Valley Water) published hardness information; population change is from U.S. Census Bureau decennial counts.'),
    issue=("Gilroy sits at the transition between Bay Area suburbs and Central Valley farmland, and "
           "its plumbing profile reflects both. Santa Clara Valley groundwater is mineral-heavy — "
           "the regional water agency Valley Water puts average hardness in county groundwater above "
           "250 mg/L, against less than 120 mg/L for its treated surface water — so homes on well or "
           "on blended supply see scale build up in water heaters and on valve seats. The city has "
           "also grown fast: population jumped from 48,821 in 2010 to 59,520 in 2020, and new "
           "subdivisions mean slab construction, where a leaking supply line under concrete is a "
           "different and more expensive job than the same leak in a crawlspace."),
    services=["Slab leak detection and repair", "Water heater replacement", "Repiping",
              "Drain and sewer cleaning", "Fixture installation", "Gas line service",
              "Water softener and filtration", "Irrigation backflow and plumbing tie-ins"],
    faq=[
        ("How do I know if I have a slab leak?",
         "The usual signs are an unexplained jump in the water bill, warm spots on a floor, the "
         "sound of running water when everything is off, or moisture wicking up at the base of "
         "slab-edge walls. Electronic leak detection locates it without tearing up the whole floor."),
        ("Is hard water a real issue in Gilroy?",
         "Groundwater in Santa Clara County is mineral-rich compared with imported surface water, so "
         "scale is a genuine consideration — how much depends on which supply your address draws "
         "from. A plumber can test hardness on site in minutes and tell you whether a softener or a "
         "point-of-use treatment makes sense."),
        ("Do new-build homes in Gilroy still have plumbing problems?",
         "Different ones. Slab access, undersized water heater placement, and long runs from the "
         "meter are more typical than corrosion or old cast iron. That is why it is worth getting "
         "the shutoff locations mapped out early, before you need them in a hurry."),
    ],
),

# --------------------------------------------------------------------------- 6
dict(
    slug="hollister", name="Hollister", county="San Benito County",
    population="41,678", pop_note="2020 U.S. Census",
    zips=["95023", "95024"],
    neighborhoods=["Downtown Hollister", "Northside", "Ridgemark area",
                   "Sunridge / Vista Hills area", "south Hollister along Highway 25"],
    nearby=["San Juan Bautista", "Aromas", "Tres Pinos", "Ridgemark", "Paicines", "Gilroy"],
    landmarks=["the San Benito County Courthouse", "historic downtown Hollister",
               "the Hollister Hills area"],
    fact=("Hollister is the county seat of San Benito County with 41,678 residents at the 2020 "
          "Census, and it sits on the eastern side of the Gabilan Range within sight of the San "
          "Andreas and Calaveras fault systems."),
    sources=('Hollister is the county seat of San Benito County. Water heater bracing requirements come from the California Plumbing Code and state seismic safety guidance.'),
    issue=("Seismic ground movement is the local variable in Hollister plumbing. The city sits close "
           "enough to active trace of the San Andreas system that soil creep and shaking both matter "
           "underground, where rigid connections between a house and a street main are the first "
           "thing to fail. In practice that means flexible connectors at the water heater, a "
           "working seismic gas shutoff, and supply lines that are not hard-piped through shifting "
           "soil are worth more here than cosmetic upgrades. Above ground, Hollister's housing is "
           "dominated by 1970s-through-2000s ranch stock with a substantial historic Victorian core "
           "downtown, so both aging copper and older galvanized pipe are in play."),
    services=["Water heater strapping and seismic bracing", "Automatic gas shutoff installation",
              "Flexible connector replacement", "Sewer lateral repair", "Repiping",
              "Drain cleaning", "Leak detection", "Fixture and appliance hookups"],
    faq=[
        ("Is my water heater strapped correctly?",
         "California requires water heaters to be braced against movement, and in a shaking-prone "
         "area it is worth checking the strapping, the pan, the flexible gas connector and the "
         "overflow routing all at once. A plumber can confirm compliance and fix the details in one "
         "visit."),
        ("Should I install an automatic gas shutoff valve?",
         "In Hollister it is a reasonable thing to ask about. These devices close the gas supply on "
         "detected shaking and are installed at the meter. Whether one is appropriate depends on "
         "your service setup and local requirements — get a licensed plumber or your gas utility to "
         "advise rather than buying a unit off the shelf."),
        ("What should I check on the plumbing side after an earthquake?",
         "Look for new moisture at the water heater connections, listen for running water with "
         "everything off, check the gas meter and flexible connectors, and confirm your main shutoff "
         "still turns. If you smell gas, leave and call the utility from outside."),
    ],
),

# --------------------------------------------------------------------------- 7
dict(
    slug="seaside", name="Seaside", county="Monterey County",
    population="32,366", pop_note="2020 U.S. Census",
    zips=["93955"],
    neighborhoods=["Noank", "East Seaside", "Fort Ord-area neighborhoods", "Downtown Seaside",
                   "Del Monte Blvd corridor", "CSUMB / former Fort Ord area"],
    nearby=["Monterey", "Marina", "Del Rey Oaks", "Sand City", "Salinas", "Pacific Grove"],
    landmarks=["California State University, Monterey Bay", "the former Fort Ord",
               "Monterey Bay Coastal Recreation Trail"],
    fact=("Seaside sits about two miles east of Monterey on the former Fort Ord, where California "
          "State University, Monterey Bay now occupies much of the old base land; the city recorded "
          "32,366 residents at the 2020 Census."),
    sources=("California State University, Monterey Bay occupies part of the former Fort Ord, which shapes much of the city's post-war housing stock."),
    issue=("Seaside's housing stock is largely post-war, built up around the army base, which means "
           "a large share of homes here carry original 1950s-through-1970s plumbing: galvanized "
           "steel supply pipe that rusts closed from the inside, cast iron drain stacks that crack "
           "at the hub, and water heaters sitting in garages or tight utility closets without pans. "
           "Because much of the city sits on the former Fort Ord, some properties are also on "
           "converted or non-standard infrastructure, and former base housing can have quirks in "
           "how laterals were originally run. Coastal salt air adds corrosion on any exposed metal, "
           "particularly at exterior hose bibs and water heater vents."),
    services=["Galvanized pipe replacement", "Cast iron stack repair", "Water heater replacement",
              "Sewer lateral inspection", "Leak detection", "Drain cleaning",
              "Fixture replacement", "Hose bib and exterior plumbing repair"],
    faq=[
        ("My home was built in the 1950s or 60s near the old base. What should I assume?",
         "Assume nothing and inspect. Post-war Seaside homes commonly have galvanized supply pipe "
         "and cast iron drains, both of which have a finite life, and both are hidden behind walls "
         "and under slabs until they fail. A supply-pipe material check and a camera inspection of "
         "the lateral is the fastest way to know where you stand."),
        ("Is rust-colored water in the morning a plumbing problem or a city problem?",
         "Usually the house. Galvanized pipe sheds rust overnight when water sits in it, and the "
         "first draw of the day carries it out. If the discoloration clears after a minute of "
         "running, that pattern points at your own supply pipe rather than the main."),
        ("Do converted Fort Ord-area properties have unusual plumbing?",
         "Some do, particularly where former base or government housing was adapted for residential "
         "use. Pipe routing, cleanout placement and lateral connections can differ from a standard "
         "tract build, which is worth knowing before a plumber quotes a repair sight unseen."),
    ],
),

# --------------------------------------------------------------------------- 8
dict(
    slug="santa-barbara", name="Santa Barbara", county="Santa Barbara County",
    population="88,665", pop_note="2020 U.S. Census",
    zips=["93101", "93103", "93105", "93107", "93108", "93109", "93110", "93111"],
    neighborhoods=["Downtown / State Street", "the Mesa", "Samarkand", "the Riviera",
                   "Westside", "Eastside", "Hope Ranch area", "Oak Park area"],
    nearby=["Montecito", "Summerland", "Carpinteria", "Goleta", "Isla Vista", "Mission Canyon"],
    landmarks=["the Santa Barbara Mission", "Stearns Wharf", "the Santa Barbara County Courthouse"],
    fact=("Santa Barbara anchors the South Coast of Santa Barbara County, with 88,665 residents at the "
          "2020 Census, and it is home to the Santa Barbara Mission, founded in "
          "1786, and to a downtown built in the Spanish Colonial Revival style after the 1925 "
          "earthquake."),
    sources=('Water hardness range reflects softener-setting guidance published locally for Santa Barbara supplies; the USGS hardness classification scale is used for interpretation.'),
    issue=("Santa Barbara has both hard water and hard geology. The city's water is genuinely "
           "mineral-rich — local guidance on softener settings puts Santa Barbara hardness in the "
           "20 to 25 grains per gallon range, which is well past the 10.5 gpg threshold the U.S. "
           "Geological Survey calls very hard — so scale accumulates in water heaters, on heating "
           "elements and inside fixture cartridges. The 1925 earthquake is why so much of the "
           "downtown streetscape looks the way it does, and the rebuilding era means a distinctive "
           "mix of pre-1925 Victorian and Craftsman housing alongside 1920s and 30s revival stock. "
           "Older hillside neighborhoods on the Riviera and in Mission Canyon add slope and access "
           "complications for sewer laterals."),
    services=["Water softener installation and service", "Water heater descaling and replacement",
              "Hillside lateral repair", "Leak detection", "Repiping", "Drain and root cutting",
              "Remodel and ADU plumbing", "Gas line service"],
    faq=[
        ("Is a water softener worth it in Santa Barbara?",
         "With hardness in the 20 to 25 grain range, most homeowners see a measurable difference in "
         "water heater life, fixture cartridge failures and spotting. Local guidance suggests "
         "setting the unit around 20 gpg rather than chasing the softest possible water, since "
         "over-softening wastes both salt and rinse water. Get a hardness test on your specific "
         "supply first."),
        ("What should I know about plumbing in an older hillside home?",
         "Access is the main issue. Laterals on slopes often have long runs, changes of direction "
         "and limited cleanout points, and getting equipment to the cleanout can matter as much as "
         "the repair itself. Ask for a camera inspection before committing to any excavation plan."),
        ("Are ADUs changing what plumbers do here?",
         "Noticeably. New units mean new sewer connections or upsized laterals, additional water "
         "heater capacity, and separate submeters in some cases. The plumbing scope is usually the "
         "part of an ADU project that is hardest to estimate from a floor plan alone."),
    ],
),

# --------------------------------------------------------------------------- 9
dict(
    slug="paso-robles", name="Paso Robles", county="San Luis Obispo County",
    population="31,490", pop_note="2020 U.S. Census",
    zips=["93446", "93447"],
    neighborhoods=["Downtown / City Park area", "Spring Street corridor",
                   "east side along Highway 46", "Creekside / Niblick area",
                   "west-side hills toward the wineries"],
    nearby=["Atascadero", "Templeton", "San Miguel", "Lake Nacimiento", "Estrella",
            "Santa Margarita", "Whitley Gardens"],
    landmarks=["Downtown Paso Robles City Park", "the Paso Robles Event Center",
               "the Salinas River"],
    fact=("Paso Robles sits on the Salinas River about 30 miles north of San Luis Obispo, with 31,490 "
          "residents at the 2020 Census, and the town grew up around its mineral hot springs — the "
          "name itself is a shortening of El Paso de Robles, the pass of the oaks."),
    sources=("The city's mineral hot springs and its position on the Salinas River are documented in local and county histories; hardness context reflects inland San Luis Obispo County supplies."),
    issue=("Those hot springs are a hint at the groundwater: Paso Robles water is mineral-laden, and "
           "inland SLO County supplies generally sit well above the 10.5 grains per gallon line the "
           "USGS calls very hard. Scale is therefore the default maintenance story — water heater "
           "tanks collecting sediment, tankless units throwing flow-error codes, and faucet "
           "cartridges seizing. The other local factor is expansive clay soil that swells and "
           "shrinks with the wet-dry cycle, which moves underground pipe and separates lateral "
           "joints, and the rural edges of town where wells and septic systems replace municipal "
           "service entirely."),
    services=["Water softener installation", "Tankless water heater service and descaling",
              "Water heater replacement", "Sewer lateral repair", "Well pump and pressure tank work",
              "Septic-side plumbing service", "Leak detection", "Whole-house filtration"],
    faq=[
        ("Why does my tankless water heater keep faulting here?",
         "Scale is the usual answer. Tankless units have narrow internal passages and a heat "
         "exchanger that fouls quickly in hard water, which is why manufacturers specify an annual "
         "descaling flush in mineral-heavy supply areas. If a unit is faulting on flow, that flush "
         "is the first thing a plumber will check."),
        ("Is well water common around Paso Robles?",
         "On the rural and vineyard-adjacent parcels outside city service, yes. Well plumbing adds "
         "pumps, pressure tanks, switches and often iron or sulfur treatment, and hardness varies "
         "widely from one well to the next — the only way to know yours is a certified lab test."),
        ("Do the soils here really move pipes?",
         "Clay that expands when wet and contracts when dry applies steady force to buried pipe, and "
         "the joints are where it shows. Root intrusion follows any joint that has shifted, which is "
         "why a camera inspection beats guessing on a slow drain."),
    ],
),

# --------------------------------------------------------------------------- 10
dict(
    slug="marina", name="Marina", county="Monterey County",
    population="22,359", pop_note="2020 U.S. Census",
    zips=["93933"],
    neighborhoods=["Marina Beach area", "Reservation Communities", "Downtown Marina",
                   "north Marina toward the dunes", "south Marina along Highway 1"],
    nearby=["Fort Ord area", "Seaside", "Monterey", "Salinas", "Castroville", "Del Rey Oaks"],
    landmarks=["Marina State Beach", "the Monterey Bay Coastal Recreation Trail",
               "the former Fort Ord dunes"],
    fact=("Marina sits directly on Monterey Bay between the former Fort Ord and the Salinas River "
          "mouth, and recorded 22,359 residents at the 2020 Census — most of its development dates "
          "from the post-war and base-era decades."),
    sources=('Marina sits between the former Fort Ord and the Salinas River mouth on Monterey Bay; coastal soil and water-table conditions are characteristic of the dune-adjacent areas.'),
    issue=("Marina is sandy, coastal and shallow-water-table, all three of which affect plumbing. "
           "Sandy soil offers little support for buried pipe, so bedding and backfill quality decide "
           "whether a lateral holds its grade over decades, and a high water table near the dunes "
           "means trenches fill and infiltration into old joints is a real risk. Salt air does "
           "steady corrosive work on exterior fixtures. Housing here is mostly post-war "
           "single-family stock with a significant share of homes on former base-adjacent land, so "
           "galvanized supply pipe and original cast iron drains are common finds in older sections."),
    services=["Lateral repair and replacement", "Sump and drainage work", "Water heater replacement",
              "Galvanized pipe replacement", "Leak detection", "Drain cleaning",
              "Exterior fixture and hose bib repair", "Trenchless sewer repair"],
    faq=[
        ("Does sandy soil change how a sewer line should be repaired?",
         "Yes. In sand, proper bedding, compaction and sometimes trench shielding matter more than "
         "they would in clay, and a shallow water table can mean dewatering during the dig. It is "
         "worth asking a plumber how they plan to bed and support the pipe, not just what the pipe "
         "costs."),
        ("Why does my drain run slowly when it rains?",
         "Infiltration. Groundwater entering through cracked or open-jointed pipe raises the level "
         "in the lateral and slows everything above it. A camera inspection will show whether the "
         "problem is a blockage inside the pipe or water coming in from outside it."),
        ("Is trenchless repair an option in Marina?",
         "Often, and it can be attractive where surface restoration over sandy ground or landscaping "
         "is expensive. Pipe lining and pipe bursting each have limits on bend angles and diameter "
         "change, so it is a site-specific decision rather than a default."),
    ],
),

# --------------------------------------------------------------------------- 11
dict(
    slug="pacific-grove", name="Pacific Grove", county="Monterey County",
    population="15,090", pop_note="2020 U.S. Census",
    zips=["93950"],
    neighborhoods=["Lovers Point area", "downtown Pacific Grove / Pine Avenue",
                   "Asilomar area", "Butterfly Grove neighborhood", "east side toward Del Monte"],
    nearby=["Monterey", "Del Rey Oaks", "Pebble Beach", "Carmel-by-the-Sea", "Seaside"],
    landmarks=["Point Pinos Lighthouse", "the Monarch Grove Sanctuary", "Asilomar State Beach"],
    fact=("Pacific Grove is a small coastal city on the tip of the Monterey Peninsula, population "
          "15,090 at the 2020 Census, known for the Point Pinos Lighthouse — the oldest continuously "
          "operating lighthouse on the West Coast — and for the monarch butterflies that overwinter "
          "in its groves."),
    sources=("Point Pinos Lighthouse is the oldest continuously operating lighthouse on the U.S. West Coast; the city's 1870s camp-meeting origins shaped its Victorian and cottage housing stock."),
    issue=("Pacific Grove's dominant plumbing story is the age of its houses. The city was laid out "
           "in the 1870s as a Methodist retreat and camp-meeting ground, and a large share of its "
           "housing is Victorian and early-twentieth-century cottages built to a modest budget, "
           "which means original or near-original galvanized supply pipe, cast iron and clay drains, "
           "and decades of piecemeal repairs behind plaster walls. Add continuous salt exposure — "
           "the city is surrounded by open bay and ocean on three sides — and corrosion at exposed "
           "fittings, water heater flues and exterior hose bibs is a routine finding rather than an "
           "exception."),
    services=["Older-home repiping", "Cast iron and clay drain replacement",
              "Sewer lateral camera inspection", "Water heater replacement", "Corrosion repair",
              "Fixture upgrades in historic homes", "Leak detection", "Gas line service"],
    faq=[
        ("I have an 1890s or 1920s cottage in Pacific Grove. What is likely under the floors?",
         "Commonly galvanized steel supply pipe, cast iron or clay waste lines, and evidence of "
         "several generations of repairs. None of that is automatically a problem, but knowing the "
         "materials tells you how much life is left. Ask for a materials check and a camera "
         "inspection at the same time."),
        ("Does the historic character of the neighborhood restrict plumbing work?",
         "Interior plumbing generally no, but exterior work, visible fixtures, and anything touching "
         "a designated historic property can involve local review. Check with the City of Pacific "
         "Grove before altering visible exterior elements; a plumber who works on historic homes "
         "locally will already know the process."),
        ("How much does salt air cost me in plumbing terms?",
         "It shortens the life of anything unprotected and exposed: hose bibs, backflow assemblies, "
         "water heater vents, brass valves in exterior walls, and tank straps. Rinsing exterior "
         "fixtures periodically and replacing corroded parts before they leak is cheaper than "
         "finding them after a failure."),
    ],
),

# --------------------------------------------------------------------------- 12
dict(
    slug="atascadero", name="Atascadero", county="San Luis Obispo County",
    population="29,773", pop_note="2020 U.S. Census",
    zips=["93422"],
    neighborhoods=["downtown / Administration Building area", "colony-era neighborhoods off El Camino Real",
                   "west-side hills", "the flats along El Camino Real", "Joaquin / Santa Ana area"],
    nearby=["Paso Robles", "Templeton", "Santa Margarita", "Morro Bay", "San Luis Obispo", "Creston"],
    landmarks=["the Atascadero Colony administration building", "Lake Nacimiento",
               "the Salinas River headwaters area"],
    fact=("Atascadero was founded in 1913 by E. G. Lewis as a planned colony, and that original "
          "large-lot subdivision still shapes the town's layout today; the city recorded 29,773 "
          "residents at the 2020 Census."),
    sources=("Atascadero was founded in 1913 by E. G. Lewis as a planned colony, and the original large-lot subdivision still shapes the city's layout."),
    issue=("Colony-era housing plus expansive clay is the Atascadero combination. Restored "
           "colony-period homes sit alongside standard suburban tracts and rural parcels, so a "
           "plumber here may be working on century-old pipe in one call and a 1990s slab in the "
           "next. The soils swell and shrink through the wet-dry cycle, which shifts buried laterals "
           "and separates joints, and the December 2003 San Simeon earthquake reminded the whole "
           "North County that unreinforced masonry and rigid utility connections move. Inland SLO "
           "County water is also hard, so scale in water heaters and tankless units is standard "
           "maintenance rather than a surprise."),
    services=["Sewer lateral repair", "Water softener installation", "Water heater replacement",
              "Seismic gas shutoff and flexible connectors", "Older-home repiping",
              "Drain and root cutting", "Well and septic-side plumbing", "Remodel plumbing"],
    faq=[
        ("What breaks first in an Atascadero home during shaking?",
         "Rigid connections: the water heater if it is not strapped and flexibly connected, hard-piped "
         "gas lines, and any supply line crossing a foundation joint. Flexible connectors, proper "
         "strapping and a working gas shutoff address most of that list."),
        ("Is the soil here a real plumbing problem?",
         "Expansive clay moves with moisture, and buried pipe feels it. The typical symptoms are a "
         "lateral that has lost its slope, joints that have opened to root intrusion, and drains "
         "that get progressively slower over years. A camera inspection documents the actual "
         "condition instead of guessing."),
        ("Do colony-era homes have original plumbing?",
         "Some do, in whole or in part, and the mix of materials in one house can be surprising. "
         "That is worth establishing early in any remodel, because tying new fixtures into "
         "century-old waste pipe is how leaks appear in places nobody expected."),
    ],
),

# --------------------------------------------------------------------------- 13
dict(
    slug="san-luis-obispo", name="San Luis Obispo", county="San Luis Obispo County",
    population="47,063", pop_note="2020 U.S. Census",
    zips=["93401", "93405", "93406", "93407", "93410"],
    neighborhoods=["Downtown / Higuera Street", "Foothill area", "the Meadows",
                   "Cerro / Bishop Peak foothills", "south SLO along Highway 101"],
    nearby=["Avila Beach", "Shell Beach", "Grover Beach", "Pismo Beach", "Atascadero", "Edna Valley"],
    landmarks=["Mission San Luis Obispo de Tolosa", "Bishop Peak", "Cal Poly"],
    fact=("San Luis Obispo grew up around Mission San Luis Obispo de Tolosa, founded in 1772, and is "
          "the county seat of San Luis Obispo County, with 47,063 residents at the 2020 Census and a large student presence from Cal Poly."),
    sources=('Mission San Luis Obispo de Tolosa was founded in 1772 and the city is the San Luis Obispo County seat.'),
    issue=("SLO's plumbing demand splits between two very different building types. Older "
           "neighborhoods near downtown and the mission carry pre-1960 housing with cast iron and "
           "clay waste lines and original galvanized supply, while the rental-heavy student market "
           "generates a steady volume of drain blockages and fixture abuse in multi-unit buildings. "
           "The foothills above town add slope-driven laterals with long runs and limited cleanout "
           "access. Inland county water is hard enough that water heater scale is a normal "
           "maintenance item."),
    services=["Drain and main line cleaning", "Sewer camera inspection", "Water heater replacement",
              "Multi-unit plumbing service", "Repiping of galvanized lines", "Leak detection",
              "Remodel and ADU plumbing", "Water softener service"],
    faq=[
        ("I manage a rental property near campus. What fails most often?",
         "Drains and fixtures. Student housing generates a high rate of blockages from grease, hair "
         "and foreign objects, plus worn flappers, loose supply connections and misused garbage "
         "disposals. None of it is complicated, and most of it is preventable with a short "
         "move-in briefing and an annual service visit."),
        ("Why is my hillside home's sewer line so expensive to work on?",
         "Access and length. Long runs with changes of direction need more cleanout points to service "
         "properly, and equipment has to be brought to the line rather than the reverse. Before any "
         "excavation quote, ask whether adding a cleanout would make future maintenance cheaper."),
        ("Is SLO water hard?",
         "Inland San Luis Obispo County supplies are generally hard by the USGS scale, which puts "
         "anything over 10.5 grains per gallon in the very hard category. Hardness varies by source "
         "and zone, so a quick on-site test is more useful than a regional average when you are "
         "deciding about a softener."),
    ],
),

# --------------------------------------------------------------------------- 14
dict(
    slug="santa-maria", name="Santa Maria", county="Santa Barbara County",
    population="109,707", pop_note="2020 U.S. Census",
    zips=["93454", "93455", "93456", "93457", "93458"],
    neighborhoods=["downtown Santa Maria / Broadway", "Foxenwood area",
                   "Preisker Park area", "Orcutt (adjacent)", "south Santa Maria along Highway 101"],
    nearby=["Orcutt", "Nipomo", "Guadalupe", "Lompoc", "Santa Barbara", "Los Alamos"],
    landmarks=["Allan Hancock College", "the Foxen Canyon wine trail", "Preisker Park"],
    fact=("Santa Maria is the largest city on the Central Coast south of the Salinas Valley, with "
          "109,707 residents at the 2020 Census and a 2024 estimate above 111,000, sitting roughly "
          "65 miles northwest of Santa Barbara."),
    sources=('All hardness figures are published by the City of Santa Maria Utilities Department (Water Services), which also posts current blended hardness readings on the city website.'),
    issue=("Santa Maria has the hardest water of any city in this list, and the city says so itself. "
           "Its Utilities Department publishes the numbers: local groundwater ranges from about 420 "
           "to 730 milligrams per liter of hardness — roughly 25 to 43 grains per gallon — while "
           "imported State Water comes in near 120 mg/L, or 7 gpg. The city blends the two, so a "
           "typical delivered blend lands around 250 mg/L (15 gpg) with a maximum blend around 300 "
           "mg/L (18 gpg), and the exact ratio shifts with rainfall and snowpack. At those levels "
           "scale is the single biggest wear factor on water heaters, tankless units, dishwasher "
           "pumps and faucet cartridges, and softener settings matter more than softener brand."),
    services=["Water softener installation and rebuild", "Water heater descaling and replacement",
              "Tankless flush service", "Fixture cartridge replacement", "Whole-house filtration",
              "Drain and sewer cleaning", "Leak detection", "Gas line service"],
    faq=[
        ("How hard is Santa Maria water, exactly?",
         "The City of Santa Maria publishes it: local groundwater runs about 420 to 730 mg/L (25 to "
         "43 gpg), imported State Water about 120 mg/L (7 gpg), and the delivered blend typically "
         "around 250 mg/L (15 gpg) with a maximum blend near 300 mg/L (18 gpg). The blend changes "
         "with rainfall and snowpack, and the city posts current hardness figures on its website."),
        ("Why does the hardness change during the year?",
         "Because the ratio of imported State Water to local groundwater changes. In wet years with a "
         "good Sierra snowpack the city can deliver more of the softer imported supply; in dry years "
         "it leans on the much harder groundwater. That is also why the city has asked customers to "
         "reduce softener use during periods when softer blended water is being delivered."),
        ("What should I set my softener to?",
         "Set it to your actual measured hardness, not to the factory maximum. Oversetting wastes "
         "salt, water and resin life, and it delivers water softer than you need. Have the hardness "
         "tested at your tap first, then have a plumber size and program the unit to that number."),
    ],
),

# --------------------------------------------------------------------------- 15
dict(
    slug="soledad", name="Soledad", county="Monterey County",
    population="24,925", pop_note="2020 U.S. Census",
    zips=["93960"],
    neighborhoods=["downtown Soledad", "north Soledad along Highway 101",
                   "east side toward the river", "newer subdivisions south of town"],
    nearby=["Greenfield", "Gonzales", "Salinas", "Chualar", "King City",
            "Mission Nuestra Señora de la Soledad"],
    landmarks=["Mission Nuestra Señora de la Soledad", "the Salinas River",
               "the Pinnacles National Park turnoff"],
    fact=("Soledad sits in the Salinas Valley 21 miles southeast of Salinas, population 24,925 at the "
          "2020 Census, and it is the closest town to the ruins of Mission Nuestra Señora de la "
          "Soledad, founded in 1791."),
    sources=("Mission Nuestra Señora de la Soledad was founded in 1791; hardness context reflects Cal Water's published reporting for the Salinas Valley."),
    issue=("Soledad is agricultural Salinas Valley, which means two distinct plumbing worlds inside "
           "one service area. In town, the housing is mostly modest mid-to-late twentieth-century "
           "single-family stock where galvanized supply pipe and original fixtures are still turning "
           "up. On the rural and farm-adjacent parcels, the work is wells, pressure tanks, pumps and "
           "septic systems rather than municipal connections. Valley groundwater is mineral-heavy — "
           "Cal Water's own reporting for the nearby Salinas system averages near 254 ppm — so scale "
           "in water heaters and on valve seats is a shared concern across both."),
    services=["Well pump and pressure tank service", "Water softener installation",
              "Septic-side plumbing and sewer line work", "Water heater replacement",
              "Drain cleaning", "Fixture replacement", "Leak detection",
              "Agricultural and outbuilding plumbing"],
    faq=[
        ("Is well water common around Soledad?",
         "On rural and agricultural parcels, yes. Well plumbing means a pump, pressure tank, switch "
         "and usually some treatment, and hardness and mineral content vary well to well. A "
         "certified lab test is the only reliable way to know what your water is doing to your "
         "fixtures and heater."),
        ("My pressure keeps cycling on and off. Is that the well or the plumbing?",
         "Usually the pressure tank or the switch rather than the well itself. A waterlogged tank "
         "loses its air cushion and makes the pump short-cycle, which shortens pump life quickly. It "
         "is a fast diagnosis and a cheap fix compared with replacing a pump that was never the "
         "problem."),
        ("What is the first thing to check when water pressure drops across the whole house?",
         "The pressure tank reading, then the main shutoff and any pressure-reducing valve at the "
         "house. If pressure is normal at the tank and low inside, the restriction is downstream — "
         "often a clogged filter, a failing PRV or scale-narrowed supply pipe."),
    ],
),

# --------------------------------------------------------------------------- 16
dict(
    slug="pismo-beach", name="Pismo Beach", county="San Luis Obispo County",
    population="8,072", pop_note="2020 U.S. Census",
    zips=["93448", "93449"],
    neighborhoods=["downtown Pismo Beach / Price Street", "Beach Street and the bluff area",
                   "Shell Beach (adjacent)", "Grover Heights area", "south Pismo toward the dunes"],
    nearby=["Grover Beach", "Shell Beach", "Oceano", "Arroyo Grande", "Avila Beach",
            "San Luis Obispo", "Nipomo"],
    landmarks=["Pismo Beach Pier", "the Monarch Butterfly Grove at Pismo State Beach",
               "the Oceano Dunes"],
    fact=("Pismo Beach is a small coastal city on the southern edge of San Luis Obispo County with a "
          "8,072 residents at the 2020 Census, built around its pier and the Monarch "
          "Butterfly Grove at Pismo State Beach."),
    sources=("The Monarch Butterfly Grove at Pismo State Beach and the Pismo Beach Pier are the city's defining coastal features."),
    issue=("Everything here is within a few hundred yards of open ocean, and that salt exposure is the "
           "defining maintenance factor. Coastal corrosion attacks exposed brass and copper, water "
           "heater flues and gas connections, exterior hose bibs, backflow assemblies and tank "
           "straps, and it does so quietly — the green and white crusting at a joint appears years "
           "before the leak. Bluff-side and near-dune properties also deal with sandy, shifting soil "
           "and, in places, a high water table, which affects how buried laterals hold their grade."),
    services=["Corrosion inspection and repair", "Water heater replacement and flue repair",
              "Backflow prevention testing", "Sewer lateral repair", "Exterior fixture replacement",
              "Leak detection", "Vacation and rental property plumbing checks",
              "Whole-house repiping"],
    faq=[
        ("How often should a coastal home have its plumbing looked at?",
         "An annual walk-through is reasonable, focused on the things salt attacks: exterior fixtures "
         "and hose bibs, the water heater and its venting, gas connections, and any exposed brass. "
         "For a part-time or rental property, add a pre-season check before the property is "
         "occupied."),
        ("I own a second home here that sits empty for months. What goes wrong?",
         "Stagnant water, dried-out trap seals, and corrosion that progresses without anyone "
         "noticing. A short service visit that flushes the system, checks trap seals, inspects the "
         "water heater and verifies shutoff operation covers most of it."),
        ("Does the ocean air really shorten water heater life?",
         "It shortens the life of the metal parts around it — flue, venting, straps, the burner "
         "assembly on gas units, and the fittings on top of the tank. The tank itself is glass-lined "
         "inside, but a corroded vent or a failed anode rod will end it early."),
    ],
),

# --------------------------------------------------------------------------- 17
dict(
    slug="morro-bay", name="Morro Bay", county="San Luis Obispo County",
    population="10,757", pop_note="2020 U.S. Census",
    zips=["93442"],
    neighborhoods=["the Embarcadero / waterfront", "downtown Morro Bay",
                   "north Morro Bay toward the state park", "hillside streets east of town",
                   "Los Osos (adjacent, unincorporated)"],
    nearby=["Los Osos", "Baywood Park", "Cayucos", "Atascadero", "San Luis Obispo", "Morro Bay State Park"],
    landmarks=["Morro Rock", "the Morro Bay Embarcadero", "Morro Bay State Park"],
    fact=("Morro Bay is a harbor town of 10,757 residents at the 2020 Census, built "
          "around a working waterfront and the volcanic plug known as Morro Rock, which rises "
          "directly out of the bay."),
    sources=('Morro Rock and the working Embarcadero define the harbor; adjacent unincorporated Los Osos and Baywood Park rely substantially on on-site septic systems.'),
    issue=("Morro Bay combines marine salt exposure with older waterfront housing and a working "
           "harbor. Salt-laden air is constant along the Embarcadero and in the streets behind it, "
           "so exposed brass, copper, galvanized pipe, water heater vents and exterior fixtures "
           "corrode faster than they would even a few miles inland. Much of the town's housing "
           "predates the 1970s, which means original cast iron and clay waste lines and galvanized "
           "supply pipe are still in service, and hillside lots east of town add slope and access "
           "complications for laterals. Adjacent unincorporated Los Osos and Baywood Park rely "
           "heavily on septic systems, which changes what a plumbing call looks like there."),
    services=["Corrosion and fitting replacement", "Cast iron and clay drain replacement",
              "Sewer lateral camera inspection", "Water heater replacement",
              "Septic-side plumbing service", "Leak detection", "Hillside lateral repair",
              "Marine and commercial fixture work"],
    faq=[
        ("Do septic properties around Morro Bay need different plumbing help?",
         "Yes. In Los Osos, Baywood Park and other nearby unincorporated areas, a lot of the work is "
         "septic-related: tank access, inlet and outlet baffle condition, distribution lines and "
         "what should never go down the drain. A plumber familiar with on-site systems is a "
         "different conversation from one who only works on municipal sewer."),
        ("Is corrosion visible before it becomes a leak?",
         "Usually. Look for white or green crust at brass joints, rust staining under galvanized "
         "fittings, flaking on water heater venting, and seized exterior valve handles. Catching it "
         "at the crust stage is a parts replacement; catching it at the leak stage is an opening-up-"
         "walls job."),
        ("What should a buyer check on an older Morro Bay home?",
         "Supply pipe material, the water heater and its venting, the sewer lateral condition and "
         "cleanout access, and whether any past remodel moved fixtures without proper venting. On a "
         "hillside lot, also ask how the lateral runs and where it can be serviced from."),
    ],
),

# --------------------------------------------------------------------------- 18
dict(
    slug="greenfield", name="Greenfield", county="Monterey County",
    population="18,937", pop_note="2020 U.S. Census",
    zips=["93927"],
    neighborhoods=["downtown Greenfield", "north Greenfield along Highway 101",
                   "south Greenfield toward King City", "east side toward the river"],
    nearby=["King City", "Soledad", "Chualar", "Gonzales", "Salinas", "San Ardo"],
    landmarks=["the Salinas River", "highway 101 corridor", "Salinas Valley farmland"],
    fact=("Greenfield is a small agricultural city in the upper Salinas Valley with 18,937 residents "
          "at the 2020 Census, located between Soledad and King City along Highway 101 in the "
          "farmland that gives Monterey County its Salad Bowl of the World reputation."),
    sources=("Greenfield lies in the upper Salinas Valley between Soledad and King City along Highway 101, in the farmland behind Monterey County's agricultural output."),
    issue=("Greenfield's plumbing profile is small-town Salinas Valley: mostly modest single-family "
           "homes built from the 1950s onward, surrounded by agricultural land where wells and "
           "septic systems take over from municipal service. Valley groundwater is hard and "
           "mineral-rich, and the surrounding soils are the same heavy valley-fill clays that move "
           "with moisture, so underground laterals shift at the joints and roots follow. Where "
           "properties are on wells, hardness is well-specific rather than predictable, and iron and "
           "manganese staining show up in fixtures alongside scale."),
    services=["Well pump and pressure tank repair", "Water softener and iron filtration",
              "Sewer lateral repair and camera inspection", "Water heater replacement",
              "Drain cleaning and root cutting", "Fixture replacement", "Leak detection",
              "Farm and outbuilding plumbing"],
    faq=[
        ("My well water stains fixtures orange-brown. What is that?",
         "Typically iron, sometimes with manganese, and both are common in valley groundwater. It is "
         "an aesthetic and staining problem rather than a safety one in most cases, and it is treated "
         "with filtration or oxidation systems rather than a standard water softener. Get the water "
         "tested so the treatment matches the actual concentration."),
        ("How does hard well water affect my water heater?",
         "The same way hard municipal water does, only less predictably. Mineral sediment collects at "
         "the bottom of the tank and insulates the water from the burner or element, which raises "
         "energy use and shortens tank life. Annual flushing and a working anode rod are the two "
         "things that matter most."),
        ("Are septic systems common around Greenfield?",
         "Outside the city's sewer service area, yes. Septic plumbing work centers on tank condition, "
         "inlet and outlet condition, and protecting the leach field from grease, solids and excess "
         "water. Pumping intervals depend on tank size and household size, and a plumber can tell "
         "you where yours stands."),
    ],
),

]

# ----------------------------------------------------------------- lookups ---
BY_SLUG = {c["slug"]: c for c in CITIES}

COUNTY_ORDER = [
    "Monterey County",
    "Santa Cruz County",
    "San Benito County",
    "Santa Clara County",
    "San Luis Obispo County",
    "Santa Barbara County",
]


def cities_by_county():
    out = {c: [] for c in COUNTY_ORDER}
    for c in CITIES:
        out.setdefault(c["county"], []).append(c)
    return out


def neighbors(slug, n=4):
    """Covered cities that this page lists as nearby, used for footer cross-links."""
    c = BY_SLUG[slug]
    names = {x.lower() for x in c["nearby"]}
    hits = []
    for other in CITIES:
        if other["slug"] == slug:
            continue
        if other["name"].lower() in names:
            hits.append(other)
    # pad with same-county, then nearest-listed-order cities so small pages
    # still get useful cross-links
    if len(hits) < n:
        for other in CITIES:
            if other["slug"] == slug or other in hits:
                continue
            if other["county"] == c["county"]:
                hits.append(other)
    if len(hits) < n:
        for other in CITIES:
            if other["slug"] != slug and other not in hits:
                hits.append(other)
    return hits[:n]
