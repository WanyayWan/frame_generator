import base64
import json
import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llava:7b"

def image_to_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

image_b64 = image_to_base64("character.png")

prompt = """
You are a character analysis and prompt engineer for Stable Diffusion animation.

Look carefully at the image and do the following:

1. Describe the character's appearance in detail (hair, clothes, colors, style).
2. Create animation prompts for:
   - IDLE (subtle breathing, blinking)
   - TALK (mouth opening and closing naturally)
   - GREET (friendly expression, small wave)
3. Keep the character identity consistent.
4. Background should be simple and clean.
5. Style should match the image.

Return the result in JSON with these keys:
- character_description
- idle_prompt
- talk_prompt
- greet_prompt
- negative_prompt
"""

payload = {
    "model": MODEL,
    "prompt": prompt,
    "images": [image_b64],
    "stream": False
}

response = requests.post(OLLAMA_URL, json=payload, timeout=120)
response.raise_for_status()

result = response.json()["response"]

print("===== RAW OUTPUT =====")
print(result)

print("\n===== TRY PARSE JSON =====")
try:
    parsed = json.loads(result)
    print(json.dumps(parsed, indent=2))
except json.JSONDecodeError:
    print("⚠️ Output is not valid JSON. Still OK for now.")
   # print(result)