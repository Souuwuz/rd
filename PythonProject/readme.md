# Mortem House Stat - Discord RPG Bot

A Discord RPG bot offering immersive gameplay with combat mechanics, character progression, inventory management, and gacha-style item collection.

## Features

- **Player Profiles**: Display HP, Energy, Level, and EXP
- **Combat System**: Attack other players and defend yourself
- **Inventory Management**: Collect and use items
- **Gacha System**: Roll for new items using gacha coins
- **Admin Commands**: Special commands for server moderators

## Bot Commands

All commands use the prefix `Statbot!`

### Profile Commands
- `Statbot!profile` - View your profile
- `Statbot!profile @username` - View another user's profile
- `Statbot!exercise` - Exercise once per day to gain EXP

### Combat Commands
- `Statbot!attack @username` - Attack another user

### Inventory Commands
- `Statbot!inventory` - View your inventory
- `Statbot!use [item name]` - Use an item from your inventory

### Gacha Commands
- `Statbot!gacha` - Roll the gacha (costs 10 coins)
- `Statbot!searching` - Search for gacha coins (2 hour cooldown)

### Admin Commands
- `Statbot!heal @username` - Fully restore a user's HP and Energy (healing role only)
- `Statbot!grantexp @username [amount]` - Grant EXP to a user (moderator+ only)
- `Statbot!grantrole @role` - Add a role to authorized roles (owner only)
- `Statbot!grantmodrole @role` - Add a role to moderator roles (owner only)
- `Statbot!revokerole @role` - Remove a role from authorized roles (owner only)
- `Statbot!revokemodrole @role` - Remove a role from moderator roles (owner only)

## Setup for 24/7 Uptime

To ensure your bot stays online 24/7, follow these steps:

1. **Enable Replit Always On**:
   - In your Replit project, click on "Tools" in the left sidebar
   - Select "Always On" 
   - Toggle the switch to enable

2. **Use an External Uptime Service**:
   - Sign up for a free account at [UptimeRobot](https://uptimerobot.com/)
   - Add a new HTTP(s) monitor 
   - Enter your Replit URL: `https://[your-repl-name].[your-username].repl.co/status`
   - Set the monitoring interval to 5 minutes

## Troubleshooting

If your bot goes offline:

1. Check that the DISCORD_BOT_TOKEN is still valid
2. Verify the Replit is running (green "Running" indicator)
3. Check UptimeRobot for any downtime alerts
4. Restart the Replit project

## Important Links

- Discord Developer Portal: https://discord.com/developers/applications
- UptimeRobot: https://uptimerobot.com/
- Discord.py Documentation: https://discordpy.readthedocs.io/