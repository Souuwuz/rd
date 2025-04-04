"""
Uptime helper for Discord bot.
This script helps keep the bot running 24/7 by using external uptime services.
"""

import os
import logging
import requests
from threading import Thread
import time

logger = logging.getLogger(__name__)

# How often to ping external services (in seconds)
PING_INTERVAL = 4 * 60 * 60  # 4 hours


def get_replit_url():
    """Get the public URL for this repl."""
    # For local development/testing, use the local IP
    return "http://0.0.0.0:8080"


def register_with_uptime_services():
    """
    Register the bot with free uptime monitoring services.
    You'll need to manually sign up for these services and add your URL.
    """
    replit_url = get_replit_url()
    logger.info(f"Replit URL for uptime services: {replit_url}")
    logger.info("To ensure 24/7 uptime:")
    logger.info("1. Sign up at UptimeRobot.com (free)")
    logger.info("2. Add a new HTTP(s) monitor with your repl URL:")
    logger.info(f"   {replit_url}")
    logger.info("3. Set checking interval to 5 minutes")


def setup_uptime_helper():
    """Set up the uptime helper."""
    register_with_uptime_services()

    # Even if not using uptime services, we can ping ourselves
    def self_ping_background():
        # Give the Flask server time to start up
        time.sleep(10)

        replit_url = get_replit_url()
        ping_url = f"{replit_url}/health"

        while True:
            try:
                logger.info(f"Self-pinging: {ping_url}")
                response = requests.get(ping_url, timeout=10)
                if response.status_code == 200:
                    logger.info("Self-ping successful")
                else:
                    logger.warning(f"Self-ping returned status code: {response.status_code}")
            except Exception as e:
                logger.error(f"Error during self-ping: {e}")
                logger.info("Will try again later...")

            # Sleep before next ping
            time.sleep(PING_INTERVAL)

    # Start self-ping thread
    ping_thread = Thread(target=self_ping_background)
    ping_thread.daemon = True
    ping_thread.start()

    logger.info("Uptime helper started!")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    setup_uptime_helper()