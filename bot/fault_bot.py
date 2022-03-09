"""
This file contains and runs the Discord bot.

Methods include watching for commands and messaging information to users.

Written by Chris Quartararo

"""


# Import packages
import os
from dotenv import load_dotenv  # Package titled python-dotenv

# Import discord stuff
import slash_util  # Requires discord.py 2.0.0+

# Import custom modules
import bot.logger as log
from bot.cogs import UserManagement


# Set up logging
log.setup_info("bot/fault_bot.log")
log.setup_error("bot/fault_bot.log")

# Load the environmental variables from the .env file
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN_DEV')
GUILD = os.getenv('DISCORD_GUILDID_DEV')


# Create the discord bot
bot = slash_util.Bot(command_prefix="/")


# Logging for bot startup functions
@bot.event
async def on_connect():
    """
    Runs when bot is connected to a server.
    """

    log.info(f'{bot.user} has successfully connected to Discord in server {bot.guilds}.')


@bot.event
async def on_ready():
    """
    Runs when the bot is fully functional and is ready to start being a bot.
    """

    log.info(f'{bot.user} is ready to recieve commands.')


# Add the cog to the bot
bot.add_cog(UserManagement(bot))

# Runs the bot
bot.run(TOKEN)

