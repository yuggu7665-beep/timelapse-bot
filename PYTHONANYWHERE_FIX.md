# PythonAnywhere Fix: Missing requirements.txt

## Quick Solution (Run on PythonAnywhere)

1. **Create requirements.txt manually**:

   ```bash
   cd ~/timelapse-bot
   cat > requirements.txt << 'EOF'
   Flask==3.0.3
   python-telegram-bot==21.7
   openai==1.52.0
   requests==2.32.3
   python-dotenv==1.0.1
   redis==5.0.7  # optional for future
   psycopg2-binary==2.9.10  # optional for future
   EOF
   ```

2. **Or use the Python script**:

   ```bash
   cd ~/timelapse-bot
   python create_requirements.py
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Proper Git Setup

### On Your Local Machine (where code is):

```bash
# Add remote repository
git remote add origin https://github.com/yuggu7665-beep/timelapse-bot.git

# Rename branch to main
git branch -M main

# Push to GitHub
git push -u origin main
```

### On PythonAnywhere (after Git setup):

```bash
# Delete current directory and re-clone
cd ~
rm -rf timelapse-bot
git clone https://github.com/yuggu7665-beep/timelapse-bot.git
cd timelapse-bot

# Continue with deployment steps
python3.9 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Alternative: Manual File Creation

If you can't use Git, manually create these files on PythonAnywhere:

1. **requirements.txt** (as above)
2. **All other project files** - copy them from your local machine using SFTP or the PythonAnywhere file editor

## Next Steps After Fix

1. Create `.env` file with your credentials
2. Set up web app in PythonAnywhere dashboard
3. Set webhook: `python set_webhook.py`
4. Test the bot

The bot should now work with all dependencies installed.
