import asyncio
import discord
import logging
import os
from discord.ext import commands

# Import cogs
from cogs.combat import Combat
from cogs.profile import Profile
from cogs.inventory import Inventory
from cogs.gacha import Gacha
from cogs.admin import Admin
from utils.db_manager import DatabaseManager

# Configure logging
logger = logging.getLogger(__name__)


async def setup_bot():
    """
    Set up and configure the Discord bot with all necessary cogs and settings.
    """
    intents = discord.Intents.default()
    intents.message_content = True
    intents.members = True

    from config import DEFAULT_PREFIX
    bot = commands.Bot(command_prefix=DEFAULT_PREFIX, intents=intents)

    # Initialize database
    bot.db_manager = DatabaseManager()
    await bot.db_manager.initialize()

    # Store background tasks
    bot.background_tasks = []

    @bot.event
    async def on_ready():
        """
        Event handler for when the bot is ready and connected to Discord.
        """
        logger.info(f"Logged in as {bot.user.name} (ID: {bot.user.id})")
        logger.info("------")

        # Start background tasks for HP and Energy regeneration
        bot.background_tasks.append(bot.loop.create_task(regenerate_stats(bot)))

        # Set the bot's activity status
        await bot.change_presence(activity=discord.Game(name="RPG Adventure | Statbot!help"))

    @bot.event
    async def on_command_error(ctx, error):
        """
        Global error handler for the bot.
        """
        if isinstance(error, commands.CommandOnCooldown):
            minutes, seconds = divmod(error.retry_after, 60)
            hours, minutes = divmod(minutes, 60)
            if int(hours) == 0 and int(minutes) == 0:
                await ctx.send(f"This command is on cooldown. Try again in {int(seconds)} seconds.")
            elif int(hours) == 0:
                await ctx.send(
                    f"This command is on cooldown. Try again in {int(minutes)} minutes and {int(seconds)} seconds.")
            else:
                await ctx.send(
                    f"This command is on cooldown. Try again in {int(hours)} hours, {int(minutes)} minutes and {int(seconds)} seconds.")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"Missing required argument: {error.param.name}")
        elif isinstance(error, commands.CommandNotFound):
            await ctx.send("Command not found. Use Statbot!help to see available commands.")
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send("You don't have the required permissions to use this command.")
        else:
            logger.error(f"Command error: {error}")
            await ctx.send(f"An error occurred: {error}")

    # Add cogs to the bot
    await bot.add_cog(Combat(bot))
    await bot.add_cog(Profile(bot))
    await bot.add_cog(Inventory(bot))
    await bot.add_cog(Gacha(bot))
    await bot.add_cog(Admin(bot))

    return bot


async def regenerate_stats(bot):
    """
    Background task for regenerating HP and Energy for all users.
    """
    from config import HP_REGEN_RATE, HP_REGEN_INTERVAL, ENERGY_REGEN_RATE, ENERGY_REGEN_INTERVAL, MAX_HP, MAX_ENERGY

    logger.info("Starting stats regeneration task")

    hp_timer = 0
    energy_timer = 0

    while not bot.is_closed():
        await asyncio.sleep(60)  # Check every minute

        # Increment timers
        hp_timer += 60
        energy_timer += 60

        # HP regeneration cycle
        if hp_timer >= HP_REGEN_INTERVAL:
            hp_timer = 0
            users = await bot.db_manager.get_all_users()
            for user_id, user_data in users.items():
                if user_data['hp'] < MAX_HP:
                    new_hp = min(user_data['hp'] + HP_REGEN_RATE, MAX_HP)
                    await bot.db_manager.update_user_stat(user_id, 'hp', new_hp)
            logger.debug(f"HP regeneration cycle completed for {len(users)} users")

        # Energy regeneration cycle
        if energy_timer >= ENERGY_REGEN_INTERVAL:
            energy_timer = 0
            users = await bot.db_manager.get_all_users()
            for user_id, user_data in users.items():
                if user_data['energy'] < MAX_ENERGY:
                    new_energy = min(user_data['energy'] + ENERGY_REGEN_RATE, MAX_ENERGY)
                    await bot.db_manager.update_user_stat(user_id, 'energy', new_energy)
            logger.debug(f"Energy regeneration cycle completed for {len(users)} users")
