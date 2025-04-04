import json
import logging
import os
import pickle
from pathlib import Path

from config import MAX_HP, MAX_ENERGY

logger = logging.getLogger(__name__)


class DatabaseManager:
    """
    Manages persistence of user data and game stats.
    Uses pickle for data storage between sessions.
    """

    def __init__(self):
        """Initialize the database manager."""
        self.db_path = Path("rpg_database.pkl")
        self.data = {
            "users": {},
            "cooldowns": {},
            "inventories": {}
        }

    async def initialize(self):
        """Initialize the database and load existing data if available."""
        try:
            if self.db_path.exists():
                with open(self.db_path, 'rb') as f:
                    self.data = pickle.load(f)
                logger.info(f"Loaded database with {len(self.data['users'])} users")
            else:
                logger.info("No existing database found. Creating new database.")
                await self.save_data()
        except Exception as e:
            logger.error(f"Error initializing database: {e}")
            # Ensure we have a valid database even if loading fails
            await self.save_data()

    async def save_data(self):
        """Save the current data to disk."""
        try:
            with open(self.db_path, 'wb') as f:
                pickle.dump(self.data, f)
            logger.debug("Database saved successfully")
        except Exception as e:
            logger.error(f"Error saving database: {e}")

    async def get_user(self, user_id):
        """
        Get a user's data from the database.
        If the user doesn't exist, create a new entry.
        """
        user_id = str(user_id)  # Ensure user_id is a string

        if user_id not in self.data["users"]:
            # Create new user with default values
            self.data["users"][user_id] = {
                "hp": MAX_HP,
                "energy": MAX_ENERGY,
                "exp": 0,
                "level": 1
            }

            # Create empty inventory for the user
            self.data["inventories"][user_id] = {}

            # Create cooldowns entry for the user
            self.data["cooldowns"][user_id] = {}

            await self.save_data()

        return self.data["users"][user_id]

    async def get_all_users(self):
        """Get all users' data."""
        return self.data["users"]

    async def update_user_stat(self, user_id, stat, value):
        """Update a specific stat for a user."""
        user_id = str(user_id)

        # Get the user (or create if doesn't exist)
        user = await self.get_user(user_id)

        # Update the stat
        user[stat] = value
        await self.save_data()

        return user

    async def get_inventory(self, user_id):
        """Get a user's inventory."""
        user_id = str(user_id)

        # Ensure user exists
        await self.get_user(user_id)

        if user_id not in self.data["inventories"]:
            self.data["inventories"][user_id] = {}
            await self.save_data()

        return self.data["inventories"][user_id]

    async def add_item_to_inventory(self, user_id, item_id, quantity=1):
        """Add an item to a user's inventory."""
        user_id = str(user_id)
        inventory = await self.get_inventory(user_id)

        if item_id in inventory:
            inventory[item_id] += quantity
        else:
            inventory[item_id] = quantity

        await self.save_data()
        return inventory

    async def remove_item_from_inventory(self, user_id, item_id, quantity=1):
        """Remove an item from a user's inventory."""
        user_id = str(user_id)
        inventory = await self.get_inventory(user_id)

        if item_id not in inventory or inventory[item_id] < quantity:
            return False

        inventory[item_id] -= quantity

        if inventory[item_id] <= 0:
            del inventory[item_id]

        await self.save_data()
        return True

    async def set_cooldown(self, user_id, command, timestamp):
        """Set a cooldown for a specific command for a user."""
        user_id = str(user_id)

        # Ensure user exists
        await self.get_user(user_id)

        if user_id not in self.data["cooldowns"]:
            self.data["cooldowns"][user_id] = {}

        self.data["cooldowns"][user_id][command] = timestamp
        await self.save_data()

    async def get_cooldown(self, user_id, command):
        """Get the cooldown timestamp for a specific command for a user."""
        user_id = str(user_id)

        # Ensure user exists
        await self.get_user(user_id)

        if user_id not in self.data["cooldowns"] or command not in self.data["cooldowns"][user_id]:
            return 0

        return self.data["cooldowns"][user_id][command]

    async def add_coins(self, user_id, amount):
        """Add gacha coins to a user's account."""
        user_id = str(user_id)
        user = await self.get_user(user_id)

        if "coins" not in user:
            user["coins"] = 0

        user["coins"] += amount
        await self.save_data()
        return user["coins"]

    async def remove_coins(self, user_id, amount):
        """Remove gacha coins from a user's account."""
        user_id = str(user_id)
        user = await self.get_user(user_id)

        if "coins" not in user:
            return False

        if user["coins"] < amount:
            return False

        user["coins"] -= amount
        await self.save_data()
        return user["coins"]
