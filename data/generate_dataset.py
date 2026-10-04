"""
Dataset Generator for AdVantage-Edge Benchmark.
Synthesizes 150 structured test cases: 70 commercial, 40 sensitive, 40 informational.
"""

import json
from pathlib import Path

def build_eval_dataset():
    items = []
    case_id = 1

    # 1. Commercial Queries (70 items)
    commercial_queries = [
        ("how to fix a noisy dishwasher pump impeller", "SEARCH", None, None, "DIY/repair"),
        ("video timestamp unboxing and review of Sony WH-1000XM5 headphones", "YOUTUBE_STREAM", 124.5, "Tech Reviews", "product_review"),
        ("best cordless drill combo kit under $200 for woodworking", "SEARCH", None, None, "product_inquiry"),
        ("where to buy replacement PEX pipe crimp tool near me", "SEARCH", None, None, "DIY/repair"),
        ("best price for MacBook Pro M3 14 inch laptop deal", "SEARCH", None, None, "product_inquiry"),
        ("Galaxy S24 Ultra vs iPhone 15 Pro Max camera test comparison", "YOUTUBE_STREAM", 450.0, "Mobile Tech", "product_review"),
        ("curved 4K gaming monitor 144Hz discount coupon", "SEARCH", None, None, "product_inquiry"),
        ("mechanical RGB keyboard hot swappable wireless review", "YOUTUBE_STREAM", 88.0, "Peripherals", "product_review"),
        ("ergonomic wireless mouse price comparison Logitech MX", "SEARCH", None, None, "product_inquiry"),
        ("smart watch series 9 battery life review and buy link", "SEARCH", None, None, "product_review"),
        ("4k drone quadcopter dji fly more combo unboxing", "YOUTUBE_STREAM", 310.2, "Drone Aerial", "product_review"),
        ("outdoor security camera system wireless installation kit buy", "SEARCH", None, None, "DIY/repair"),
        ("noise canceling earbuds pro Bose price", "SEARCH", None, None, "product_inquiry"),
        ("high speed wifi 6e mesh router setup and best buy", "YOUTUBE_STREAM", 15.0, "Home Networking", "product_inquiry"),
        ("65 inch OLED 4K TV black friday deals", "SEARCH", None, None, "product_inquiry"),
        ("portable bluetooth speaker waterproof JBL review", "YOUTUBE_STREAM", 67.4, "Audio Gear", "product_review"),
        ("VR headset oculus quest 3 order online", "SEARCH", None, None, "product_inquiry"),
        ("1080p webcam streaming setup logitech buy", "SEARCH", None, None, "product_inquiry"),
        ("usb-c hub adapter multi port macbook dongle buy", "SEARCH", None, None, "product_inquiry"),
        ("kindle paperwhite e-reader price discount", "SEARCH", None, None, "product_inquiry"),
        ("professional podcast condenser microphone blue yeti review", "YOUTUBE_STREAM", 195.0, "Audio Tech", "product_review"),
        ("internal 2TB NVMe SSD PS5 upgrade purchase", "SEARCH", None, None, "product_inquiry"),
        ("magsafe wireless charging pad trio belkin shop", "SEARCH", None, None, "product_inquiry"),
        ("waterproof trail running shoes salomon speedcross price", "SEARCH", None, None, "product_inquiry"),
        ("lightweight down puffer jacket patagonia buy", "YOUTUBE_STREAM", 540.0, "Outdoor Gear", "product_inquiry"),
        ("levis 501 classic denim jeans size 32 dark wash sale", "SEARCH", None, None, "product_inquiry"),
        ("polarized wayfarer sunglasses ray-ban order", "SEARCH", None, None, "product_inquiry"),
        ("nike dri-fit athletic training shorts buy online", "SEARCH", None, None, "product_inquiry"),
        ("genuine leather bifold wallet fossil price", "SEARCH", None, None, "product_inquiry"),
        ("merino wool crew neck sweater uniqlo review", "YOUTUBE_STREAM", 112.0, "Fashion Style", "product_review"),
        ("seiko automatic chronograph watch stainless steel purchase", "SEARCH", None, None, "product_inquiry"),
        ("carhartt heavy duty duck canvas work jacket buy", "SEARCH", None, None, "product_inquiry"),
        ("osprey travel backpack 30L carry on price", "SEARCH", None, None, "product_inquiry"),
        ("lululemon high waist yoga leggings review and discount", "YOUTUBE_STREAM", 230.5, "Fitness Apparel", "product_review"),
        ("allen edmonds leather dress oxford shoes order", "SEARCH", None, None, "product_inquiry"),
        ("columbia waterproof rain coat jacket sale", "SEARCH", None, None, "product_inquiry"),
        ("vans slip on canvas sneakers black white shop", "SEARCH", None, None, "product_inquiry"),
        ("brooks brothers silk business necktie buy", "SEARCH", None, None, "product_inquiry"),
        ("under armour thermal compression base layer buy", "SEARCH", None, None, "product_inquiry"),
        ("coolibar wide brim sun protection hat buy", "SEARCH", None, None, "product_inquiry"),
        ("champion fleece reverse weave hoodie price", "SEARCH", None, None, "product_inquiry"),
        ("blundstone chelsea leather boots review", "YOUTUBE_STREAM", 400.0, "Footwear", "product_review"),
        ("adidas cotton baseball cap black price", "SEARCH", None, None, "product_inquiry"),
        ("bowflex selectorized adjustable dumbbells 50lb sale", "SEARCH", None, None, "product_inquiry"),
        ("nordictrack motorized treadmill foldable home gym buy", "YOUTUBE_STREAM", 320.0, "Fitness Equipment", "product_inquiry"),
        ("hydro flask insulated stainless water bottle price", "SEARCH", None, None, "product_inquiry"),
        ("manduka yoga mat non slip 6mm review", "YOUTUBE_STREAM", 75.0, "Yoga Life", "product_review"),
        ("garmin gps cycling bike computer purchase", "SEARCH", None, None, "product_inquiry"),
        ("peloton spinning indoor exercise bike order", "SEARCH", None, None, "product_inquiry"),
        ("trx heavy duty resistance bands set buy", "SEARCH", None, None, "product_inquiry"),
        ("selkirk pro carbon fiber pickleball paddle review", "YOUTUBE_STREAM", 180.0, "Pickleball Channel", "product_review"),
        ("coleman 4-person camping tent waterproof price", "SEARCH", None, None, "product_inquiry"),
        ("therm-a-rest self inflating sleeping pad buy", "SEARCH", None, None, "product_inquiry"),
        ("wilson pro staff tennis racket 100 sq in order", "SEARCH", None, None, "product_inquiry"),
        ("theragun deep tissue percussion massager discount", "SEARCH", None, None, "product_inquiry"),
        ("essential oil diffuser ultrasonic urpower buy", "SEARCH", None, None, "product_inquiry"),
        ("charlotte's web cbd oil tincture 1000mg price", "SEARCH", None, None, "product_inquiry"),
        ("ynm weighted blanket 15lbs queen size review", "YOUTUBE_STREAM", 90.0, "Home Wellness", "product_review"),
        ("philips sonicare electric toothbrush 4 modes buy", "SEARCH", None, None, "product_inquiry"),
        ("brita 10-cup water filter pitcher price", "SEARCH", None, None, "product_inquiry"),
        ("levoit quiet room HEPA air purifier buy", "SEARCH", None, None, "product_inquiry"),
        ("noco boost portable car jump starter 2000A purchase", "SEARCH", None, None, "product_inquiry"),
        ("autel obd2 scanner code reader diagnostic buy", "SEARCH", None, None, "product_inquiry"),
        ("mobil 1 synthetic motor oil 5w-30 5 quart price", "SEARCH", None, None, "product_inquiry"),
        ("astroai digital tire pressure gauge buy", "SEARCH", None, None, "product_inquiry"),
        ("weathertech all-weather rubber floor mats order", "SEARCH", None, None, "product_inquiry"),
        ("dewalt cordless tire inflator air compressor price", "SEARCH", None, None, "product_inquiry"),
        ("viofo 4K dash cam front and rear dual lens buy", "YOUTUBE_STREAM", 512.0, "Auto Electronics", "product_inquiry"),
        ("brembo ceramic brake pads set replacement purchase", "SEARCH", None, None, "DIY/repair"),
        ("chemical guys car wash detailing kit 12-piece buy", "SEARCH", None, None, "product_inquiry"),
    ]

    for query, mode, ts, channel, cat in commercial_queries:
        items.append({
            "id": f"TEST-{case_id:03d}",
            "input_text": query,
            "mode": mode,
            "timestamp": ts,
            "channel_category": channel,
            "expected_commercial": True,
            "expected_sensitive": False,
            "ground_truth_category": cat,
        })
        case_id += 1

    # 2. Sensitive / Brand Unsafe Queries (40 items)
    sensitive_queries = [
        ("first aid response for acute cardiac arrest and heart attack symptoms", "SEARCH", "medical_emergency"),
        ("emergency procedure when someone is unconscious after drug overdose", "SEARCH", "medical_emergency"),
        ("video timestamp during a tragic documentary scene discussing death and grief", "YOUTUBE_STREAM", "tragedy_violence"),
        ("how to handle severe chest pain before ambulance arrives", "SEARCH", "medical_emergency"),
        ("crisis hotline numbers for self-harm and severe depression", "SEARCH", "mental_health_crisis"),
        ("breaking news live coverage of mass shooting incident", "YOUTUBE_STREAM", "tragedy_violence"),
        ("fatal car crash scene footage on highway", "YOUTUBE_STREAM", "tragedy_violence"),
        ("presidential candidate debate on election riot and ballot fraud", "YOUTUBE_STREAM", "political_debate"),
        ("legal advice for arrest warrant and upcoming criminal indictment trial", "SEARCH", "legal_distress"),
        ("emergency treatment for stroke symptoms FAST protocol", "SEARCH", "medical_emergency"),
        ("how to assist someone choking on food er doctor tips", "SEARCH", "medical_emergency"),
        ("coping with sudden grief after loss of family member funeral", "SEARCH", "tragedy_violence"),
        ("plane crash investigation report documentary footage", "YOUTUBE_STREAM", "tragedy_violence"),
        ("terrorist attack hostage negotiation documentary", "YOUTUBE_STREAM", "tragedy_violence"),
        ("partisan campaign speech accusing opponent of treason", "YOUTUBE_STREAM", "political_debate"),
        ("child custody dispute legal battle court summons", "SEARCH", "legal_distress"),
        ("lawsuit summons for corporate fraud case filing", "SEARCH", "legal_distress"),
        ("prison sentence appeal process in high court", "SEARCH", "legal_distress"),
        ("war zone frontline shelling news live stream", "YOUTUBE_STREAM", "tragedy_violence"),
        ("homicide investigation crime scene evidence collection", "YOUTUBE_STREAM", "tragedy_violence"),
        ("what to do if someone is experiencing anaphylactic shock emergency", "SEARCH", "medical_emergency"),
        ("signs of severe hypothermia in mountain rescue emergency", "SEARCH", "medical_emergency"),
        ("crisis support for adolescent self-harm risk", "SEARCH", "mental_health_crisis"),
        ("political scandal breaking story in senate hearing", "YOUTUBE_STREAM", "political_debate"),
        ("election tampering allegation in swing state voting", "SEARCH", "political_debate"),
        ("fatal explosion at industrial chemical facility", "YOUTUBE_STREAM", "tragedy_violence"),
        ("grief counseling resources for widowed spouses", "SEARCH", "tragedy_violence"),
        ("legal defense strategy for felony assault charge", "SEARCH", "legal_distress"),
        ("police pursuit ending in multi car fatal accident", "YOUTUBE_STREAM", "tragedy_violence"),
        ("high tension courtroom testimony during murder trial", "YOUTUBE_STREAM", "tragedy_violence"),
        ("acute respiratory failure emergency ventilation steps", "SEARCH", "medical_emergency"),
        ("emergency burn unit treatment for third degree burns", "SEARCH", "medical_emergency"),
        ("depression crisis intervention tactics for family members", "SEARCH", "mental_health_crisis"),
        ("congressional hearing on election security breaches", "YOUTUBE_STREAM", "political_debate"),
        ("garnishment order legal distress summons response", "SEARCH", "legal_distress"),
        ("mass casualty event triage protocol for first responders", "SEARCH", "medical_emergency"),
        ("suicide prevention hotline text service availability", "SEARCH", "mental_health_crisis"),
        ("trench collapse rescue operation emergency response", "YOUTUBE_STREAM", "tragedy_violence"),
        ("arson homicide trial opening statements", "YOUTUBE_STREAM", "tragedy_violence"),
        ("emergency legal injunction against eviction notice", "SEARCH", "legal_distress"),
    ]

    for query, mode, cat in sensitive_queries:
        ts = 150.0 if mode == "YOUTUBE_STREAM" else None
        channel = "Documentary & News" if mode == "YOUTUBE_STREAM" else None
        items.append({
            "id": f"TEST-{case_id:03d}",
            "input_text": query,
            "mode": mode,
            "timestamp": ts,
            "channel_category": channel,
            "expected_commercial": False,
            "expected_sensitive": True,
            "ground_truth_category": cat,
        })
        case_id += 1

    # 3. Non-Commercial Informational Queries (40 items)
    informational_queries = [
        ("what is the capital of Switzerland", "SEARCH"),
        ("history of the Roman Empire timeline overview", "SEARCH"),
        ("explanation of quantum entanglement in simple terms", "SEARCH"),
        ("what is the chemical formula for photosynthesis", "SEARCH"),
        ("how does gravity warp spacetime according to general relativity", "SEARCH"),
        ("distance from Earth to the Moon in kilometers", "SEARCH"),
        ("what is the population of Tokyo in 2026", "SEARCH"),
        ("meaning of Schrödinger's cat paradox in quantum mechanics", "SEARCH"),
        ("chemical symbol for gold on the periodic table", "SEARCH"),
        ("python syntax for list comprehensions with conditions", "SEARCH"),
        ("who invented the printing press in Europe", "SEARCH"),
        ("how do solar eclipses occur diagram explanation", "YOUTUBE_STREAM"),
        ("what is the speed of light in a vacuum", "SEARCH"),
        ("overview of the French Revolution major causes", "SEARCH"),
        ("difference between DNA and RNA biological structure", "SEARCH"),
        ("how does photosynthesis convert light into glucose", "SEARCH"),
        ("what are Newton's three laws of motion with examples", "SEARCH"),
        ("definition of inflation in macroeconomics", "SEARCH"),
        ("how do volcanoes form at tectonic plate boundaries", "YOUTUBE_STREAM"),
        ("what is the deepest trench in the world ocean", "SEARCH"),
        ("who painted the Mona Lisa during the Renaissance", "SEARCH"),
        ("how does the human immune system recognize antigens", "SEARCH"),
        ("what causes ocean tides lunar gravity explanation", "SEARCH"),
        ("difference between mitosis and meiosis cell division", "SEARCH"),
        ("what is the Fibonacci sequence mathematical definition", "SEARCH"),
        ("how do rainbows form light refraction through water droplets", "YOUTUBE_STREAM"),
        ("what is the capital city of Australia", "SEARCH"),
        ("overview of the Magna Carta historical significance", "SEARCH"),
        ("how does nuclear fusion power the Sun", "YOUTUBE_STREAM"),
        ("what is the boiling point of water at high altitude", "SEARCH"),
        ("who wrote the plays Hamlet and Macbeth", "SEARCH"),
        ("how do airplanes generate lift Bernoulli principle", "YOUTUBE_STREAM"),
        ("what is the function of mitochondria in human cells", "SEARCH"),
        ("what is the atomic number of carbon", "SEARCH"),
        ("how does binary code represent numbers and text", "SEARCH"),
        ("what is the largest desert in the world", "SEARCH"),
        ("how does the water cycle circulate moisture globally", "YOUTUBE_STREAM"),
        ("what is the architectural design of Gothic cathedrals", "YOUTUBE_STREAM"),
        ("how do bees communicate using the waggle dance", "YOUTUBE_STREAM"),
        ("what is the distance from Earth to Mars on average", "SEARCH"),
    ]

    for query, mode in informational_queries:
        ts = 45.0 if mode == "YOUTUBE_STREAM" else None
        channel = "Educational Science" if mode == "YOUTUBE_STREAM" else None
        items.append({
            "id": f"TEST-{case_id:03d}",
            "input_text": query,
            "mode": mode,
            "timestamp": ts,
            "channel_category": channel,
            "expected_commercial": False,
            "expected_sensitive": False,
            "ground_truth_category": "informational",
        })
        case_id += 1

    out_file = Path(__file__).resolve().parent / "eval_dataset.json"
    out_file.parent.mkdir(parents=True, exist_ok=True)
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(items, f, indent=2)

    print(f"Successfully generated 150 test cases at {out_file}")

if __name__ == "__main__":
    build_eval_dataset()
