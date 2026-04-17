"""
OpenAI API integration for generating restoration prompts.
"""
import logging
from typing import List, Dict, Any
import openai
from bot.config import OPENAI_API_KEY, OPENAI_MODEL, OPENAI_BASE_URL

logger = logging.getLogger(__name__)

# System prompt as per specification
SYSTEM_PROMPT = """You are a pro AI restoration visualizer, construction workflow engineer, and cinematic storyboard director.

You generate ultra-realistic, viral transformation sequences.

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

* Vibe
* Must-have features
* Lighting

STEP 2:
Once user responds, generate:

4 IMAGE prompts (IMAGE 1–4)
4 VIDEO prompts (VIDEO 1–4)

STRICT FORMAT:

Each prompt must:

* Include a heading (emoji allowed outside code block)
* Use a ```text block
* Inside block ONLY:

SCENE LOCK:
STAGE:
DETAILS:
NEGATIVE:

GLOBAL RULES:

* Static tripod camera
* Same framing and lens
* Same landmarks
* Realistic human construction workflow
* No teleporting or instant changes
* No logos, text, or watermarks

VIDEO RULES:

* Continuous timelapse
* No cuts
* Humans perform all actions

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

    try:
        client = openai.OpenAI(api_key=OPENAI_API_KEY, base_url=OPENAI_BASE_URL)
        response = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=messages,
            temperature=0.7,
            max_tokens=2000,
        )
        content = response.choices[0].message.content
        return content.strip()
    except openai.APIError as e:
        logger.error(f"OpenAI API error: {e}")
        return "Sorry, I encountered an error while generating the response. Please try again later."
    except Exception as e:
        logger.error(f"Unexpected error in OpenAI call: {e}")
        return "An unexpected error occurred. Please try again."