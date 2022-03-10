"""
This file contains the cog and commands for the bot.
"""

# Import packages
import os
from dotenv import load_dotenv  # Package titled python-dotenv

# Import discord stuff
import discord  # v2.0.0 found at (git+https://github.com/Rapptz/discord.py)
import slash_util  # Requires discord.py 2.0.0+

# Import custom modules
import bot.logger as log  # logging.info is set up by the fault_bot module
import bot.cog_helpers as helpers
import fault_api as api


# Load the environmental variables from the .env file
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN_DEV')
GUILD = os.getenv('DISCORD_GUILDID_DEV')

# Cog for user slash_command()s
class UserManagement(slash_util.Cog):

    @slash_util.slash_command(guild_id=GUILD, name="register", description="Associate or change a Fault username with your discord user.")
    async def register_fault_username(self, ctx: slash_util.Context, fault_name: str):
        """
        Registers or updates a discord user's name in a JSON for persistent storage.
        If the JSON is blank or doesn't exist it is created.
        If the JSON exists, it is updated and rewritten.
        """

        # Some variables for easy access
        guild_id = str(ctx.guild.id)
        discord_name = f"{ctx.author.name}#{ctx.author.discriminator}"

        users_json = helpers.read_file("./bot/users.json")
            
        users_dict = helpers.decode_json(users_json)
        
        new_dict = helpers.update_dict(users_dict, guild_id, discord_name, fault_name)

        helpers.write_file("./bot/users.json", new_dict)

        # Send confirmation of completion to the messenger
        await ctx.send(f"Your Fault username has been updated to {fault_name}. Use this command again if you would like to change it.")


    @slash_util.slash_command(guild_id=GUILD, name="unregister", description="Remove all Fault usernames associated with your discord user.")
    async def unregister_fault_username(self, ctx: slash_util.Context):
        """
        Removes all Fault usernames from the users.json file based on the discord user.
        """
        # Some easy variables
        guild_id = str(ctx.guild.id)
        discord_name = f"{ctx.author.name}#{ctx.author.discriminator}"

        users_json = helpers.read_file("./bot/users.json")

        users_dict = helpers.decode_json(users_json)

        new_dict = helpers.remove_from_dict(users_dict, guild_id, discord_name)

        helpers.write_file("./bot/users.json", new_dict)

        # Send confirmation of completion to messenger
        await ctx.send(f"Your Fault user names have been forgotten. User /register to add a new Fault user name.")


    @slash_util.slash_command(guild_id=GUILD, name="show_username", description="Display the Fault username that is registered to your discord user.")
    async def show_username(self, ctx: slash_util.Context):
        """
        Sends the user name that is registered to the messenger.
        """
        
        # Some easy variables
        guild_id = str(ctx.guild.id)
        discord_name = f"{ctx.author.name}#{ctx.author.discriminator}"

        users_json = helpers.read_file("./bot/users.json")

        users_dict = helpers.decode_json(users_json)

        user = helpers.get_from_dict(users_dict, guild_id, discord_name)

        if user == -1:
            await ctx.send("There is no Fault name registered to your discord name.")
        else:
            await ctx.send(f"Your registered Fault user name is {user}")


    """
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
        """


# Cog for stats commands
class GameStats(slash_util.Cog):

    @slash_util.slash_command(guild_id=GUILD, name="elo", description="Look at your player MMR and rank.")
    async def elo(self, ctx):
        pass