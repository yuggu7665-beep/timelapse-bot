"""
Main Flask application for Telegram bot webhook.
"""
import os
import logging
from flask import Flask, request, jsonify
from bot.handlers import handle_update

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/')
def health_check():
    """Health check endpoint."""
    return jsonify({"status": "ok", "service": "telegram-restoration-bot"})

@app.route('/webhook', methods=['POST'])
def webhook():
    """
    Main webhook endpoint for Telegram updates.
    """
    try:
        update = request.get_json()
        logger.debug(f"Received update: {update}")
        # Process update asynchronously (or directly)
        handle_update(update)
        return jsonify({"status": "ok"}), 200
    except Exception as e:
        logger.error(f"Error processing webhook: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # For local development only
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)