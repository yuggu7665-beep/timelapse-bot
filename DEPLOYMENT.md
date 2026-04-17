# Deployment Guide: PythonAnywhere & Git

## 1. Push to a Private Git Repository

### If you haven't set up a remote repository yet:

**On GitHub / GitLab / Bitbucket:**

1. Create a new private repository (do not initialize with README).
2. Copy the remote URL (e.g., `https://github.com/yuggu7665-beep/timelapse-bot.git`).

**In your local project directory, run:**

```bash
# Add remote (replace URL with your own)
git remote add origin https://github.com/yuggu7665-beep/timelapse-bot.git

# Rename branch to main (optional)
git branch -M main

# Push to remote
git push -u origin main
```

**If you already have a remote but want to replace everything (force push):**

```bash
# Force push (overwrites remote history)
git push -u origin main --force
```

## 2. Deploy on PythonAnywhere

### Step‑by‑step copy‑paste commands (run in PythonAnywhere Bash console)

```bash
# 1. Clone your repository (if you haven't uploaded manually)
git clone https://github.com/yuggu7665-beep/timelapse-bot.git
cd timelapse-bot

# 2. Create a virtual environment
python3.9 -m venv venv
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create a .env file with your actual keys
cat > .env << 'EOF'
TELEGRAM_TOKEN=8779036874:AAHPCE4FH33wv6jzfzqjJ9_NLEzWW4fTVh4
OPENAI_API_KEY=ak_24e4WW3Bn3tf1vj2zR9yR2C01qN13
OPENAI_BASE_URL=https://api.longcat.chat/openai
OPENAI_MODEL=LongCat-Flash-Chat
MAX_HISTORY_PER_USER=20
WEBHOOK_URL=https://galxy678.pythonanywhere.com/webhook
EOF

# 5. Test that the app loads
python -c "from app import app; print('Flask app loaded successfully')"
```

### Step‑by‑step Web App Configuration (PythonAnywhere Dashboard)

1. Go to the **Web** tab.
2. Click **Add a new web app** → **Manual configuration** → **Python 3.9**.
3. In the **Code** section, set the source directory to `/home/galxy678/timelapse-bot`.
4. In the **Virtualenv** section, enter `/home/galxy678/timelapse-bot/venv`.
5. **WSGI configuration** – click the link to edit the WSGI file.

Replace the entire content of the WSGI file with:

```python
import sys
import os

project_home = '/home/galxy678/timelapse-bot'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

from dotenv import load_dotenv
load_dotenv(os.path.join(project_home, '.env'))

from app import app as application
```

6. **Static files** – not needed for this bot.
7. Go back to the **Web** tab and click the green **Reload** button.

### Set the Telegram Webhook

After the web app is running (green "live" status), run the following command in a Bash console:

```bash
cd timelapse-bot
source venv/bin/activate
python set_webhook.py
```

If you haven't set `WEBHOOK_URL` in `.env` yet, update it first:

```bash
sed -i "s|WEBHOOK_URL=.*|WEBHOOK_URL=https://galxy678.pythonanywhere.com/webhook|" .env
```

Then run the webhook script again.

### Verify the Webhook

Visit `https://galxy678.pythonanywhere.com/` in your browser. You should see:

```json
{ "status": "ok", "service": "telegram-restoration-bot" }
```

## 3. Test the Bot

1. Open Telegram and search for your bot (by its username).
2. Send `/start` – you should receive the welcome message with four buttons.
3. Select a space type and follow the conversation.

## 4. Monitoring & Logs

- **PythonAnywhere logs**: Go to the **Web** tab and click **Error log** or **Access log**.
- **Bot logs**: All errors are printed to the console (visible in the **Web** tab under **Log files** → **Server log**).

## 5. Troubleshooting

| Issue              | Solution                                                                        |
| ------------------ | ------------------------------------------------------------------------------- |
| 502 Bad Gateway    | Check the error log; likely missing dependencies or environment variables.      |
| Webhook not set    | Verify `WEBHOOK_URL` is correct and the endpoint `/webhook` returns 200.        |
| Bot not responding | Check the Telegram token and that the webhook is set (`python set_webhook.py`). |
| OpenAI API errors  | Ensure the LongCat API key is valid and the model name is correct.              |

## 6. Updating the Bot

```bash
cd timelapse-bot
git pull origin main
source venv/bin/activate
pip install -r requirements.txt  # if dependencies changed
# Reload the web app from the PythonAnywhere Web tab
```

---

**Your bot is now live and ready to generate cinematic restoration timelapse prompts!**
