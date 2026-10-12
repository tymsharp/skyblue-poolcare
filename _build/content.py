"""Content for skyblue-poolcare.com.

Business facts come from Skyblue's current site (skyblue-poolcare.com and
go.skyblue-poolcare.com, read 2026-10-11). Anything wrapped in FILL(...)
renders as a yellow placeholder and needs Zach to confirm before launch.

City pages: 13 real city pages. All 74 service-area zips are folded into
them as "areas we serve" (see ZIP list per city). No per-zip pages, on
purpose: dozens of near-identical location pages read as doorway pages.
"""


def FILL(text):
    return f'<span class="fill">{text}</span>'


BIZ = {
    "name": "SkyBlue Pool Care",
    "legal": "SkyBlue Pool Care",
    "owner": "Zach",
    # Main site uses (310) 421-8863; the GHL landing page uses (213) 668-6131.
    # Pick ONE before launch and use it on the Google Business Profile too.
    "phone": "(310) 421-8863",
    "phone_e164": "+13104218863",
    "email": "zach@skyblue-poolcare.com",
    "hours": "Mon to Sat, 7:00 AM to 5:00 PM",  # FILL: confirm
    "region": "San Fernando Valley & Westside Los Angeles",
    "domain": "https://skyblue-poolcare.com",
    "experience": "35+ years",  # "over 35 years" combined, per current site
    "license": FILL("License / insurance details"),
    "price_from": FILL("$XXX"),  # weekly service starting price per month
}

SERVICES = [
    {
        "slug": "weekly",
        "name": "Weekly Pool Service",
        "short": "Same day every week. Brush, skim, vacuum, balance, photo report.",
        "body": "Your tech comes the same day each week, cleans the pool top to bottom and balances the water. You get a photo and a full pool report after every visit.",
        "points": ["Brush walls, steps and tile line", "Skim, vacuum, empty baskets", "Test and balance chemicals", "Photo report after every visit"],
        "href": "weekly-pool-service.html",
    },
    {
        "slug": "filter",
        "name": "Filter Cleaning",
        "short": "Cartridge and DE filter cleans that bring pressure back down.",
        "body": "A dirty filter makes the pump work harder and the water go cloudy. We break it down, clean it and check pressure before and after.",
        "points": ["Cartridge and DE filters", "Pressure check before and after", "Less strain on the pump"],
    },
    {
        "slug": "green",
        "name": "Green-to-Blue Cleanup",
        "short": "Green or cloudy pool back to clear, then weekly care if you want it.",
        "body": "Vacant rental, missed weeks, or a pool you just bought. We bring it back to clear and balanced, then you decide on weekly service.",
        "points": ["Algae treatment and brushing", "Filter clean included", "Move-in and listing prep"],
    },
    {
        "slug": "repair",
        "name": "Equipment Repair",
        "short": "Pumps, filters, valves and leaks, diagnosed in plain terms.",
        "body": "When a pump won't prime, a valve sticks or the water level keeps dropping, we find the cause and tell you what it costs before work starts.",
        "points": ["Pumps, motors and valves", "Filters, plumbing and leaks", "Clear quote before any work"],
    },
    {
        "slug": "salt",
        "name": "Salt Cell Service",
        "short": "Salt cell cleaning, output checks and replacement when it quits.",
        "body": "A salt system still needs care. LA's hard water scales the cell, and a scaled cell stops making chlorine. We clean the cell, check salt level and output, and replace it when it reaches end of life.",
        "points": ["Cell cleaning and scale removal", "Salt level and output check", "Cell replacement, any major brand"],
    },
    {
        "slug": "automation",
        "name": "Pool Automation",
        "short": "Run the pump, heater and lights from your phone.",
        "body": "Pentair, Jandy and Hayward automation, installed and programmed. We set schedules that fit your pool and your power rates, and fix systems that stopped talking to the app.",
        "points": ["Pentair, Jandy and Hayward systems", "Schedules for pump, heater and lights", "App setup and troubleshooting"],
    },
    {
        "slug": "heater",
        "name": "Heater Repair & Install",
        "short": "Gas heaters and heat pumps that won't light, or need replacing.",
        "body": "A heater that won't light or shuts off early usually comes down to a few parts. We diagnose gas heaters and heat pumps, fix what's worth fixing and tell you straight when it's time to replace.",
        "points": ["Gas heaters and heat pumps", "Won't light, short cycles, error codes", "New heater sizing and install"],
    },
    {
        "slug": "tile",
        "name": "Tile Cleaning",
        "short": "Calcium line off the waterline tile, without harsh acid.",
        "body": "The white crust on your waterline tile is calcium from LA's hard water. We remove it with bead blasting or pumice, depending on the tile, so the tile line looks like it did when the pool was built.",
        "points": ["Calcium scale off the waterline", "Bead blasting or pumice, matched to the tile", "Spa and raised wall tile too"],
    },
    {
        "slug": "drain",
        "name": "Drains & Acid Washes",
        "short": "Drain and refill, or acid wash stained plaster.",
        "body": "High calcium, stains or water that won't balance sometimes needs a fresh start. We drain, clean or acid wash, and refill with a proper start-up.",
        "points": ["Full drain and refill", "Acid wash for stained plaster", "Start-up chemistry after refill"],
    },
]

PROMISES = [
    ("Photo report", "after every visit"),
    ("No skipped", "cleanings guarantee"),
    ("21-point", "inspection after your first service"),
    ("No contract", "cancel any time"),
]

TESTIMONIALS = [
    ("They clean our pool on a regular basis and are always timely. They send a photo and list of work after each clean.", "Daisy S."),
    ("Fantastic company to deal with. From day 1 signing up with them they've taken great care of my pool.", "Steven W."),
]

FAQ = [
    ("How much is weekly pool service?",
     f"Weekly service starts at {BIZ['price_from']} a month. The exact price depends on pool size, spa, trees and equipment. Send the quote form and we'll give you a firm number."),
    ("What happens on a weekly visit?",
     "We brush the walls, steps and tile line, skim, vacuum, empty the skimmer and pump baskets, check the equipment, and test and balance the water. Then we send a photo and a full pool report."),
    ("Do I have to sign a contract?",
     "No. Service is month to month. If you're not happy, you can stop any time."),
    ("What if you miss a week?",
     "We don't. SkyBlue has a no skipped cleanings guarantee. If weather or a holiday moves your day, we tell you and make it up."),
    ("How do I get started?",
     "Send the quote form or call. We quote over the phone, a service manager does a full first cleaning, and after your first scheduled service we do a free 21-point inspection of the pool and equipment."),
    ("Do you service salt water pools?",
     "Yes. We check salt levels and keep the salt cell clean so it lasts."),
]

# 13 city pages. zips = every service-area zip folded into this page.
# local = things that are true about pools in this area; faq = local questions.
CITIES = [
    # ---------------- San Fernando Valley
    {
        "slug": "calabasas", "name": "Calabasas & West Hills", "short": "Calabasas", "region": "valley",
        "zips": ["91302", "91307", "91304", "91303"],
        "hoods": ["Calabasas", "Hidden Hills", "West Hills", "Bell Canyon", "Canoga Park"],
        "intro": "Calabasas, Hidden Hills and West Hills sit at the west end of the Valley against the Santa Monica Mountains and the Simi Hills. Lots are big, many pools have an attached spa, and a lot of homes are behind a gate.",
        "local": [
            ("Gated communities and access", "Hidden Hills, Bell Canyon and many Calabasas communities are gated. We keep your gate code or guard-list name on file so your tech gets in on the same day every week."),
            ("Oak leaves and hillside debris", "Coast live oaks and hillside brush drop leaves and seed pods all year, and more on wind days. Skimmer and pump baskets fill fast here, so we empty both on every visit."),
            ("Inland heat", "The west Valley runs some of the hottest summer days in Los Angeles County. Chlorine burns off faster in that heat, so we test every week instead of guessing."),
        ],
        "faq": [
            ("Can you service pools in gated Hidden Hills or Bell Canyon?", "Yes. Give us your gate code or have us added to the guard list, and the same tech comes the same day every week."),
            ("Do you clean the spa too?", "Yes. An attached spa is cleaned and balanced with the pool on every visit."),
        ],
    },
    {
        "slug": "woodland-hills", "name": "Woodland Hills", "short": "Woodland Hills", "region": "valley",
        "zips": ["91364", "91367", "91306", "91335"],
        "hoods": ["Woodland Hills", "Warner Center", "Winnetka", "Reseda"],
        "intro": "Woodland Hills holds the Los Angeles County heat record: 121°F on September 6, 2020. South of Ventura Boulevard the lots climb into the hills. North of it, Winnetka and Reseda are flat streets of single-story homes with backyard pools.",
        "local": [
            ("Built for heat", "On 100-degree weeks chlorine can be gone in a day or two and algae follows. Weekly testing and the right stabilizer level keep the water from flipping green between visits."),
            ("Hillside lots south of Ventura", "Homes off Topanga Canyon, Mulholland and the streets above Ventura Boulevard often have steep side yards and equipment pads below the pool. We plan the route for it."),
            ("Pumps that run all summer", "Long run times in summer wear out pumps. If yours is an older single-speed pump, we'll tell you what a variable-speed upgrade would save."),
        ],
        "faq": [
            ("Do you cover Winnetka and Reseda?", "Yes. Our Woodland Hills routes also cover Winnetka (91306) and Reseda (91335)."),
            ("My pool turns green every August. Why?", "Heat burns off chlorine fast. Weekly testing, the right stabilizer level and a clean filter usually stop it."),
        ],
    },
    {
        "slug": "encino", "name": "Encino & Tarzana", "short": "Encino", "region": "valley",
        "zips": ["91316", "91436", "91356", "91406"],
        "hoods": ["Encino", "Encino Hills", "Tarzana", "Lake Balboa"],
        "intro": "Encino and Tarzana run along Ventura Boulevard, with hillside homes to the south and flatter streets to the north down to Lake Balboa. Tarzana is named after Tarzan, whose author Edgar Rice Burroughs owned the ranch the neighborhood was built on.",
        "local": [
            ("Mature trees", "Older Encino lots have big oaks, sycamores and pines. They shade the pool, which helps, and drop leaves and needles, which doesn't. We empty baskets every visit and brush the tile line where debris collects."),
            ("Hillside access in 91436", "Pools in the Encino hills often sit on terraces with stairs down to the equipment. Your tech knows the property before the first visit."),
            ("Older equipment", "Many Encino pools were built decades ago and still run original plumbing or older heaters. Our 21-point inspection after your first service shows what's worn before it fails."),
        ],
        "faq": [
            ("Do you cover the Encino hills south of Ventura?", "Yes. 91436 is on our Encino route, including hillside homes with stairs down to the equipment."),
            ("Is Tarzana on the same route as Encino?", "Yes. Tarzana (91356) and Lake Balboa (91406) are served from our Encino routes."),
        ],
    },
    {
        "slug": "sherman-oaks", "name": "Sherman Oaks & Van Nuys", "short": "Sherman Oaks", "region": "valley",
        "zips": ["91403", "91423", "91401", "91405", "91411", "91402"],
        "hoods": ["Sherman Oaks", "Van Nuys", "Valley Glen", "Panorama City"],
        "intro": "Sherman Oaks south of Ventura Boulevard climbs into the hills toward Mulholland. North of the boulevard, and on into Van Nuys and Valley Glen, the streets are flat and almost every block has backyard pools.",
        "local": [
            ("Hard water", "Los Angeles tap water is hard, so refills add calcium every week of summer. Left alone it shows up as white scale on the tile. We track calcium and keep the water balanced so scale doesn't build."),
            ("Hillside homes in 91403", "Streets off Beverly Glen, Valley Vista and Woodcliff are steep and narrow. Pools there often sit above or below the house. We plan access before the first visit."),
            ("Smaller backyard pools", "Many Van Nuys and Valley Glen homes have compact pools. They heat up and lose chlorine faster than big ones, so weekly balancing matters even more."),
        ],
        "faq": [
            ("Do you cover both Sherman Oaks zip codes?", "Yes. 91403 south of Ventura and 91423 north and east are both on our Sherman Oaks route."),
            ("What's the white crust on my tile?", "Calcium scale from hard water. We keep calcium in range to slow it down, and can clean existing scale."),
        ],
    },
    {
        "slug": "studio-city", "name": "Studio City & Toluca Lake", "short": "Studio City", "region": "valley",
        "zips": ["91604", "91602", "91607", "91608", "91601", "91605", "91606"],
        "hoods": ["Studio City", "Toluca Lake", "Valley Village", "Universal City", "North Hollywood"],
        "intro": "Studio City takes its name from the film studio lot on Radford Avenue, now CBS Studio Center. Homes run from the hills off Laurel Canyon and Coldwater Canyon down to the flat streets of Valley Village, Toluca Lake and North Hollywood.",
        "local": [
            ("Hillside pools", "Pools in the Studio City hills are often tucked into small, steep lots with tight side yards. Your tech knows the access before the first visit."),
            ("Tree cover", "Toluca Lake and the older parts of Studio City have mature shade trees. Leaves are the main fight here, so baskets get emptied every visit."),
            ("Flat-lot pools in North Hollywood", "North Hollywood and Valley Village pools get full sun most of the day, so chlorine and stabilizer are checked every week."),
        ],
        "faq": [
            ("Do you cover North Hollywood?", "Yes. North Hollywood (91601, 91605, 91606), Valley Village (91607) and Universal City (91608) are on our Studio City routes."),
            ("Can you get to a pool on a steep hillside lot?", "Yes. Tell us about access when you request a quote and we'll plan for it."),
        ],
    },
    {
        "slug": "northridge", "name": "Northridge & Granada Hills", "short": "Northridge", "region": "valley",
        "zips": ["91324", "91325", "91326", "91311", "91344", "91343", "91345", "91340", "91342", "91331"],
        "hoods": ["Northridge", "Granada Hills", "Porter Ranch", "Chatsworth", "North Hills", "Mission Hills", "San Fernando", "Sylmar", "Pacoima", "Arleta"],
        "intro": "The north Valley is ranch-style homes and big flat lots, from Northridge and Granada Hills to the newer hillside tracts of Porter Ranch. Granada Hills has Balboa Highlands, one of the Valley's Eichler neighborhoods, with pools built into the original mid-century design.",
        "local": [
            ("Big lots, bigger pools", "North Valley lots are large and so are many pools. Bigger pools take more chemical, so we size every treatment to your pool's volume."),
            ("Porter Ranch HOAs", "Many Porter Ranch communities have HOA rules for service vehicles and gate access. We work within them."),
            ("Wind off the mountains", "Santa Ana winds come through the north Valley passes and fill pools with leaves and dust. After a wind event we brush and vacuum, and the filter gets checked."),
        ],
        "faq": [
            ("Do you cover Chatsworth and Granada Hills?", "Yes. Chatsworth (91311), Granada Hills (91344), North Hills, Mission Hills, San Fernando, Sylmar, Pacoima and Arleta are all on our north Valley routes."),
            ("Can you work with my Porter Ranch HOA?", "Yes. Tell us the gate and vehicle rules and we'll follow them."),
        ],
    },
    {
        "slug": "burbank", "name": "Burbank", "short": "Burbank", "region": "valley",
        "zips": ["91501", "91502", "91504", "91505", "91506", "91352", "91040", "91042"],
        "hoods": ["Burbank", "Rancho District", "Magnolia Park", "Burbank Hills", "Sun Valley", "Sunland", "Tujunga"],
        "intro": "Burbank runs its own water utility, Burbank Water and Power, separate from Los Angeles. Pools range from the Burbank hillside homes above Glenoaks to the horse-zoned Rancho District near Griffith Park, and on to the foothills of Sunland and Tujunga.",
        "local": [
            ("Your water, not LA's", "Burbank tap water comes from Burbank Water and Power. Every refill changes your pool's balance, so we test calcium and alkalinity every visit rather than assuming."),
            ("Rancho District", "Rancho homes back onto the Los Angeles River equestrian trails. Dust and debris are part of life here, so baskets and filters get extra attention."),
            ("Foothill pools in Sunland-Tujunga", "Homes against the San Gabriel foothills get more wind, ash on fire days and wildlife. We check for damage and clean up after wind events."),
        ],
        "faq": [
            ("Do you cover Sunland and Tujunga?", "Yes. Sunland (91040), Tujunga (91042) and Sun Valley (91352) are on our Burbank routes."),
            ("Do you service the Rancho District?", "Yes. 91505 and 91506 are both on our Burbank routes."),
        ],
    },
    # ---------------- Westside and Hollywood
    {
        "slug": "hollywood-hills", "name": "Hollywood Hills & Los Feliz", "short": "Hollywood Hills", "region": "westside",
        "zips": ["90046", "90068", "90027", "90028", "90038"],
        "hoods": ["Hollywood Hills", "Laurel Canyon", "Hollywood Dell", "Lake Hollywood", "Los Feliz", "Hollywood"],
        "intro": "In the Hollywood Hills the streets are narrow, steep and winding, and the pool is often on a terrace above or below the house. Laurel Canyon, the Hollywood Dell and the hills around Lake Hollywood are some of the hardest pools in LA to get to, and some of the best views.",
        "local": [
            ("Access is the job", "Street parking is tight and equipment pads are often down a flight of stairs. We plan each stop before the first visit so your day never gets skipped."),
            ("Infinity and vanishing-edge pools", "View pools with a spillover edge have a catch basin and extra plumbing. We clean and balance both bodies of water."),
            ("Canyon debris", "Laurel Canyon and the Dell have heavy tree cover. Leaves and needles are the weekly fight, plus ash and dust on fire-weather days."),
        ],
        "faq": [
            ("Can you service a pool I can only reach by stairs?", "Yes. Most Hollywood Hills pools are like that. Let us know about access when you request a quote."),
            ("Do you service infinity-edge pools?", "Yes. We clean and balance the pool and the catch basin, and check the overflow equipment."),
        ],
    },
    {
        "slug": "west-hollywood", "name": "West Hollywood", "short": "West Hollywood", "region": "westside",
        "zips": ["90069", "90048", "90036"],
        "hoods": ["West Hollywood", "Sunset Strip", "Bird Streets", "Beverly Grove", "Fairfax"],
        "intro": "West Hollywood is its own city, about two square miles between Beverly Hills and Hollywood. Above Sunset, the Bird Streets are hillside homes with view pools. Below it, Beverly Grove and Fairfax have compact backyards, plunge pools and spas.",
        "local": [
            ("Small pools and spas", "Plunge pools and spas hold far less water than a full pool, so the chemistry swings faster. We balance them carefully every visit."),
            ("Bird Streets and hillside homes", "Homes above the Sunset Strip have steep drives and limited parking. Your tech knows the access before the first visit."),
            ("Short-term rentals", "Rental and guest homes need the pool ready every week. Your photo report shows it's clean before guests arrive."),
        ],
        "faq": [
            ("Do you service plunge pools and spas only?", "Yes. Spa-only and plunge pool service is available. Ask for a quote."),
            ("Do you cover Beverly Grove and Fairfax?", "Yes. 90048 and 90036 are on our West Hollywood route."),
        ],
    },
    {
        "slug": "beverly-hills", "name": "Beverly Hills & Bel Air", "short": "Beverly Hills", "region": "westside",
        "zips": ["90210", "90211", "90212", "90077", "90067", "90035"],
        "hoods": ["Beverly Hills", "Beverly Hills Post Office", "Bel Air", "Century City", "Beverlywood", "Pico-Robertson"],
        "intro": "Beverly Hills north of Sunset and Bel Air are estate properties, often with a pool, a spa and water features on one property, and staff, gates and cameras at the door. South of Wilshire, Beverlywood and Pico-Robertson are family homes with backyard pools.",
        "local": [
            ("Multiple bodies of water", "Estate properties often have a pool, a spa and fountains or ponds. Each one is cleaned, balanced and listed on your photo report."),
            ("Gates and staff", "We coordinate with your house manager or staff on access and keep gate codes on file."),
            ("Equipment rooms", "Larger properties run automation, heaters and multiple pumps. Our 21-point inspection covers the full equipment room after your first service."),
        ],
        "faq": [
            ("Do you coordinate with house managers?", "Yes. We can send the weekly photo report to you and your house manager."),
            ("Do you cover Century City and Beverlywood?", "Yes. 90067 and 90035 are on our Beverly Hills route."),
        ],
    },
    {
        "slug": "brentwood", "name": "Brentwood & Pacific Palisades", "short": "Brentwood", "region": "westside",
        "zips": ["90049", "90272", "90024", "90025", "90064"],
        "hoods": ["Brentwood", "Pacific Palisades", "Westwood", "Holmby Hills", "West LA", "Cheviot Hills", "Rancho Park"],
        "intro": "Brentwood runs from San Vicente Boulevard up into Mandeville and Sullivan canyons. Pacific Palisades is rebuilding after the January 2025 Palisades Fire, and many of those homes are getting new pools and new equipment.",
        "local": [
            ("New pools in the Palisades", "A new or rebuilt pool needs a proper start-up: careful chemistry for the first weeks while fresh plaster cures. We do start-ups and then take over weekly service."),
            ("Canyon homes", "Mandeville and Sullivan canyon homes have big trees and narrow access roads. Your tech knows the route."),
            ("Coastal air", "Closer to the ocean, the marine layer slows evaporation, but salt air is hard on metal equipment. We check heaters, pumps and fittings for corrosion."),
        ],
        "faq": [
            ("Do you do start-ups for new or rebuilt pools?", "Yes. We handle the start-up chemistry for new plaster and then move you to weekly service."),
            ("Do you cover Westwood and Cheviot Hills?", "Yes. Westwood (90024), West LA (90025) and Cheviot Hills (90064) are on our Brentwood route."),
        ],
    },
    {
        "slug": "santa-monica", "name": "Santa Monica & Venice", "short": "Santa Monica", "region": "westside",
        "zips": ["90401", "90402", "90403", "90404", "90405", "90291", "90292"],
        "hoods": ["Santa Monica", "North of Montana", "Ocean Park", "Sunset Park", "Venice", "Marina del Rey"],
        "intro": "Santa Monica pools live in ocean air. The marine layer keeps mornings cool and evaporation low, but salt air is hard on heaters, pumps and metal fittings. North of Montana has the larger lots; Ocean Park, Sunset Park and Venice have compact yards and spas.",
        "local": [
            ("Corrosion checks", "Salt air corrodes heater parts, pump motors and metal fittings faster here than in the Valley. We look for it every visit."),
            ("Cooler water, slower algae", "Cooler coastal water is easier to keep clear, but it's not immune. Weekly testing catches problems early."),
            ("Compact yards in Venice", "Many Venice and Ocean Park homes have small pools or spas squeezed into tight yards. We service those too."),
        ],
        "faq": [
            ("Do you cover Venice and Marina del Rey?", "Yes. Venice (90291) and Marina del Rey (90292) are on our Santa Monica route."),
            ("Why does my heater keep breaking near the beach?", "Salt air corrodes heater parts. We check for corrosion and tell you what's worn before it fails."),
        ],
    },
    {
        "slug": "culver-city", "name": "Culver City & Mar Vista", "short": "Culver City", "region": "westside",
        "zips": ["90230", "90232", "90034", "90066", "90094"],
        "hoods": ["Culver City", "Fox Hills", "Palms", "Mar Vista", "Playa Vista"],
        "intro": "Culver City is its own city, home to Sony Pictures Studios. Mar Vista has the Mar Vista Tract, a mid-century modern neighborhood designed by architect Gregory Ain. Playa Vista is newer construction near the Ballona Wetlands.",
        "local": [
            ("Mid-century pools", "Older pools in Mar Vista and Palms often run original plumbing and older equipment. Our 21-point inspection shows what's worn."),
            ("Newer builds in Playa Vista", "Newer homes and condos often have salt systems and variable-speed pumps. We keep salt cells clean and settings right."),
            ("West-side marine air", "Mornings are cool and damp near the coast, which is easy on water but hard on metal. We check equipment for corrosion."),
        ],
        "faq": [
            ("Do you cover Palms and Playa Vista?", "Yes. Palms (90034), Mar Vista (90066) and Playa Vista (90094) are on our Culver City route."),
            ("Do you service salt water pools?", "Yes. We check salt levels and clean the salt cell."),
        ],
    },
]

ZIP_HOODS = {}  # filled by build.py from data/service-area-zips.csv


# Blog posts. body = list of (tag, html) blocks; tag is p, h2, h3 or ul (list of items).
# Keep claims general and true; anything Skyblue-specific that needs Zach goes in FILL().
POSTS = [
    {
        "slug": "weekly-pool-service-cost-los-angeles",
        "title": "How Much Does Weekly Pool Service Cost in Los Angeles?",
        "desc": "What drives the monthly price of weekly pool service in the San Fernando Valley and Westside, and what should be included.",
        "date": "2026-10-12", "date_h": "October 12, 2026", "read": "4 min read", "tag": "Pricing",
        "body": [
            ("p", "Most Los Angeles pool companies charge a flat monthly price for weekly service. The number you're quoted depends on a handful of things you can check before you call."),
            ("h2", "What changes the price"),
            ("ul", ["<strong>Pool size.</strong> More water takes more chemical and more time to brush and vacuum.",
                    "<strong>A spa.</strong> An attached spa is a second body of water to clean and balance.",
                    "<strong>Trees and debris.</strong> Oaks in Encino or canyon brush in Laurel Canyon fill baskets fast and add time to every stop.",
                    "<strong>Access.</strong> A hillside pool down a flight of stairs takes longer than a flat backyard.",
                    "<strong>Chemicals included or extra.</strong> Some companies include chemicals, some bill them separately. Ask."]),
            ("h2", "What weekly service should include"),
            ("p", "At minimum: brushing walls, steps and the tile line, skimming, vacuuming, emptying the skimmer and pump baskets, testing and balancing the water, and a look at the pump, filter and heater. Filter cleans are usually extra and done a few times a year."),
            ("p", "Ask for proof of each visit. SkyBlue sends a photo and a full pool report after every cleaning, so you never have to wonder whether the tech came."),
            ("h2", "What SkyBlue charges"),
            ("p", f"Weekly service starts at {BIZ['price_from']} a month, month to month with no contract. Send the quote form with your address and we'll give you a firm number."),
        ],
    },
    {
        "slug": "hard-water-calcium-scale-la-pools",
        "title": "Hard Water and Calcium Scale in LA Pools",
        "desc": "Why a white crust shows up on the tile line, what calcium hardness level to hold, and when a drain and refill makes sense.",
        "date": "2026-10-12", "date_h": "October 12, 2026", "read": "4 min read", "tag": "Water care",
        "body": [
            ("p", "Southern California tap water is hard, meaning it carries a lot of dissolved calcium. Every time your pool tops itself off after a hot week, it adds more. Water evaporates; the calcium stays."),
            ("h2", "What scale looks like"),
            ("p", "A white or gray crust along the tile line, rough spots on plaster, and white flakes in the water. Scale also builds inside heaters and on salt cells, where you can't see it but it shortens their life."),
            ("h2", "The level to hold"),
            ("p", "Most pool pros aim for calcium hardness between about 200 and 400 parts per million. Scale forms faster when calcium is high and pH and alkalinity drift up at the same time, so the three have to be managed together. That's why we test every week instead of guessing."),
            ("h2", "Burbank vs Los Angeles water"),
            ("p", "Burbank homes get water from Burbank Water and Power, not LADWP. The supply is different, so the pool's balance drifts differently. See our <a href=\"pool-service-burbank.html\">Burbank pool service page</a>."),
            ("h2", "When to drain and refill"),
            ("p", "When calcium climbs so high that the water won't stay balanced, a partial or full drain and refill resets it. Acid washing removes stains and scale from older plaster at the same time. Drains are best done in cooler months, not in a September heat wave."),
        ],
    },
    {
        "slug": "green-pool-heat-wave-san-fernando-valley",
        "title": "Why Pools Turn Green in a San Fernando Valley Heat Wave",
        "desc": "Valley heat burns off chlorine fast. Here's why pools flip green in a few days and how weekly service prevents it.",
        "date": "2026-10-12", "date_h": "October 12, 2026", "read": "4 min read", "tag": "Seasonal",
        "body": [
            ("p", "The San Fernando Valley gets some of the hottest days in Los Angeles County. Woodland Hills set the county record at 121°F on September 6, 2020. Pools feel it."),
            ("h2", "What heat does to your water"),
            ("ul", ["Sunlight breaks chlorine down. Without stabilizer, most of it can be gone in an afternoon.",
                    "Warm water grows algae faster.",
                    "More swimmers add more sunscreen, sweat and debris that use up chlorine.",
                    "Evaporation means more top-off water, which shifts the balance."]),
            ("h2", "How to keep it clear"),
            ("ul", ["Hold stabilizer (cyanuric acid) in range so chlorine survives the sun.",
                    "Test and adjust every week, not every few weeks.",
                    "Keep the filter clean so it can catch what the chlorine kills.",
                    "Run the pump long enough on hot weeks to turn the water over."]),
            ("h2", "If it's already green"),
            ("p", "Our green-to-blue cleanup brings it back with algae treatment, brushing and a filter clean. Then weekly service keeps it there. Serving <a href=\"pool-service-woodland-hills.html\">Woodland Hills</a>, <a href=\"pool-service-encino.html\">Encino</a>, <a href=\"pool-service-northridge.html\">Northridge</a> and the rest of the Valley."),
        ],
    },
    {
        "slug": "winter-pool-service-los-angeles",
        "title": "Do You Need Weekly Pool Service in an LA Winter?",
        "desc": "Algae slows down when the water cools, but leaves, wind and rain don't. What changes in winter and what doesn't.",
        "date": "2026-10-12", "date_h": "October 12, 2026", "read": "3 min read", "tag": "Seasonal",
        "body": [
            ("p", "Los Angeles pools stay open all year. Water cools down in winter and algae grows more slowly, so some owners wonder if weekly service can wait until spring."),
            ("h2", "What still happens in winter"),
            ("ul", ["<strong>Santa Ana winds</strong> fill pools with leaves and dust, mostly from fall through winter.",
                    "<strong>Rain</strong> dilutes the water and washes in dirt, which throws off the balance.",
                    "<strong>Leaf drop</strong> from sycamores and other deciduous trees clogs baskets and stains plaster.",
                    "<strong>Equipment</strong> still runs and still breaks. Freeze-protection settings and heaters need checking."]),
            ("h2", "What changes"),
            ("p", "Pumps can usually run fewer hours, and chemical use drops. The weekly visit becomes more about debris and equipment, less about chlorine."),
            ("h2", "The cost of skipping"),
            ("p", "A pool left alone for a month or two can turn green, stain, or hide an equipment problem until spring. Getting it back costs more than the weeks you skipped. Weekly service is month to month with no contract."),
        ],
    },
]
