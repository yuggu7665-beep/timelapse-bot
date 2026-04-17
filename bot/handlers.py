"""
Telegram update handlers.
"""
import logging
from typing import Dict, Any
from bot.telegram_client import send_message, send_buttons, edit_message_reply_markup, set_my_commands
from bot.memory import get_user_memory, add_user_message, clear_user_memory
from bot.openai_client import generate_response
from bot.utils import split_message, extract_photo_info

logger = logging.getLogger(__name__)

def handle_update(update: Dict[str, Any]) -> None:
    """
    Route incoming update to appropriate handler.
    """
    if "message" in update:
        handle_message(update["message"])
    elif "callback_query" in update:
        handle_callback_query(update["callback_query"])
    else:
        logger.warning(f"Unhandled update type: {update.keys()}")

def handle_message(message: Dict[str, Any]) -> None:
    """
    Handle incoming text or photo messages.
    """
    chat_id = message["chat"]["id"]
    user_id = message["from"]["id"]

    # Check for photo
    if "photo" in message:
        # Treat as final result (IMAGE 4)
        photo_info = extract_photo_info(message["photo"])
        logger.info(f"User {user_id} sent photo: {photo_info}")
        # Add a system message indicating image upload
        add_user_message(user_id, "system",
                         "User uploaded a photo representing the final restored state (IMAGE 4). "
                         "Generate the full restoration sequence: IMAGE 1-3 and VIDEO 1-4.")
        # We'll also add a user message to trigger the AI
        text = "Generate restoration sequence for this uploaded final image."
    else:
        text = message.get("text", "").strip()
        if not text:
            return  # ignore empty messages

    # Handle commands
    if text.startswith("/"):
        handle_command(chat_id, user_id, text)
        return

    # Normal conversation flow
    memory = get_user_memory(user_id)
    # Add user message to memory (if not already added for photo case)
    if "photo" not in message:
        add_user_message(user_id, "user", text)

    # Generate AI response
    response = generate_response(user_id, memory)

    # Add assistant response to memory
    add_user_message(user_id, "assistant", response)

    # Send response to user
    for chunk in split_message(response):
        send_message(chat_id, chunk)

def handle_command(chat_id: int, user_id: int, command: str) -> None:
    """
    Handle slash commands.
    """
    # Strip args (e.g. /start@botname)
    base_command = command.split("@")[0].split()[0]

    if base_command in ("/start", "/menu"):
        send_welcome(chat_id)
    elif base_command == "/reset":
        clear_user_memory(user_id)
        send_message(chat_id, "✅ Memory cleared! Use /start to begin fresh.")
    elif base_command == "/spaces":
        send_welcome(chat_id)
    elif base_command == "/help":
        send_help(chat_id)
    elif base_command == "/about":
        send_about(chat_id)
    else:
        send_message(chat_id, f"❓ Unknown command: {command}\n\nTry /help to see available commands.")

def send_help(chat_id: int) -> None:
    """
    Send help message.
    """
    text = (
        "📖 <b>How to use the Restoration Timelapse Bot</b>\n\n"
        "1️⃣ Use /start or /spaces to pick a space type\n"
        "2️⃣ Tap one of the 10 space buttons\n"
        "3️⃣ Describe your vibe, features, and lighting\n"
        "4️⃣ Get 4 IMAGE + 4 VIDEO prompts instantly!\n\n"
        "<b>Commands:</b>\n"
        "/start — Start the bot\n"
        "/spaces — Show space options again\n"
        "/menu — Same as /start\n"
        "/reset — Clear memory & start fresh\n"
        "/help — Show this help\n"
        "/about — About this bot\n\n"
        "💡 <i>Tip: After generating prompts, paste them into OpenArt to create images/videos!</i>"
    )
    send_message(chat_id, text)

def send_about(chat_id: int) -> None:
    """
    Send about message.
    """
    text = (
        "🎬 <b>AI Restoration Timelapse Bot</b>\n\n"
        "This bot generates ultra-realistic, cinematic restoration\n"
        "timelapse prompts for 10 different space types.\n\n"
        "<b>What it does:</b>\n"
        "• Generates 4 IMAGE prompts (before → after stages)\n"
        "• Generates 4 VIDEO prompts (continuous timelapse)\n"
        "• Locked framing, real construction workflow\n"
        "• Ready to use in OpenArt, Midjourney, Sora & more\n\n"
        "Built with ❤️ using Python + Telegram Bot API"
    )
    send_message(chat_id, text)

def send_welcome(chat_id: int) -> None:
    """
    Send welcome message with inline keyboard buttons.
    """
    buttons = [
        [("🛋️ Interior Room", "space_interior")],
        [("🏠 Exterior Facade", "space_exterior")],
        [("🛣️ Road/Street/Driveway", "space_road")],
        [("🔧 Garage/Workshop", "space_garage")],
        [("🌿 Backyard/Landscape/Pool", "space_backyard")],
        [("🏙️ Luxury Apartment", "space_luxury")],
        [("🛍️ Retail/Showroom", "space_retail")],
        [("🏚️ Abandoned Property", "space_abandoned")],
        [("🕳️ Underground Space", "space_underground")],
        [("🔨 Custom Build Object", "space_custom")],
    ]
    text = (
        "Welcome to the AI Restoration Timelapse Prompt Generator! 🎬\n\n"
        "I'll help you create cinematic restoration sequences.\n"
        "Choose a space type to begin:"
    )
    send_buttons(chat_id, text, buttons)

def handle_callback_query(callback_query: Dict[str, Any]) -> None:
    """
    Handle button callbacks.
    """
    data = callback_query["data"]
    user_id = callback_query["from"]["id"]
    chat_id = callback_query["message"]["chat"]["id"]
    message_id = callback_query["message"]["message_id"]

    # Remove buttons after selection
    edit_message_reply_markup(chat_id, message_id, None)

    # Map callback data to space names
    space_map = {
        "space_interior": "Interior Room",
        "space_exterior": "Exterior Facade",
        "space_road": "Road/Street/Driveway",
        "space_garage": "Garage/Workshop",
        "space_backyard": "Backyard/Landscape/Pool",
        "space_luxury": "Luxury Apartment",
        "space_retail": "Retail/Showroom",
        "space_abandoned": "Abandoned Property",
        "space_underground": "Underground Space",
        "space_custom": "Custom Build Object",
    }
    if data in space_map:
        space = space_map[data]
        # Custom Build Object needs extra info about WHAT the object is
        if data == "space_custom":
            response = (
                "🔨 Great! You selected <b>Custom Build Object</b>.\n\n"
                "First, tell me: <b>what object do you want to build or restore?</b>\n"
                "(e.g. a wooden shed, stone wall, vintage car, brick oven, pergola...)\n\n"
                "Then also share:\n"
                "• <b>Vibe</b> – rustic, modern, industrial, etc.\n"
                "• <b>Must-have features</b> – materials, size, special details\n"
                "• <b>Lighting</b> – golden hour, overcast, studio, etc."
            )
        else:
            response = (
                f"Great! You selected <b>{space}</b>.\n\n"
                f"Now, please describe:\n"
                f"• <b>Vibe</b> – mood/style\n"
                f"• <b>Must-have features</b>\n"
                f"• <b>Lighting</b>\n\n"
                f"Or choose another space from the list."
            )
        send_message(chat_id, response)
        # Store selection in memory
        add_user_message(user_id, "system", f"User selected space: {space}")
    else:
        send_message(chat_id, f"Unknown selection: {data}")