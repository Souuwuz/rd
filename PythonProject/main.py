
from bot import setup_bot
from keep_alive import keep_alive
from uptime import setup_uptime_helper
# Load environment variables from .env file
load_dotenv()
logger.error(f"Error loading stats: {e}")
return jsonify({'error': 'Failed to load stats'}), 500
@app.route('/status')
def status():
    """Status endpoint for monitoring services."""
    return jsonify({
        'status': 'online',
        'bot': 'STATBOT',
        'version': '1.0.0'
    })
async def main():
    """
    Main entry point for the Discord RPG bot.
    """
    try:
        bot = await setup_bot()
        bot_token = os.getenv("DISCORD_BOT_TOKEN")
        if not bot_token:
            logger.error("No Discord bot token found in environment variables. Please set DISCORD_BOT_TOKEN.")
            return

        # Log successful connection
        logger.info("Starting Discord bot with token...")
        await bot.start(bot_token)
    except Exception as e:
        logger.error(f"Error starting bot: {e}")
        if __name__ == "__main__":
            # Start the keep-alive web server in a separate thread
            keep_alive()
            # Run the bot

            # Setup the uptime helper for 24/7 operation
            setup_uptime_helper()

            # Run the Discord bot
            logger.info("Starting Discord RPG Bot - Mortem House Stat")
            asyncio.run(main())
