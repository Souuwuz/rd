import os
import time
import requests
import logging
from flask import Flask
from threading import Thread

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get the Replit URL for pinging
REPLIT_URL = os.environ.get('REPLIT_URL',
                            f"https://{os.environ.get('REPL_SLUG')}.{os.environ.get('REPL_OWNER')}.repl.co")


@app.route('/')
def home():
    """Simple endpoint for Replit to ping and keep the repl alive."""
    return "Bot is alive!"


@app.route('/health')
def health():
    """Health check endpoint for monitoring."""
    return {"status": "healthy", "timestamp": time.time()}


def ping_self():
    """Ping the application to keep it alive."""
    while True:
        try:
            time.sleep(60 * 5)  # Ping every 5 minutes
            response = requests.get(f"{REPLIT_URL}/health")
            logger.info(f"Self-ping status: {response.status_code}")
        except Exception as e:
            logger.error(f"Error pinging self: {e}")


def run():
    """Run the Flask app in a separate thread."""
    app.run(host='0.0.0.0', port=8080)


def keep_alive():
    """Start threads to run the Flask app and ping service."""
    # Start the Flask server
    server_thread = Thread(target=run)
    server_thread.daemon = True
    server_thread.start()

    # Start the self-ping service
    ping_thread = Thread(target=ping_self)
    ping_thread.daemon = True
    ping_thread.start()

    logger.info("Keep-alive service started")