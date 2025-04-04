level = logging.INFO,
format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create a simple Flask server for keep alive
app = Flask(__name__) \
 \
      @ app.route('/')


def home():
    return "Bot is running!"


def run_server():
    app.run(host='0.0.0.0', port=8080)


async def main():
    """
    Main entry point for the Discord RPG bot.
    """
    try:
        # Start Flask server in a separate thread
        server_thread = Thread(target=run_server)
        server_thread.daemon = True
        server_thread.start()

        # Set up and start the bot
        bot = await setup_bot()
        bot_token = os.getenv("DISCORD_BOT_TOKEN")
        if not bot_token:
            logger.error("No Discord bot token found in environment variables. Please set DISCORD_BOT_TOKEN.")
            return

        logger.info("Starting Discord bot with token...")
        await bot.start(bot_token)
    except Exception as e:
        logger.error(f"Error starting bot: {e}")


if __name__ == "__main__":
    # Run the bot and keep it alive
    asyncio.run(main())