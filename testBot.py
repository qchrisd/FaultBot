"""
Test bot to figure out wtf is happening here.
"""

# Regular imports
import os
from dotenv import load_dotenv
import logging

# Discord imports
import discord
from discord.ext import commands
import slash_util

# set up logging and import dotenv details
load_dotenv()
logging.basicConfig(filename="FaultBot.log", format="[%(process)d] %(asctime)s - %(message)s", level=logging.INFO)

# Get dotenv things
TOKEN = os.getenv("DISCORD_TOKEN_DEV")

# Create bot
bot = slash_util.Bot(command_prefix="/")

# Try a cog
class test_cog(slash_util.Cog):

    @slash_util.slash_command(guild_id=740376813120782367)
    async def testing(self, ctx):
        await ctx.send("Command received.")

bot.add_cog(test_cog(bot))

# Run the bot
bot.run(TOKEN)