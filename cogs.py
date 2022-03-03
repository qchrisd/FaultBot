"""
This file contains the cog and commands for the bot.
"""

# Import packages
import os
from dotenv import load_dotenv  # Package titled python-dotenv
import logging

# Import discord stuff
import discord  # v2.0.0 found at (git+https://github.com/Rapptz/discord.py)
import slash_util  # Requires discord.py 2.0.0+

# Import custom modules
import CommandFunctions as functions

# Set up logging
logging.basicConfig(filename="FaultBot.log", format="[%(process)d] %(asctime)s - %(message)s", level=logging.INFO)

# Load the environmental variables from the .env file
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN_DEV')
GUILD = os.getenv('DISCORD_GUILDID_DEV')

# Cog for slash_command()s
class cog_commands(slash_util.Cog):

    @slash_util.slash_command(guild_id=GUILD, name="register")
    async def register_fault_username(self, ctx: slash_util.Context, fault_name: str):
        """
        Registers or updates a discord user's name in a JSON for persistent storage.
        If the JSON is blank or doesn't exist it is created.
        If the JSON exists, it is updated and rewritten.
        """

        guild_id = str(ctx.guild.id)
        discord_name = f"{ctx.author.name}#{ctx.author.discriminator}"

        import json
        try:
            with open("users.json", "r") as file:
                users_json = file.read()
        except FileNotFoundError as e:
            logging.info(f"Caught error {e}. Should throw UnboundLocalError.")
            
        try:
            users_dict = json.loads(users_json)
        except json.decoder.JSONDecodeError as e:
            logging.info(f"Caught error {e}. File will be set to default.")
            users_dict = {"guild":{}}
        except UnboundLocalError as e:
            logging.info(f"Caught error {e}. File users.json will be created.")
            users_dict = {"guild":{}}
        
        new_dict = functions.update_dict(users_dict, guild_id, discord_name, fault_name)

        with open("users.json", "w") as file:
            json_data = json.dumps(new_dict, indent=4)
            file.write(json_data)

        await ctx.send(f"Your Fault username has been updated to {fault_name}. Use this command again if you would like to change it.")


    @slash_util.slash_command(guild_id=GUILD)
    async def send_test_embed(self, ctx):
        # Creating new test embed
        test = discord.Embed(title='This is the first embed', 
            description='this is the \n multiline description **with markdown**',
            color=discord.Color.purple())

        # Test the footer
        test.set_footer(text='Test for a footer')
        test.set_author(name='FaultBot')
        test.add_field(name='test **field**', value='test **value** \n newline')
        test.add_field(name='test *field* 2', value='value 2')
        test.add_field(name='test field 3', value='value 3', inline=False)

        print(test.to_dict())

        # Test sending the embed
        await ctx.send(embed=test)


    @slash_util.slash_command(guild_id=GUILD, name="match")
    async def match_info(self, ctx):
        test_string = functions.match_info(ctx)
        await ctx.send(test_string)