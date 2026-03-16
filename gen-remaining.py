#!/usr/bin/env python3
import warnings; warnings.filterwarnings('ignore')
import os, time
from google import genai
from google.genai import types

API_KEY = os.environ.get("GOOGLE_AI_API_KEY", "")
MODEL = "imagen-4.0-generate-001"
OUT_DIR = "/Users/harrison/lifecykel-dashboard/images"
client = genai.Client(api_key=API_KEY)

REMAINING = [
    ("lm06.jpg", "Lifestyle flat-lay photography from above: a premium mushroom supplement liquid extract bottle laying on a natural linen surface alongside a ceramic coffee cup, a leather journal, reading glasses, and a smartphone. Morning light streaming in from the side. Warm, Instagram-worthy styling with earthy natural tones — creams, greens, warm browns. Aspirational but accessible daily wellness aesthetic. Professional overhead photography. No text. No watermarks. No logos."),
    ("re04.jpg", "Two-panel split composition: Left panel shows bright warm morning light, a premium supplement bottle next to a coffee cup on a kitchen counter, energetic vibrant tones. Right panel shows warm cozy evening light, a different premium supplement bottle next to a tea cup, candle glow, calming muted tones. The contrast between energised morning and peaceful evening. Clean editorial advertising layout. Professional photography. No text. No watermarks. No logos."),
    ("sh04.jpg", "Luxury product photography of a premium Shilajit resin glass jar on a polished marble surface with warm amber backlighting. A tiny brass spoon rests elegantly beside it. Sophisticated, aspirational aesthetic. Rich dark tones with gold and amber highlights. Morning coffee cup slightly blurred in background for scale reference. Premium supplement advertising style, shot like a luxury fragrance ad. No text. No watermarks. No logos."),
    ("nr03.jpg", "Visual comparison concept: on the left, supplement capsules dissolving and breaking apart in stylized stomach acid, fading away — representing poor absorption. On the right, a glowing protective lipid bubble encasing a supplement molecule, intact and powerful — representing liposomal delivery. Split composition with warm golds on the liposomal side and cold grey on the capsule side. Scientific illustration meets advertising photography. No text. No watermarks. No logos."),
    ("nr04.jpg", "Clean, authoritative product photography of a premium liquid supplement bottle on a white background with subtle Australian-themed elements — eucalyptus leaves, native botanicals. Official, trustworthy, clinical aesthetic. The bottle is perfectly lit with soft diffused studio lighting. A subtle quality seal or badge element in gold. Medical-grade meets premium wellness brand. Professional product photography, clean and minimal. No text. No watermarks. No logos."),
]

for filename, prompt in REMAINING:
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
    time.sleep(8)

print("\n✅ All remaining images complete!")
