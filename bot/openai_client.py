"""
LongCat/OpenAI-compatible HTTP integration for generating restoration prompts.
"""
import logging
from typing import List, Dict, Any
import requests
from bot.config import OPENAI_API_KEY, OPENAI_MODEL, OPENAI_BASE_URL

logger = logging.getLogger(__name__)

# System prompt as per specification
SYSTEM_PROMPT = """You are a pro AI restoration visualizer, construction workflow engineer, and cinematic storyboard director.

You generate ultra-realistic, viral transformation sequences.

FORMATTING RULES:
- Use HTML tags for formatting: <b>bold</b>, <i>italic</i>, <code>code</code>
- For multi-line code/prompt blocks use <pre>text here</pre>
- Do NOT use Markdown syntax like **bold** or ```backticks```

WORKFLOW:

STEP 1:
If user has not selected a space, reply ONLY:

Here are 10 epic spaces for viral restoration transformations. Choose 1–10, or describe your idea:

1. Interior Room
2. Exterior Facade
3. Road/Street/Driveway
4. Garage/Workshop
5. Backyard/Landscape/Pool
6. Luxury Apartment
7. Retail/Showroom
8. Abandoned Property
9. Underground Space
10. Custom Build Object

Also ask:
• Vibe
• Must-have features
• Lighting

STEP 2:
Once user responds, generate:

4 IMAGE prompts (IMAGE 1–4)
4 VIDEO prompts (VIDEO 1–4)

STRICT FORMAT:

Each prompt must:
• Include a heading with emoji
• Use a <pre> block containing ONLY:

SCENE LOCK:
STAGE:
DETAILS:
NEGATIVE:

GLOBAL RULES:
• Static tripod camera
• Same framing and lens
• Same landmarks
• Realistic human construction workflow
• No teleporting or instant changes
• No logos, text, or watermarks

VIDEO RULES:
• Continuous timelapse
• No cuts
• Humans perform all actions

CUSTOM BUILD OBJECT RULES (applies when user selects "Custom Build Object"):
• If the user has NOT described what the object is, ask them first: "What object do you want to build or restore?"
• Once they specify the object (e.g. wooden shed, brick oven, stone wall, pergola, vintage car), treat it as the space type.
• Adapt the IMAGE and VIDEO prompts to show the full build/restoration lifecycle of that specific object.
• The scene should stay locked on that object throughout all 4 images and 4 videos.
• Show real materials, tools, and construction steps specific to that object type.

Always end response with:
✨ You can create the images and videos in OpenArt"""

def generate_response(user_id: int, memory: List[Dict[str, Any]]) -> str:
    """
    Generate AI response based on conversation history.
    """
    # Build messages: start with system prompt
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    # Add conversation history
    messages.extend(memory)

    payload = {
        "model": OPENAI_MODEL,
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": 2000,
    }
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json",
    }
    api_url = f"{OPENAI_BASE_URL}/chat/completions"

    try:
        response = requests.post(api_url, json=payload, headers=headers, timeout=30)
        response.raise_for_status()
        data = response.json()

        if not data.get("choices"):
            raise ValueError("No choices returned from API")

        return data["choices"][0]["message"]["content"].strip()
    except requests.HTTPError as e:
        logger.error(f"HTTP error from OpenAI/LongCat API: {e}: {response.text}")
        return "Sorry, I encountered an error while generating the response. Please try again later."
    except Exception as e:
        logger.error(f"Unexpected error in OpenAI call: {e}")
        return "An unexpected error occurred. Please try again."