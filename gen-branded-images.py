#!/usr/bin/env python3
import warnings; warnings.filterwarnings('ignore')
import os, base64
from google import genai
from google.genai import types

API_KEY = os.environ.get("GOOGLE_AI_API_KEY", "")
MODEL   = "gemini-3.1-flash-image-preview"
REFS    = "/Users/harrison/lifecykel-dashboard/product-refs"
OUT     = "/Users/harrison/lifecykel-dashboard/images"

client = genai.Client(api_key=API_KEY)

def load_image(path):
    ext = path.split(".")[-1].lower()
    mime = "image/png" if ext == "png" else "image/jpeg"
    with open(path, "rb") as f:
        data = base64.b64encode(f.read()).decode()
    return types.Part(inline_data=types.Blob(mime_type=mime, data=data))

def gen(filename, ref_path, prompt):
    output = f"{OUT}/{filename}"
    print(f"⏳ Generating {filename}...")
    try:
        img_part = load_image(ref_path)
        response = client.models.generate_content(
            model=MODEL,
            contents=[
                types.Content(parts=[
                    img_part,
                    types.Part(text=f"Using this exact product bottle as the subject, create a premium ad creative image: {prompt}. Keep the product bottle accurate and recognisable. No watermarks. No additional text overlays. Photorealistic editorial quality.")
                ])
            ],
            config=types.GenerateContentConfig(
                response_modalities=["IMAGE", "TEXT"],
            ),
        )
        for part in response.candidates[0].content.parts:
            if part.inline_data:
                raw = part.inline_data.data
                # data is already bytes from the SDK
                img_bytes = raw if isinstance(raw, bytes) else base64.b64decode(raw)
                with open(output, "wb") as f:
                    f.write(img_bytes)
                print(f"  ✅ {filename} ({os.path.getsize(output)//1000} KB)")
                return
        print(f"  ⚠️  {filename}: no image in response")
    except Exception as e:
        print(f"  ❌ {filename}: {e}")

LM  = f"{REFS}/lm-product.jpg"
CO  = f"{REFS}/cordyceps-product.jpg"
RE  = f"{REFS}/reishi-product.jpg"
SH  = f"{REFS}/shilajit-product.png"
NR  = f"{REFS}/liposomal-product.jpg"

jobs = [
    # Lion's Mane
    ("lm01.jpg", LM,
     "Product placed on a natural stone surface with soft warm morning light streaming in. Fresh lion's mane mushrooms arranged around the bottle. Earthy tones — cream, forest green, warm amber. Premium wellness editorial photography, shallow depth of field, bokeh background."),
    ("lm03.jpg", LM,
     "Product hero shot on a clean white background. Surrounded by floating gold 5-star icons and subtle review snippet bubbles. Bright clean studio lighting. Premium supplement advertising aesthetic."),
    ("lm04.jpg", LM,
     "Product bottle on the left in sharp focus with vibrant colour. On the right, a generic unlabelled mushroom powder jar slightly blurred and desaturated. Clean white background. Comparison advertising aesthetic."),
    ("lm06.jpg", LM,
     "Flat-lay lifestyle scene on a warm oak desk. Product bottle alongside a ceramic pour-over coffee cup, leather-bound journal, and fountain pen. Soft golden morning sunlight. Aspirational wellness lifestyle photography."),

    # Cordyceps
    ("co01.jpg", CO,
     "Product bottle on a gym bench, athletic training equipment blurred in background. Bold dramatic side lighting. Dark moody athletic aesthetic. High energy, performance-focused mood."),
    ("co03.jpg", CO,
     "Product bottle on a natural wood surface with soft morning light from the side. Minimal zen composition. One or two dried cordyceps mushrooms nearby. Premium clean product hero photography."),
    ("co05.jpg", CO,
     "Lifestyle flat-lay on a dark slate athletic surface. The Cordyceps bottle and a Lion's Mane dropper bottle (black with green/orange label) side by side. White earphones and a glass water bottle nearby. Premium supplement stack photography."),

    # Reishi
    ("re01.jpg", RE,
     "Product bottle on a cosy wooden side table next to a steaming chamomile tea mug and two lit candles. Warm amber evening light, soft shadows. Intimate, calming mood. Premium wellness lifestyle photography."),
    ("re03.jpg", RE,
     "Product bottle resting on soft white linen fabric with a dreamy soft-focus bedroom in the background. Floating gold star icons surrounding the bottle. Peaceful, sleep-focused aesthetic. Soft diffused lighting."),
    ("re04.jpg", RE,
     "Split panel editorial image. Left half: bright morning light with a Lion's Mane dropper bottle (black with green/orange label) next to an espresso cup. Right half: warm amber evening glow with the Reishi bottle next to chamomile tea. AM and PM ritual concept side by side."),

    # Shilajit
    ("sh01.jpg", SH,
     "The Shilajit jar sitting on rugged natural mountain rock. Dramatic moody side lighting from one direction. Dark, bold, masculine luxury aesthetic. Deep shadow and highlight contrast. Premium editorial supplement photography."),
    ("sh03.jpg", SH,
     "The Shilajit jar on the left in sharp focus and full colour. A generic white plastic capsule supplement bottle on the right, blurred and slightly desaturated. Clean white background. Comparison ad aesthetic showing quality difference."),
    ("sh04.jpg", SH,
     "The Shilajit jar on polished white marble surface. Warm gold backlighting creating a luxury halo effect. Clean, high-end editorial supplement photography. Marble texture, gold tones, premium minimalist composition."),

    # Liposomal NR+
    ("nr01.jpg", NR,
     "Product bottle on a clean white surface. Subtle scientific molecular structure graphics and cell illustrations floating softly in the background. Premium clinical wellness aesthetic. Bright, clean, authoritative lighting."),
    ("nr03.jpg", NR,
     "Product bottle on the right side of frame in sharp focus. On the left, a pile of broken open capsule pills spilling powder. Clean white background. Visual metaphor for superior absorption vs poor bioavailability. Clinical comparison aesthetic."),
    ("nr04.jpg", NR,
     "Product bottle on a clean minimalist surface. Soft Australian outback landscape visible through a large window in the background — red earth, eucalyptus trees, golden light. TGA regulatory authority aesthetic. Warm, trustworthy, premium Australian brand photography."),
]

print(f"Generating {len(jobs)} branded ad images...\n")
for filename, ref, prompt in jobs:
    gen(filename, ref, prompt)

print("\n✅ All done.")
