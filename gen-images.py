#!/usr/bin/env python3
import warnings; warnings.filterwarnings('ignore')
import os, sys, time
from google import genai
from google.genai import types

API_KEY = os.environ.get("GOOGLE_AI_API_KEY", "")
MODEL = "imagen-4.0-generate-001"
OUT_DIR = "/Users/harrison/lifecykel-dashboard/images"
os.makedirs(OUT_DIR, exist_ok=True)

client = genai.Client(api_key=API_KEY)

# Which batch to run (pass as arg: 1, 2, 3, 4, 5)
batch = int(sys.argv[1]) if len(sys.argv) > 1 else 1

BATCHES = {
    1: [  # Lion's Mane
        ("lm01.jpg", "Product photography of a premium mushroom supplement liquid extract bottle with dark green label on a clean modern desk workspace. Split composition: left side shows a foggy cluttered desk with scattered papers and dim light, right side shows a pristine organized workspace bathed in warm morning light with the supplement bottle as hero. Earthy natural colour palette with forest greens and warm golds. Professional advertising photography, soft natural lighting, shallow depth of field. No text. No watermarks. No logos."),
        ("lm03.jpg", "Premium mushroom supplement liquid extract bottle centred on pure white background, surrounded by floating golden five-star icons and soft review card elements. Product hero shot with warm studio lighting, the bottle glowing with rich amber-brown liquid inside. Trust badges and star ratings floating around the product. Clean, minimal, high-end supplement advertising style. Professional product photography, 4K quality. No text. No watermarks. No logos."),
        ("lm04.jpg", "Side by side comparison advertising image. Left side: a generic white mushroom powder supplement jar looking dull and clinical, dusty powder spilling out, cold blue-grey tones. Right side: a premium dark glass liquid extract bottle with dropper, rich golden-amber liquid, warm inviting lighting, fresh Australian native plum fruits beside it. Clear visual contrast between cheap powder and premium liquid. Clean infographic advertising style. No text. No watermarks. No logos."),
        ("lm06.jpg", "Lifestyle flat-lay photography from above: a premium mushroom supplement liquid extract bottle laying on a natural linen surface alongside a ceramic coffee cup, a leather journal, reading glasses, and a smartphone. Morning light streaming in from the side. Warm, Instagram-worthy styling with earthy natural tones — creams, greens, warm browns. Aspirational but accessible daily wellness aesthetic. Professional overhead photography. No text. No watermarks. No logos."),
    ],
    2: [  # Cordyceps
        ("co01.jpg", "Bold athletic advertising image: a premium mushroom supplement liquid extract bottle with amber liquid, positioned front-and-centre against a dramatic gym/outdoor athletic backdrop with morning sunlight. A synthetic neon-coloured pre-workout tub sits crossed out and faded in the background. High-energy, powerful composition. Dark athletic aesthetic with pops of natural green and gold. Professional sports supplement advertising photography. No text. No watermarks. No logos."),
        ("co03.jpg", "Premium mushroom supplement liquid extract bottle with amber liquid on a natural wood surface, bathed in warm golden morning light. The bottle is hero-lit from behind creating a natural glow. Simple elegant composition with the product as focal point. Natural earthy background with blurred green foliage. Clean, warm, inviting product photography. Professional advertising quality. No text. No watermarks. No logos."),
        ("co05.jpg", "Lifestyle flat-lay of two premium mushroom supplement liquid extract bottles laying side by side on a modern workout bench. One bottle has a bright energetic orange-amber tone, the other a calmer golden tone. A gym towel, water bottle, and earbuds in the scene. Morning light, clean athletic-meets-wellness aesthetic. Warm natural tones with touches of green. Professional product photography from above. No text. No watermarks. No logos."),
    ],
    3: [  # Reishi
        ("re01.jpg", "Cozy evening lifestyle scene: a premium mushroom supplement liquid extract bottle on a side table next to a steaming ceramic cup of herbal tea. Soft ambient candlelight, a plush couch with a knit throw blanket visible. Person's hand reaching for the tea cup. Warm, moody evening tones — deep greens, warm ambers, soft shadows. Calming, inviting atmosphere. Professional lifestyle photography with shallow depth of field. No text. No watermarks. No logos."),
        ("re03.jpg", "Dreamy, soft-focus bedroom scene with a premium mushroom supplement liquid extract bottle on a bedside table. Warm low lighting from a table lamp. The bottle hero-lit with soft golden glow. Peaceful, serene atmosphere with rumpled linen sheets and a book in the background. Muted earth tones — deep forest green, warm gold, soft cream. Professional product photography with bokeh. No text. No watermarks. No logos."),
        ("re04.jpg", "Two-panel split composition: Left panel shows bright warm morning light, a premium supplement bottle next to a coffee cup on a kitchen counter, energetic vibrant tones. Right panel shows warm cozy evening light, a different premium supplement bottle next to a tea cup, candle glow, calming muted tones. The contrast between energised morning and peaceful evening. Clean editorial advertising layout. Professional photography. No text. No watermarks. No logos."),
    ],
    4: [  # Shilajit
        ("sh01.jpg", "Dark, dramatic product photography of a premium glass jar containing thick black Shilajit resin. The jar is hero-lit against a dramatic mountain rock backdrop with moody storm clouds. Gold and amber accent lighting creating a luxurious, powerful atmosphere. A tiny brass spoon rests beside the jar. Premium masculine energy — luxury supplement meets ancient wisdom aesthetic. Dark tones with gold highlights. Professional advertising photography. No text. No watermarks. No logos."),
        ("sh03.jpg", "Clean comparison advertising image. Left side: a cheap-looking white plastic jar with generic dark powder spilling out, cold clinical lighting, untrusted feel. Right side: a premium glass jar with authentic thick black Shilajit resin, warm gold lighting, a tiny spoon, mountain imagery subtly in background, trustworthy premium feel. Clear quality contrast. Professional product comparison photography. No text. No watermarks. No logos."),
        ("sh04.jpg", "Luxury product photography of a premium Shilajit resin glass jar on a polished marble surface with warm amber backlighting. A tiny brass spoon rests elegantly beside it. Sophisticated, aspirational aesthetic. Rich dark tones with gold and amber highlights. Morning coffee cup slightly blurred in background for scale reference. Premium supplement advertising style, shot like a luxury fragrance ad. No text. No watermarks. No logos."),
    ],
    5: [  # Liposomal NR+
        ("nr01.jpg", "Scientific-meets-premium advertising image: a sleek supplement bottle on one side, with an abstract visualization of healthy glowing cells and molecular structures on the other side. Cool blue and warm gold colour palette meeting in the middle. Clinical credibility mixed with premium lifestyle appeal. Modern, clean, sophisticated. Australian-made supplement aesthetic. Professional advertising photography with motion graphics feel. No text. No watermarks. No logos."),
        ("nr03.jpg", "Visual comparison concept: on the left, supplement capsules dissolving and breaking apart in stylized stomach acid, fading away — representing poor absorption. On the right, a glowing protective lipid bubble encasing a supplement molecule, intact and powerful — representing liposomal delivery. Split composition with warm golds on the liposomal side and cold grey on the capsule side. Scientific illustration meets advertising photography. No text. No watermarks. No logos."),
        ("nr04.jpg", "Clean, authoritative product photography of a premium liquid supplement bottle on a white background with subtle Australian-themed elements — eucalyptus leaves, native botanicals. Official, trustworthy, clinical aesthetic. The bottle is perfectly lit with soft diffused studio lighting. A subtle quality seal or badge element in gold. Medical-grade meets premium wellness brand. Professional product photography, clean and minimal. No text. No watermarks. No logos."),
    ],
}

if batch not in BATCHES:
    print(f"Usage: python3 gen-images.py [1-5]")
    sys.exit(1)

for filename, prompt in BATCHES[batch]:
    out_path = os.path.join(OUT_DIR, filename)
    if os.path.exists(out_path):
        print(f"⏭ {filename} already exists, skipping")
        continue
    print(f"🎨 Generating {filename}...")
    try:
        response = client.models.generate_images(
            model=MODEL,
            prompt=prompt,
            config=types.GenerateImagesConfig(
                number_of_images=1,
                aspect_ratio="1:1",
                output_mime_type="image/jpeg",
            ),
        )
        if response.generated_images:
            with open(out_path, "wb") as f:
                f.write(response.generated_images[0].image.image_bytes)
            print(f"  ✅ {filename} ({os.path.getsize(out_path)/1000:.0f} KB)")
        else:
            print(f"  ❌ No image returned for {filename}")
    except Exception as e:
        print(f"  ❌ Error: {e}")
    time.sleep(2)

print(f"\n✅ Batch {batch} complete!")
