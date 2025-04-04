"""
Configuration settings for the Discord RPG bot.
"""

# General settings
DEFAULT_PREFIX = "Statbot!"
MAX_HP = 100
MAX_ENERGY = 100
HP_REGEN_RATE = 2  # HP points per cycle
HP_REGEN_INTERVAL = 5 * 60  # 5 minutes in seconds
ENERGY_REGEN_RATE = 2  # Energy points per cycle
ENERGY_REGEN_INTERVAL = 3 * 60  # 3 minutes in seconds

# Combat settings
ATTACK_ENERGY_COST = 10
DEFENSE_ENERGY_COST = 5

# Level settings
LEVEL_THRESHOLDS = {
    1: 0,      # Default level
    5: 500,    # 500 EXP required for level 5
    10: 1000,  # 1,000 EXP required for level 10
    15: 1500,  # 1,500 EXP required for level 15
    100: 10000 # 10,000 EXP required for level 100
}

# Attack probabilities by level
ATTACK_PROBABILITIES = {
    1: {
        (0, 5): 0.20,   # 20% chance for 0-5 damage
        (6, 10): 0.18,  # 18% chance for 6-10 damage
        (11, 15): 0.15, # 15% chance for 11-15 damage
        (16, 20): 0.10  # 10% chance for 16-20 damage
    },
    5: {
        (0, 5): 0.17,
        (6, 10): 0.20,
        (11, 15): 0.15,
        (16, 20): 0.10
    },
    10: {
        (0, 5): 0.05,
        (6, 10): 0.10,
        (11, 15): 0.17,
        (16, 20): 0.19
    },
    15: {
        (0, 5): 0.05,
        (6, 10): 0.10,
        (11, 15): 0.18,
        (16, 20): 0.20
    },
    100: {
        "fixed_damage": 30  # Fixed 30 damage at level 100
    }
}

# Defense probabilities by level
DEFENSE_PROBABILITIES = {
    1: {
        (0, 5): 0.20,   # 20% chance for 0-5 block
        (6, 10): 0.15,  # 15% chance for 6-10 block
        (11, 15): 0.10  # 10% chance for 11-15 block
    },
    5: {
        (0, 5): 0.15,
        (6, 10): 0.20,
        (11, 15): 0.10
    },
    10: {
        (0, 5): 0.10,
        (6, 10): 0.15,
        (11, 15): 0.20
    },
    15: {
        (0, 5): 0.10,
        (6, 10): 0.15,
        (11, 15): 0.20
    },
    100: {
        "fixed_block": 80  # Fixed 80 block at level 100
    }
}

# EXP gain probabilities
EXERCISE_EXP_PROBABILITIES = {
    (1, 10): 0.30,   # 30% chance for 1-10 EXP
    (11, 20): 0.29,  # 29% chance for 11-20 EXP
    (21, 30): 0.15   # 15% chance for 21-30 EXP
}

# Item settings
ITEMS = {
    "energy_drink": {
        "name": "Energy Drink",
        "description": "Restores 40 Energy points",
        "effect": {"energy": 40},
        "rarity": "common",
        "emoji": "🧃"
    },
    "first_aid_kit": {
        "name": "First Aid Kit",
        "description": "Restores 30 HP points",
        "effect": {"hp": 30},
        "rarity": "common",
        "emoji": "🩹"
    }
}

# Gacha settings
GACHA_COIN_COST = 10
SEARCHING_COOLDOWN = 2 * 60 * 60  # 2 hours in seconds
SEARCHING_PROBABILITIES = {
    "success": 0.80,  # 80% chance to get coins
    "coin_range": (5, 10)  # 5-10 coins when successful
}

# Exercise cooldown (24 hours in seconds)
EXERCISE_COOLDOWN = 24 * 60 * 60
