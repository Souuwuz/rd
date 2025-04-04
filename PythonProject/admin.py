import discord
import logging
from discord.ext import commands

from config import MAX_HP, MAX_ENERGY

logger = logging.getLogger(__name__)


class Admin(commands.Cog):
    """
    Admin commands for the RPG bot.
    Special commands that can only be used by authorized roles.
    """

    def __init__(self, bot):
        self.bot = bot

        # List to store authorized role IDs
        # These would normally be stored in a configuration file or database
        self.authorized_roles = []

        # Special role ID for healing command
        self.healing_role_id = 1356952258444525750

        # List to store moderator role IDs for EXP grant
        self.moderator_roles = []

    def cog_check(self, ctx):
        """
        Check that runs before any command in this cog.
        Verifies the user has an authorized role.
        """
        # Always allow bot owner
        if ctx.author.id == self.bot.owner_id:
            return True

        # Check for authorized roles
        if ctx.guild:
            user_roles = [role.id for role in ctx.author.roles]
            return any(role_id in self.authorized_roles for role_id in user_roles)

        return False

    async def heal_check(self, ctx):
        """Special check for heal command."""
        # Always allow bot owner
        if ctx.author.id == self.bot.owner_id:
            return True

        # Check for healing role
        if ctx.guild:
            user_roles = [role.id for role in ctx.author.roles]
            return self.healing_role_id in user_roles

        return False

    @commands.command(name="heal")
    async def heal(self, ctx, user: discord.Member = None):
        """
        Fully restore HP and Energy for a user.
        Only available to the healing role (ID: 1356952258444525750).

        Usage: Statbot!heal or Statbot!heal @username
        """
        if not await self.heal_check(ctx):
            await ctx.send("You don't have permission to use this command. It's restricted to the Healer role only.")
            return

        # If no user specified, use the command author
        if user is None:
            user = ctx.author

        # Get user data
        user_data = await self.bot.db_manager.get_user(user.id)

        # Restore HP and Energy
        user_data['hp'] = MAX_HP
        user_data['energy'] = MAX_ENERGY

        # Update in database
        await self.bot.db_manager.update_user_stat(user.id, 'hp', MAX_HP)
        await self.bot.db_manager.update_user_stat(user.id, 'energy', MAX_ENERGY)

        await ctx.send(f"✨ {user.mention}'s HP and Energy have been fully restored!")

    async def moderator_check(self, ctx):
        """Check if user has a moderator role."""
        # Always allow bot owner
        if ctx.author.id == self.bot.owner_id:
            return True

        # Check for moderator roles
        if ctx.guild:
            user_roles = [role.id for role in ctx.author.roles]
            return any(role_id in self.moderator_roles for role_id in user_roles) or any(
                role.permissions.administrator or role.permissions.manage_guild for role in ctx.author.roles)

        return False

    @commands.command(name="grantexp")
    async def grant_exp(self, ctx, user: discord.Member, amount: int):
        """
        Grant experience points to a user.
        Only available to moderator roles and above.
        Max 10,000 EXP per grant.

        Usage: Statbot!grantexp @username <amount>
        """
        if not await self.moderator_check(ctx):
            await ctx.send("You don't have permission to use this command. It's restricted to moderator roles only.")
            return

        # Limit amount to 10,000
        amount = min(amount, 10000)

        if amount <= 0:
            await ctx.send("The EXP amount must be positive.")
            return

        # Get user data
        user_data = await self.bot.db_manager.get_user(user.id)

        # Get current level before adding EXP
        from utils.helpers import get_current_level
        current_level = get_current_level(user_data['exp'])

        # Add EXP
        user_data['exp'] += amount
        await self.bot.db_manager.update_user_stat(user.id, 'exp', user_data['exp'])

        # Calculate new level
        new_level = get_current_level(user_data['exp'])

        # Check if user leveled up
        level_up = new_level > current_level

        if level_up:
            # Update level in the database
            await self.bot.db_manager.update_user_stat(user.id, 'level', new_level)
            await ctx.send(f"Granted {amount} EXP to {user.mention}. They leveled up to Level {new_level}! 🎉")
        else:
            await ctx.send(f"Granted {amount} EXP to {user.mention}. Current level: {new_level}")

    @commands.command(name="grantrole")
    @commands.is_owner()
    async def grant_role(self, ctx, role: discord.Role):
        """
        Add a role to the list of authorized roles.
        Only available to the bot owner.

        Usage: Statbot!grantrole @role
        """
        if role.id in self.authorized_roles:
            await ctx.send(f"The role {role.name} is already authorized.")
            return

        self.authorized_roles.append(role.id)
        await ctx.send(f"The role {role.name} has been added to the authorized roles list.")

    @commands.command(name="grantmodrole")
    @commands.is_owner()
    async def grant_mod_role(self, ctx, role: discord.Role):
        """
        Add a role to the list of moderator roles.
        Only available to the bot owner.

        Usage: Statbot!grantmodrole @role
        """
        if role.id in self.moderator_roles:
            await ctx.send(f"The role {role.name} is already a moderator role.")
            return

        self.moderator_roles.append(role.id)
        await ctx.send(f"The role {role.name} has been added to the moderator roles list.")

    @commands.command(name="revokerole")
    @commands.is_owner()
    async def revoke_role(self, ctx, role: discord.Role):
        """
        Remove a role from the list of authorized roles.
        Only available to the bot owner.

        Usage: Statbot!revokerole @role
        """
        if role.id not in self.authorized_roles:
            await ctx.send(f"The role {role.name} is not an authorized role.")
            return

        self.authorized_roles.remove(role.id)
        await ctx.send(f"The role {role.name} has been removed from the authorized roles list.")

    @commands.command(name="revokemodrole")
    @commands.is_owner()
    async def revoke_mod_role(self, ctx, role: discord.Role):
        """
        Remove a role from the list of moderator roles.
        Only available to the bot owner.

        Usage: Statbot!revokemodrole @role
        """
        if role.id not in self.moderator_roles:
            await ctx.send(f"The role {role.name} is not a moderator role.")
            return

        self.moderator_roles.remove(role.id)
        await ctx.send(f"The role {role.name} has been removed from the moderator roles list.")

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        """Handle command errors."""
        if isinstance(error, commands.CheckFailure):
            if ctx.command.cog_name == self.__class__.__name__:
                await ctx.send(
                    "You don't have permission to use this command. It's restricted to authorized roles only.")
