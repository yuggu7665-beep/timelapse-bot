# AI Restoration Timelapse Prompt Generator (Telegram Bot)

A production-ready Telegram bot that replicates a custom GPT experience for generating AI restoration timelapse prompts. The bot maintains conversation memory per user, supports button UI, image input, and generates cinematic restoration prompts (IMAGE 1–4, VIDEO 1–4) using OpenAI's GPT.

## Features

- **Webhook-based** (no polling) using Flask
- **OpenAI Integration** with configurable model (gpt-4o by default)
- **Per‑user memory** (in‑memory dict, upgradable to Redis)
- **Telegram UI** with inline keyboard buttons for space selection
- **Image upload handling** – treats uploaded photos as final result (IMAGE 4) and generates the full restoration sequence
- **Response splitting** for long messages (respects Telegram's 4096‑character limit)
- **Error handling & logging** for API failures

## Tech Stack

- Python 3.9+
- Flask (web framework)
- python‑telegram‑bot (for Telegram API interactions)
- OpenAI Python SDK
- (Optional) Redis, PostgreSQL for future scaling

## Project Structure

```
.
├── app.py                 # Flask application & webhook endpoints
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── .env.example          # Example environment variables
└── bot/                  # Core bot modules
    ├── __init__.py
    ├── config.py         # Configuration & environment
    ├── handlers.py       # Telegram update handlers
    ├── memory.py         # In‑memory conversation storage
    ├── openai_client.py  # OpenAI API integration
    ├── telegram_client.py# Telegram API wrapper
    └── utils.py          # Utility functions (splitting, photo extraction)
```

## Setup for Local Development

1. **Clone the repository**

   ```bash
   git clone <repo-url>
   cd timelapse
   ```

2. **Create a virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set environment variables**

   Copy `.env.example` to `.env` and fill in your keys:

   ```bash
   cp .env.example .env
   ```

   Edit `.env`:

   ```ini
   TELEGRAM_TOKEN=your_telegram_bot_token
   OPENAI_API_KEY=your_openai_api_key
   OPENAI_MODEL=gpt-4o  # optional
   MAX_HISTORY_PER_USER=20
   WEBHOOK_URL=https://yourdomain.com/webhook  # required for production
   ```

5. **Run the Flask app locally**

   ```bash
   python app.py
   ```

   The app will start on `http://0.0.0.0:5000`.

6. **Set up a tunnel for webhook (ngrok)**

   Because Telegram requires HTTPS for webhooks, use ngrok to expose your local server:

   ```bash
   ngrok http 5000
   ```

   Copy the HTTPS URL (e.g., `https://abc123.ngrok.io`) and set it as `WEBHOOK_URL` in your `.env`.

7. **Set the webhook**

   Run the provided script (or manually call the Telegram API) to set the webhook:

   ```bash
   python -c "from bot.telegram_client import set_webhook; set_webhook('https://abc123.ngrok.io/webhook')"
   ```

   Alternatively, you can use the Telegram Bot API directly:

   ```
   curl -X POST https://api.telegram.org/bot<YOUR_TOKEN>/setWebhook?url=https://abc123.ngrok.io/webhook
   ```

8. **Start chatting**

   Open your Telegram bot and send `/start`.

## Deployment on PythonAnywhere

PythonAnywhere is a popular hosting platform for Python web apps. Follow these steps:

### 1. Create a PythonAnywhere account

Sign up at [pythonanywhere.com](https://www.pythonanywhere.com).

### 2. Upload your code

- Open a **Bash console**.
- Clone your repository or upload files via the **Files** tab.
- Ensure the project is in your user directory, e.g., `/home/yourusername/timelapse`.

### 3. Set up a virtual environment

In the Bash console:

```bash
cd timelapse
python3.9 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root with the same content as above. Alternatively, use PythonAnywhere’s **Environment variables** in the **Web app** configuration.

### 5. Create a web app

- Go to the **Web** tab and click **Add a new web app**.
- Choose **Manual configuration** (not Flask).
- Select Python version 3.9 (or higher).

### 6. Configure WSGI

Edit the WSGI file (linked from the Web tab). Replace its content with:

```python
import sys
import os

# Add your project directory to the sys.path
project_home = '/home/yourusername/timelapse'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Load environment variables
from dotenv import load_dotenv
load_dotenv(os.path.join(project_home, '.env'))

# Import Flask app
from app import app as application
```

### 7. Set static files (optional)

Not needed for this bot.

### 8. Set up webhook URL

Your PythonAnywhere web app will have a URL like `https://yourusername.pythonanywhere.com`. The webhook endpoint is `/webhook`.

Update your `.env`:

```
WEBHOOK_URL=https://yourusername.pythonanywhere.com/webhook
```

### 9. Set the Telegram webhook

Run a one‑time script to tell Telegram about your webhook. In a Bash console (with your virtual environment activated):

```python
python -c "from bot.telegram_client import set_webhook; set_webhook('https://yourusername.pythonanywhere.com/webhook')"
```

### 10. Reload the web app

Go back to the **Web** tab and click the green **Reload** button.

### 11. Test the bot

Send `/start` to your bot on Telegram. It should respond with the welcome message and buttons.

## Environment Variables

| Variable               | Description                                                                             | Required           |
| ---------------------- | --------------------------------------------------------------------------------------- | ------------------ |
| `TELEGRAM_TOKEN`       | Your Telegram Bot token from [@BotFather](https://t.me/BotFather)                       | Yes                |
| `OPENAI_API_KEY`       | Your OpenAI API key                                                                     | Yes                |
| `OPENAI_MODEL`         | OpenAI model to use (default: `gpt-4o`)                                                 | No                 |
| `MAX_HISTORY_PER_USER` | Maximum number of messages stored per user (default: 20)                                | No                 |
| `WEBHOOK_URL`          | Full HTTPS URL where your webhook is reachable (e.g., `https://yourdomain.com/webhook`) | Yes for production |

## Future‑Ready Architecture

The code is designed to be easily extended:

- **Memory**: The `memory.py` module uses an in‑memory dictionary. To switch to Redis, replace the internal store with a Redis client while keeping the same interface.
- **Database**: Add a `models.py` and use SQLAlchemy for persistent storage of user data, payment records, etc.
- **Payments**: Integrate Stripe / PayPal by adding a new handler for payment callbacks.
- **Image Generation APIs**: The photo‑handling logic can be extended to call DALL‑E, Stable Diffusion, or other image‑generation APIs.

## Error Handling & Logging

- All OpenAI API errors are caught and logged; the user receives a friendly error message.
- Telegram send failures are logged but not retried (for simplicity).
- Flask logs every webhook request; unhandled exceptions return HTTP 500.

## Testing Locally

1. Run the app with `python app.py`.
2. Use a tool like `curl` to simulate a Telegram update:

   ```bash
   curl -X POST http://localhost:5000/webhook -H "Content-Type: application/json" -d '{"message":{"chat":{"id":123},"from":{"id":456},"text":"/start"}}'
   ```

3. Check the console for logs.

## License

MIT
