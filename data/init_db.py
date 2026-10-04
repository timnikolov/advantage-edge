"""
Database Initializer for AdVantage-Edge Catalog.
Creates SQLite tables and seeds 100+ commercial product listings across 6 key verticals.
"""

import sqlite3
import random
import sys
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.config import settings

def init_database(db_path: Path = None):
    if db_path is None:
        db_path = settings.db_path

    # Ensure parent directory exists
    db_path.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Drop existing tables if re-initializing
    cursor.execute("DROP TABLE IF EXISTS inventory")
    cursor.execute("DROP TABLE IF EXISTS sponsors")

    # Create schema
    cursor.execute("""
        CREATE TABLE inventory (
            product_id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            category TEXT NOT NULL,
            price REAL NOT NULL,
            bid REAL NOT NULL,
            ctr REAL NOT NULL,
            merchant TEXT NOT NULL,
            deep_link TEXT NOT NULL,
            keywords TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE sponsors (
            product_id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            category TEXT NOT NULL,
            price REAL NOT NULL,
            bid REAL NOT NULL,
            ctr REAL NOT NULL,
            merchant TEXT NOT NULL,
            deep_link TEXT NOT NULL,
            keywords TEXT NOT NULL
        )
    """)

    # Seed data generator templates across 6 verticals
    categories = {
        "electronics": [
            ("WH-1000XM5 Noise Canceling Headphones", "Sony", 399.99, 4.50, 0.08, "headphones noise canceling audio bluetooth bluetooth5 wireless sony sound music studio microphone soundproof ANC"),
            ("MacBook Pro 14 M3", "Apple Store", 1599.00, 7.50, 0.09, "laptop macbook computer apple m3 pro software developer coding design workstation retina screen metal body M3 Max M3 Pro keyboard trackpad"),
            ("Galaxy S24 Ultra 5G", "Samsung Electronics", 1299.99, 6.80, 0.075, "smartphone phone Android Samsung S24 ultra camera 5G mobile cellular stylus screen OLED 200MP zoom titanium screen protector charger case"),
            ("Ultra-Wide 34-inch Gaming Monitor", "LG Electronics", 499.99, 3.80, 0.065, "monitor curved display 144Hz IPS gaming screen 4k HDMI desktop ultra wide PC gaming setup rig refresh rate dual monitor arm stand desk displayport"),
            ("Mechanical RGB Keyboard", "Keychron", 119.99, 2.10, 0.055, "keyboard mechanical typing switches gaming hot-swappable Keychron wireless Bluetooth mechanical switch keycaps aluminum ergonomic wrist rest retro keycaps LED RGB backlight"),
            ("Ergonomic Wireless Mouse", "Logitech", 99.99, 1.80, 0.06, "mouse logitech MX Master ergonomic bluetooth computer accessories laser sensor infinite scroll precision CAD productive quiet clicks dual mode wireless"),
            ("Smart Watch Series 9", "Apple Store", 399.00, 4.20, 0.07, "smartwatch apple watch fitness heart rate health tracker GPS cellular Series 9 OLED Always On blood oxygen ECG step counter workout band silicon strap"),
            ("4K Drone Quadcopter with Camera", "DJI", 759.00, 5.20, 0.085, "drone camera dji quadcopter 4k video aerial photography gimbal stabilized flight controller obstacle avoidance compact folding remote controller SD card fly more combo"),
            ("Smart Home Security Camera System", "Ring", 199.99, 2.90, 0.05, "camera security smart home wifi night vision outdoor indoor floodlight motion detection 1080p cloud storage door chime subscription battery solar panel"),
            ("Noise-Isolating Earbuds Pro", "Bose", 279.00, 3.90, 0.07, "earbuds wireless bluetooth Bose noise isolation sound sport sweatproof charging case active noise cancellation spatial audio ear tips true wireless touch control"),
            ("High Speed Wi-Fi 6E Mesh Router", "TP-Link", 249.99, 2.70, 0.048, "router wifi wifi6 mesh network gigabit internet coverage signal booster dual band tri-band ethernet port low latency gaming stream fiber modem compatibility"),
            ("4K OLED 65-inch Smart TV", "LG Electronics", 1799.99, 8.00, 0.095, "tv television OLED 4k 65inch smart tv streaming HDR webOS Dolby Vision gaming mode 120Hz HDMI2.1 cinema wall mount soundbar eARC remote control"),
            ("Portable Bluetooth Speaker Waterproof", "JBL", 129.95, 1.95, 0.062, "speaker bluetooth portable waterproof JBL bass party audio outdoor travel battery USB-C speakerphone strap rugged IP67 float dustproof stereo pair"),
            ("VR Headset 128GB", "Meta Quest", 499.00, 5.10, 0.078, "vr headset virtual reality gaming Oculus controllers 3D immersive passthrough wireless standalone games fitness spatial computing 4K resolution head strap"),
            ("1080p Webcam with Autofocus", "Logitech", 79.99, 1.45, 0.042, "webcam logitech 1080p stream streaming video call Zoom Teams conference lighting privacy shutter dual mic USB tripod mount auto focus 60fps frame rate"),
            ("USB-C Multi-Port Hub Adapter", "Anker", 49.99, 1.10, 0.04, "adapter usb-c hub hdmi ethernet card reader dongle laptop macbook pc power delivery 100W USB 3.0 pass through aluminum portable slim multiport splitter"),
            ("E-Reader Paper White Display", "Kindle", 139.99, 2.05, 0.053, "kindle e-reader book reading e-ink waterproof glare-free battery light warm light digital book store libby audiobooks bluetooth prime reading"),
            ("Professional Condenser Microphone", "Blue Yeti", 129.99, 2.30, 0.058, "microphone mic podcast streaming recording voiceover condenser USB Blue Yeti gain control pop filter shock mount cardioid omni directional studio quality"),
            ("Solid State Drive 2TB NVMe", "Samsung Electronics", 179.99, 2.60, 0.061, "ssd storage nvme 2tb fast read write speed hard drive pc upgrade gaming internal storage PCIe Gen4 heat sink M.2 laptop expansion PS5 compatible"),
            ("Wireless Charging Pad Trio", "Belkin", 69.99, 1.25, 0.038, "charger wireless charging pad magsafe apple watch airpods iphone fast charge desk stand Qi certified LED indicator alignment multi device dock")
        ],
        "home_improvement": [
            ("Dishwasher Pump Replacement Kit", "ApplianceParts Direct", 45.99, 2.80, 0.09, "dishwasher pump fix repair noise drainage kitchen appliance part water drain impeller motor gasket clamp DIY fix replacement OEM seal easy install"),
            ("Cordless Brushless Drill Combo Kit", "DEWALT", 199.00, 4.20, 0.085, "drill cordless impact driver power tool dewalt battery charger 20V MAX heavy duty torque masonry wood metal contractor case contractor kit brushless"),
            ("Smart Wi-Fi Programmable Thermostat", "ecobee", 189.99, 3.50, 0.065, "thermostat smart home temperature climate control energy saving app control Alexa Siri HVAC heat pump furnace sensor geofencing schedule saving energy"),
            ("High Pressure Shower Head Stainless", "Kohler", 79.00, 1.90, 0.052, "shower head high pressure stainless steel bathroom plumbing water saving spray handheld massage easy installation hose anti clog chrome rainfall stream"),
            ("Heavy Duty Garage Shelving Rack", "Gorilla Racks", 149.99, 2.40, 0.045, "shelving Garage storage rack heavy duty steel 5-tier adjustable warehouse basement organization capacity 2000lbs powder coat tool organizer metal shelves"),
            ("Self-Leveling Cross Line Laser Level", "Bosch", 129.00, 2.75, 0.058, "laser level Bosch cross line self leveling green beam tripod wall mount alignment tile hanging drywall framing construction precision 360 degree layout"),
            ("Automated Robot Lawn Mower", "Husqvarna", 1199.00, 6.50, 0.072, "lawn mower robot grass cutter garden yard smart app control boundary wire GPS anti theft quiet battery powered terrain slope rain sensor boundary wire"),
            ("Paint Sprayer Airless System", "Graco", 289.00, 3.90, 0.061, "paint sprayer airless painter house fence wall spray gun compressor nozzle Graco stain latex contractor DIY house exterior interior renovator hose"),
            ("Water Leak Detector Alarm 3-Pack", "Govee", 39.99, 0.95, 0.041, "water leak sensor alarm plumbing basement pipe drip overflow flood alert battery wifi smart app notification basement laundry sink pump security"),
            ("Motion Sensor LED Floodlight Outdoor", "Lutron", 64.99, 1.30, 0.048, "floodlight outdoor motion sensor LED security light dusk to dawn waterproof yard driveway fixture luminary adjustable heads ultra bright dusk to dawn"),
            ("Kitchen Sink Faucet Pull-Down Sprayer", "Delta Faucet", 159.99, 3.10, 0.063, "faucet kitchen sink pull down sprayer stainless steel chrome single handle touch clean magnetic docking spot resistant deck plate counter mounting"),
            ("Digital Electronic Deadbolt Lock", "Schlage", 129.99, 2.65, 0.054, "door lock deadbolt keypad keyless entry smart home SCHLAGE security pin code auto lock mechanical key emergency backup zinc alloy heavy duty matte black"),
            ("16-Foot Extension Ladder Fiberglass", "Werner", 219.00, 3.20, 0.049, "ladder extension ladder fiberglass heavy duty Werner 225 lbs rating non conductive roof gutter repair high ceiling foldable rung locks safety feet"),
            ("PEX Tubing Crimp Tool Kit", "SharkBite", 69.99, 1.40, 0.046, "pex crimp tool plumbing pipe fittings cutter gauge copper ring SharkBite cinch tool water pipe repair DIY leak fixture PEX-A PEX-B crimper gauge"),
            ("Drain Snake Cleaner Auger 25ft", "RIDGID", 34.99, 0.90, 0.051, "drain snake auger clogged sink shower plumbing pipe hair remover manual drum auger cable drill adapter plumbing snake cleanout tool trap removal"),
            ("Heavy Duty Workbench with Pegboard", "Husky", 349.00, 4.80, 0.067, "workbench garage tool bench pegboard drawers solid wood top steel frame heavy duty shop workstation adjustable height outlet surge strip LED bar"),
            ("Drywall Joint Compound 5-Gallon", "USG Sheetrock", 22.99, 0.60, 0.035, "drywall compound spackle mud sheetrock wall repair taping plastering bucket smooth finish wall patch sanding scraper knife putty hawk trowel"),
            ("Circular Saw 7-1/4 Inch Corded", "Makita", 139.00, 2.45, 0.052, "circular saw Makita power saw wood cutting blade rip fence bevel angle framing lumber plywood carpenter contractor dust blower magnesium shoe"),
            ("Compact Shop Vacuum 5 Gallon 4.5 HP", "CRAFTSMAN", 69.99, 1.60, 0.047, "shop vac vacuum wet dry cleaner garage car detailing blower attachment hose filter bag tank heavy duty dust extraction workshop cleanup drain port"),
            ("Solar Powered Outdoor String Lights 50ft", "Brightech", 39.99, 0.85, 0.039, "string lights patio outdoor solar light LED Edison bulbs waterproof garden gazebo Bistro ambiance warm white shatterproof auto sensor dusk to dawn")
        ],
        "fashion": [
            ("Waterproof Trail Running Shoes", "Salomon", 160.00, 3.20, 0.075, "shoes running trail footwear waterproof gore-tex hiking sneakers grip traction Salomon speedcross marathon outdoor comfort cushioning mesh breathable"),
            ("Lightweight Down Puffer Jacket", "Patagonia", 229.00, 4.10, 0.082, "jacket puffer down lightweight winter coat warm insulated windproof outdoor hiking Patagonia eco recycled packable zip hood navy blue black stylish"),
            ("Classic Fit Denim Jeans 501", "Levi's", 79.50, 1.80, 0.058, "jeans denim pants Levis 501 classic fit cotton straight leg dark wash indigo fashion casual wear belt loops durable classic American style"),
            ("Polarized UV400 Wayfarer Sunglasses", "Ray-Ban", 163.00, 3.40, 0.069, "sunglasses ray-ban polarized wayfarer UV protection eyewear style fashion summer beach driving sun glasses anti glare tortoise shell case cleaning cloth"),
            ("Breathable Athletic Training Shorts", "Nike", 45.00, 1.10, 0.049, "shorts athletic workout gym running sports dri-fit breathable stretch waistband pockets Nike training activewear casual summer sweat wicking"),
            ("Genuine Leather Minimalist Bifold Wallet", "Fossil", 48.00, 0.95, 0.042, "wallet leather bifold RFID blocking card holder cash pocket minimalist sleek gift brown black cowhide genuine slim front pocket organizer"),
            ("Merino Wool Crew Neck Sweater", "Uniqlo", 59.90, 1.25, 0.047, "sweater merino wool knit warm winter layering crew neck soft breathable thermal casual fashion office classic fit burgundy charcoal knitwear"),
            ("Waterproof Chronograph Stainless Watch", "Seiko", 295.00, 3.90, 0.064, "watch timepiece Seiko chronograph quartz stainless steel analog wrist watch water resistant sapphire crystal diver automatic date dial tachymeter silver"),
            ("Heavy Duty Canvas Workwear Jacket", "Carhartt", 129.99, 2.60, 0.056, "jacket workwear canvas duck canvas lined cold weather duck Carhartt durable heavy duty utility pockets zip front contractor rugged outdoor coat"),
            ("Ergonomic Travel Backpack 30L", "Osprey", 140.00, 2.90, 0.061, "backpack travel bag 30L waterproof laptop compartment Osprey carry on air mesh shoulder straps hiking commuter school daypack luggage luggage strap"),
            ("Seamless Moisture-Wicking Leggings", "Lululemon", 98.00, 2.70, 0.071, "leggings yoga pants high waist stretch Lululemon tights activewear workout gym compression squat proof soft feel seamless waistband pocket flex"),
            ("Classic Leather Dress Oxford Shoes", "Allen Edmonds", 395.00, 5.00, 0.068, "dress shoes oxfords leather dress shoes Goodyear welted formal business wear Italian leather black polished professional wedding suit shoes lace up"),
            ("Packable Waterproof Rain Coat", "Columbia", 89.99, 1.75, 0.051, "rain coat jacket waterproof Columbia breathable hood packable windbreaker seam sealed outdoor trail travel storm shield lightweight nylon shell"),
            ("Casual Slip-On Canvas Sneakers", "Vans", 65.00, 1.15, 0.044, "sneakers vans canvas slip on casual shoes skateboarding waffle sole low top classic black white board shoes streetwear everyday comfortable"),
            ("100% Silk Business Necktie Classic", "Brooks Brothers", 75.00, 1.35, 0.038, "necktie silk tie business suit formal silk woven stripe patterned Brooks Brothers wedding interview office gentleman attire woven jacquard neckwear"),
            ("Thermal Compression Base Layer Set", "Under Armour", 85.00, 1.65, 0.052, "base layer thermal compression shirt leggings Under Armour winter warm cold gear fleece sweat wicking ski snowboarding active base layer tight fit"),
            ("Wide Brim UPF 50+ Sun Protection Hat", "Coolibar", 42.00, 0.85, 0.039, "sun hat hat wide brim UPF 50 UV protection beach safari hiking chin strap foldable lightweight neck flap breathable sun block outdoor hat"),
            ("Fleece Lined Hooded Sweatshirt", "Champion", 55.00, 1.05, 0.046, "hoodie sweatshirt fleece champion reverse weave pullover athletic hoodie front pocket heavy weight cotton casual winter streetwear comfort relaxed fit"),
            ("Leather Chelsea Boots Waterproof", "Blundstone", 219.95, 3.80, 0.066, "boots chelsea boots leather blundstone slip on elastic side pull tab oil resistant lug sole durable outdoor fashion work boot unisex comfortable"),
            ("Unisex Cotton Baseball Cap Curved", "Adidas", 28.00, 0.65, 0.037, "hat cap baseball cap adidas cotton adjustable strap three stripes dad hat sports sun protection casual embroidered logo curved peak headwear")
        ],
        "sports": [
            ("Adjustable Selectorized Dumbbells 50lbs", "Bowflex", 429.00, 5.50, 0.088, "dumbbells weights adjustable strength training home gym workout equipment Bowflex bicep bench press fitness weight plates rack 50lb pair selector pin"),
            ("Foldable Motorized Treadmill 3.0 HP", "NordicTrack", 999.00, 7.20, 0.079, "treadmill running machine cardio home gym workout incline foldable screen motor NordicTrack running belt heart rate monitor cushion deck exercise"),
            ("Insulated Stainless Steel Water Bottle 32oz", "Hydro Flask", 44.95, 1.20, 0.052, "water bottle hydro flask insulated stainless steel cold hot vacuum straw lid gym hiking leakproof BPA free double wall thermal flask bottle holder"),
            ("High Density Non-Slip Yoga Mat 6mm", "Manduka", 88.00, 1.65, 0.055, "yoga mat non slip high density Manduka workout exercise stretching pilates cushion eco friendly floor mat sweat resistant strap carrying loop"),
            ("GPS Smart Cycling Bike Computer", "Garmin", 299.99, 4.10, 0.063, "cycling bike computer garmin GPS speed cadence heart rate sensor map navigation route tracking handlebar mount battery wireless USB bike sensor"),
            ("Spinning Indoor Exercise Bike", "Peloton", 1445.00, 8.00, 0.092, "exercise bike indoor cycle peloton spin workout cardio screen resistance magnetic pedals silent flywheel live classes subscription home gym fitness"),
            ("Heavy Duty Resistance Loop Bands 5-Set", "TRX", 34.95, 0.80, 0.043, "resistance bands exercise bands TRX workout latex stretch mobility therapy fitness set pull up assist booty bands handles door anchor travel pouch"),
            ("Pro Pickleball Paddle Carbon Fiber", "Selkirk", 149.99, 2.75, 0.068, "pickleball paddle carbon fiber honeycomb core Selkirk grip pickle ball tournament approved spin power control court ball bag cover lightweight balance"),
            ("Waterproof 4-Person Camping Tent", "Coleman", 129.99, 2.30, 0.051, "camping tent 4 person waterproof Coleman rainfly dome tent easy setup fiberglass poles outdoor gear backpacking ground tarp mesh ventilation door window"),
            ("Self-Inflating Sleeping Pad Mattress", "Therm-a-Rest", 99.95, 1.85, 0.047, "sleeping pad camping mattress thermal insulated self inflating foam lightweight backpacking sleep system compact valve ground insulation bag outdoor sleep"),
            ("Pro Graphite Tennis Racket 100 sq in", "Wilson", 229.00, 3.60, 0.061, "tennis racket racket Wilson graphite power control string grip unstrung 100 sq in court tournament pro staff blade clash spin tennis bag dampener"),
            ("Standard Size Composite Leather Basketball", "Spalding", 39.99, 0.90, 0.042, "basketball Spalding official size indoor outdoor composite leather grip air pump inflation needle court game ball high bounce deep channel design"),
            ("Professional Golf Driver 10.5 Degree", "TaylorMade", 549.99, 6.00, 0.073, "golf driver golf club TaylorMade titanium carbon face adjustable loft speed pocket shaft headcover golf balls swing speed distance forgiveness tee box"),
            ("Cast Iron Kettlebell 35lbs Ergonomic", "Rogue Fitness", 65.00, 1.40, 0.049, "kettlebell Rogue fitness weights cast iron powder coat strength crossfit squat swing press home gym weight training flat bottom color coded ring handle"),
            ("Foldable Multi-Position Weight Bench", "FLYBIRD", 149.99, 2.50, 0.057, "weight bench bench press adjustable incline decline flat exercise workout strength training home gym dumbbell rack compact foldable leg lock footrest"),
            ("Heavy Bag Punching Set 80lbs", "Everlast", 139.99, 2.20, 0.048, "boxing heavy bag punching bag Everlast gloves hand wraps ceiling mount chain MMA martial arts kickboxing workout stress relief leatherette shell fill"),
            ("Hydration Pack Backpack 2L Bladder", "CamelBak", 79.99, 1.50, 0.044, "hydration pack CamelBak water reservoir 2L bladder trail running cycling hiking backpack bite valve hose chest strap lightweight hydration vest pockets"),
            ("Graphite Badminton Racket 2-Pack Set", "Yonex", 89.99, 1.35, 0.041, "badminton racket Yonex shuttlecocks birdies net set backyard court carbon frame lightweight high tension string carrying bag grip tape outdoor game"),
            ("Inflatable Stand Up Paddle Board 10'6\"", "ROC", 299.99, 4.00, 0.066, "paddle board SUP stand up inflatable board paddle pump leash backpack waterproof bag lake ocean water sports stability fin ankle strap repair kit"),
            ("Heavy Jump Rope Weighted Cable 1lb", "Crossrope", 49.00, 0.95, 0.040, "jump rope weighted cable speed rope Crossrope double unders cardio handles fast rotation tangle free workout fitness endurance training adjustable length")
        ],
        "wellness": [
            ("Deep Tissue Percussion Muscle Massager", "Theragun", 299.00, 4.80, 0.081, "massager percussion massage gun Theragun muscle recovery deep tissue sore throat back soreness battery speed settings attachments quiet glide athlete motor"),
            ("Aromatherapy Ultrasonic Essential Oil Diffuser", "URPOWER", 29.99, 0.75, 0.041, "diffuser essential oil aromatherapy ultrasonic mist LED ambient lights lavender humidity home fragrance relaxation sleep timer auto shut off wood grain"),
            ("Organic Cold Pressed CBD Oil 1000mg", "Charlotte's Web", 74.99, 1.90, 0.053, "cbd oil tincture hemp extract organic stress sleep recovery relief drop sublingual natural flavor third party tested hemp full spectrum dropper 30ml"),
            ("Weighted Blanket 15lbs Glass Beads", "YnM", 69.99, 1.40, 0.048, "weighted blanket 15lb deep sleep anxiety stress relief cotton cover glass beads heavy blanket twin queen size breathable sensory comforting hug"),
            ("Smart Electric Sonic Toothbrush 4 Modes", "Philips Sonicare", 99.99, 2.10, 0.062, "toothbrush electric sonicare philips plaque removal whitening brush heads charging travel case timer pressure sensor battery rechargeable 4 modes clean"),
            ("Filtered Water Pitcher 10-Cup BPA Free", "Brita", 34.99, 0.85, 0.044, "water filter brita pitcher tap water purification lead reduction BPA free 10 cup filter replacement indicator clean taste water dispenser kitchen fridge"),
            ("Air Purifier HEPA Filter Quiet Room", "Levoit", 99.99, 2.30, 0.059, "air purifier HEPA filter Levoit quiet sleep dust smoke pollen allergen remover odor air quality sensor room bedroom office replacement filter CADR speed"),
            ("Melatonin Sleep Aid Gummies 5mg", "Natrol", 14.99, 0.45, 0.038, "sleep aid melatonin gummies natural sleep insomnia rest 5mg berry flavor non habit forming relaxation night bedtime dietary supplement 90 count bottle"),
            ("Organic Whey Protein Powder Chocolate 2lb", "Optimum Nutrition", 44.99, 1.25, 0.051, "protein powder whey Optimum Nutrition gold standard BCAAs muscle recovery shake workout nutrition chocolate flavor 24g protein 5.5g BCAA scoop 2lb tub"),
            ("Multivitamin Daily Gummies for Adults", "Centrum", 19.99, 0.50, 0.036, "multivitamin vitamins daily supplement gummies immune support energy health centrum A C D3 zinc minerals adults dietary daily nutrition 120 count"),
            ("Shiatsu Neck and Back Massager Heat", "Naipo", 49.99, 1.10, 0.045, "massager shiatsu neck back massage heat nodes deep tissue shoulder chair cushion car adapter muscle tension relief electric corded kneading straps"),
            ("Pure Magnesium Glycinate 400mg Caps", "Pure Encapsulations", 28.50, 0.70, 0.042, "magnesium glycinate supplement sleep cramp relief muscle relaxation nerve support non GMO vegetarian capsules gentle stomach 120 count high absorption"),
            ("Infrared Heating Pad for Back Pain", "UTK", 119.00, 2.40, 0.056, "heating pad infrared jade stones back pain relief thermotherapy deep heat auto turn off temperature control electric heat pad spine lumbar joint relief"),
            ("Probiotic 50 Billion CFU 10 Strains", "Garden of Life", 34.99, 0.95, 0.046, "probiotic digestive health gut microbiota 50 billion CFU acidophilus daily supplement women men shelf stable vegetarian capsules immune defense prebiotic"),
            ("Smart Body Fat Scale Bluetooth BMI", "Withings", 79.95, 1.60, 0.050, "scale smart scale body fat BMI weight muscle mass sync app bluetooth wifi Withings digital bathroom scale multi user health tracking glass step on"),
            ("SAD Light Therapy Lamp 10000 Lux", "Verilux", 49.99, 1.05, 0.043, "light therapy lamp happy light 10000 lux SAD seasonal depression mood daylight sun light UV free timer adjustable brightness desktop compact stand"),
            ("Collagen Peptides Powder Unflavored 20oz", "Vital Proteins", 27.99, 0.80, 0.047, "collagen peptides powder grass fed skin hair nails joint health vital proteins amino acids unflavored coffee mix protein keto paleo 20 oz tub scoop"),
            ("Organic Matcha Green Tea Powder 100g", "Jade Leaf", 24.95, 0.65, 0.040, "matcha green tea powder organic ceremonial grade Japanese antioxidants caffeine l-theanine energy focus whisk latte smoothie tin 100g superfood"),
            ("Digital Blood Pressure Monitor Upper Arm", "Omron", 59.99, 1.30, 0.049, "blood pressure monitor Omron cuff upper arm hypertension pulse meter heart rate memory store irregular heartbeat detector clinically validated LCD screen"),
            ("Acupressure Mat and Pillow Set", "ProsourceFit", 29.99, 0.60, 0.037, "acupressure mat pillow set back pain relief acupuncture points relaxation muscle tension cotton linen travel bag spikes trigger point therapy mat")
        ],
        "automotive": [
            ("Portable Car Jump Starter 2000A", "NOCO", 99.95, 2.40, 0.065, "jump starter car battery charger 2000A peak NOCO boost portable power bank LED flashlight 12V gas diesel engine cables clamp emergency trunk kit"),
            ("Obd2 Scanner Code Reader Diagnostic", "Autel", 49.99, 1.15, 0.048, "obd2 scanner code reader diagnostic engine check light reset car scan tool Autel live data DTC clear freeze frame error code OBDII mechanic cable"),
            ("Synthetic Motor Oil 5W-30 5 Quarts", "Mobil 1", 29.99, 0.85, 0.042, "motor oil synthetic 5w-30 5w30 Mobil 1 engine protection mileage filter change lube oil change jug car maintenance anti wear high temperature"),
            ("Digital Tire Pressure Gauge 150 PSI", "AstroAI", 14.99, 0.40, 0.035, "tire pressure gauge digital 150 PSI AstroAI LCD backlit nozzle car truck bike tire air pressure check valve stem heavy duty accuracy metric PSI BAR"),
            ("All-Weather Rubber Car Floor Mats 4-Piece", "WeatherTech", 149.95, 3.10, 0.058, "floor mats car mats rubber weathertech all weather waterproof custom fit trim to fit SUV truck sedan front rear liner dirt mud snow protection black"),
            ("Heavy Duty Cordless Tire Inflator Air Compressor", "DEWALT", 129.00, 2.70, 0.054, "tire inflator air compressor portable 20V battery 12V car plug auto shut off digital gauge hose DEWALT emergency flat tire inflation bike balls rafts"),
            ("Full HD 4K Dash Cam Front and Rear", "Viofo", 169.99, 3.50, 0.066, "dash cam camera 4K 1080p front rear dual lens GPS Wi-Fi night vision G-sensor parking mode loop recording MicroSD card Viofo car camera security"),
            ("High Performance Ceramic Brake Pad Set", "Brembo", 75.00, 1.80, 0.049, "brake pads ceramic rotor Brembo stopping power low dust silent braking car repair replacement front rear caliper hardware kit OEM fitment disc brake"),
            ("Professional Car Detailing Cleaning Kit 12-Piece", "Chemical Guys", 89.99, 2.10, 0.057, "car wash detailing kit chemical guys soap wax microfiber towel wheel cleaner foam cannon tire shine interior cleaner bucket sponge polisher shine streak free"),
            ("Bluetooth FM Transmitter Car Charger", "Anker", 24.99, 0.60, 0.041, "fm transmitter bluetooth car charger USB wireless audio streaming adapter hands free calling mic radio adapter handsfree cigarette lighter socket 12V"),
            ("Pure Carnauba Car Paste Wax 12oz", "Meguiar's", 21.99, 0.55, 0.038, "car wax Meguiars carnauba paste wax paint protection high gloss shine applicator pad scratch swirl remover polish clear coat paint finish shine"),
            ("Heavy Duty Tow Strap 30ft 30000lbs", "Rhino USA", 39.99, 0.90, 0.043, "tow strap recovery strap 30ft 30000 lb break strength Rhino USA shackled polyester loop reinforced ends offroad winch 4x4 truck SUV vehicle recovery"),
            ("Car Battery Trickle Charger Maintainer 12V", "Schumacher", 39.99, 0.85, 0.040, "battery charger trickle maintainer 12V 6V automatic Float mode lead acid AGM GEL motorcycle car boat lawn mower Schumacher emergency backup battery"),
            ("LED Headlight Bulb Conversion Kit H11", "AUXITO", 59.99, 1.40, 0.052, "led headlights bulbs H11 6000K cool white bright fog light conversion kit fanless plug and play beam pattern IP67 waterproof halogen replacement"),
            ("Heavy Duty Hydraulic Floor Jack 3 Ton", "Pittsburgh", 139.99, 2.90, 0.047, "floor jack hydraulic 3 ton steel low profile garage jack lift vehicle jack stands vehicle repair oil change brake job swivel casters dual piston pump"),
            ("Car Windshield Sun Shade Foldable Accordion", "EcoNour", 15.99, 0.40, 0.036, "sun shade windshield car sun visor heat reflector UV blocker accordion folding front window storage pouch dashboard protection SUV sedan truck shade"),
            ("Universal Roof Rack Cross Bars Aluminum", "CargoLoc", 89.99, 1.95, 0.045, "roof rack cross bars aluminum universal luggage cargo carrier kayak bike carrier mounting clamps locking system roof rails 150 lbs load capacity"),
            ("Silicone Beam Wiper Blades 26+18 Pair", "Rain-X", 29.99, 0.70, 0.042, "wiper blades Rain-X beam silicone windshield wipers rain water repellent windshield wiper pair easy adapter smooth streak free silent wipe clean view"),
            ("Synthetic Chamois Leather Car Drying Towel", "Absorber", 16.99, 0.38, 0.034, "chamois drying towel absorber car wash synthetic leather lint free streak free super absorbent cleaning rag detailer towel wash tube storage case"),
            ("12V Portable Car Vacuum Cleaner High Power", "THISWORX", 32.99, 0.75, 0.044, "car vacuum portable 12V corded high power hand vacuum detailing kit nozzle filter brush bag car interior clean pet hair dirt sand trash cleaner")
        ]
    }

    inserted_count = 0
    item_id = 1000

    for cat_name, product_list in categories.items():
        for item in product_list:
            title, merchant, price, bid, ctr, keywords = item
            product_id = f"PROD-{cat_name[:3].upper()}-{item_id}"
            deep_link = f"https://shop.example.com/item/{product_id.lower()}?ref=advantage_edge"

            cursor.execute("""
                INSERT INTO inventory (product_id, title, category, price, bid, ctr, merchant, deep_link, keywords)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (product_id, title, cat_name, price, bid, ctr, merchant, deep_link, keywords))

            # Populate sponsors table (mirrors inventory for structured ad queries)
            cursor.execute("""
                INSERT INTO sponsors (product_id, title, category, price, bid, ctr, merchant, deep_link, keywords)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (product_id, title, cat_name, price, bid, ctr, merchant, deep_link, keywords))

            item_id += 1
            inserted_count += 1

    conn.commit()
    conn.close()
    print(f"Successfully initialized catalog database at {db_path} with {inserted_count} products.")
    return inserted_count

if __name__ == "__main__":
    init_database()
