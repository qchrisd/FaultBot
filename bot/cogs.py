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
import bot.logger
import bot.cog_helpers as helpers
import fault_api as api


# Load the environmental variables from the .env file
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN_DEV')
GUILD = os.getenv('DISCORD_GUILDID_DEV')

# Set up logging
log = bot.logger.setup_logger("./bot/fault_bot.log", "cogs")


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

        # Log
        log.info(f"Registering {discord_name}")

        users_json = helpers.read_file("./bot/users.json")
            
        users_dict = helpers.decode_json(users_json)

        fault_user = api.get_user(fault_name)

        if fault_user == None:
            await ctx.send(f"Sorry, I couldn't find **{fault_name}**. Check your spelling and try again.")
            log.error(f"Failed to find {fault_name}.")
            return
        
        new_dict = helpers.update_dict(users_dict, guild_id, discord_name, fault_user)

        helpers.write_file("./bot/users.json", new_dict)

        # Send confirmation of completion to the messenger
        await ctx.send(f"Your Fault username has been updated to **{fault_user['username']}** (id: {fault_user['id']}). Use this command again if you would like to change it.")


    @slash_util.slash_command(guild_id=GUILD, name="unregister", description="Remove all Fault usernames associated with your discord user.")
    async def unregister_fault_username(self, ctx: slash_util.Context):
        """
        Removes all Fault usernames from the users.json file based on the discord user.
        """
        # Some easy variables
        guild_id = str(ctx.guild.id)
        discord_name = f"{ctx.author.name}#{ctx.author.discriminator}"

        # Log
        log.info(f"Unregistering {discord_name}.")

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

        # Log
        log.info(f"Getting Fault user for {discord_name}.")

        users_json = helpers.read_file("./bot/users.json")

        users_dict = helpers.decode_json(users_json)

        user = helpers.get_from_dict(users_dict, guild_id, discord_name)

        if user == None:
            await ctx.send("There is no Fault name registered to your discord name.")
            log.error(f"Failed to find {user['username']} in users.json.")
        else:
            await ctx.send(f"Your registered Fault user name is **{user['username']}** (id: {user['id']}).")



# Cog for stats commands
class GameStats(slash_util.Cog):

    @slash_util.slash_command(guild_id=GUILD, name="elo", description="Look at your player MMR and rank.")
    async def elo(self, ctx, fault_name: str=None):
        """
        Gets ELO for a player and sends an embed with the info.
        """

        if fault_name == None:
            guild_id = str(ctx.guild.id)
            discord_name = f"{ctx.author.name}#{ctx.author.discriminator}"

            users_json = helpers.read_file("./bot/users.json")

            users_dict = helpers.decode_json(users_json)

            user = helpers.get_from_dict(users_dict, guild_id, discord_name)

            # Log
            log.info(f"Getting elo for {discord_name}.")

            if user == None:
                await ctx.send(f"I couldn't find any registered Fault user name for {discord_name} user. Try using /register to save one.")
                log.error(f"Failed to find user {discord_name} in users.json.")
                return
        
        else:
            user = api.get_user(fault_name)

            if user == None:
                await ctx.send(f"I couldn't find {fault_name}. Check your spelling and try again.")
                log.error(f"Failed to get user {fault_name} from Fault website.")
                return

        user_elo = api.get_elo(user)

        avatar_link = api.get_player_avatar(user)

        embed_message = helpers.embed_elo(user['username'], user_elo['eloTitle'], user_elo['MMR'], user_elo['ranking'], avatar_link['avatarURI'])

        # Adds rank image to embed. This uploads the image every time.
        # TODO figure out how to use a CDN to be able to pass a url and not upload images for every call
        rank_image = discord.File(f"./assets/icons_rank/{user_elo['eloTitle']}.png", filename=f"{user_elo['eloTitle']}.png")
        embed_message.set_thumbnail(url=f"attachment://{user_elo['eloTitle']}.png")

        await ctx.send(embed=embed_message, file=rank_image)


    @slash_util.slash_command(guild_id=GUILD, name="match", description="Get match information.")
    async def match(self, ctx, fault_name:str = None, number:int = None, match_id:str = None):
        """
        Gets match information for a given user or registered user.
        Currently supports only one match.
        """

        if fault_name == None:
            guild_id = str(ctx.guild.id)
            discord_name = f"{ctx.author.name}#{ctx.author.discriminator}"

            users_json = helpers.read_file("./bot/users.json")

            users_dict = helpers.decode_json(users_json)

            user = helpers.get_from_dict(users_dict, guild_id, discord_name)

            # Log
            log.info(f"Getting elo for {discord_name}.")

            if user == None:
                await ctx.send(f"I couldn't find any registered Fault user name for {discord_name} user. Try using /register to save one.")
                log.error(f"Failed to find user {discord_name} in users.json.")
                return

        else:
            user = api.get_user(fault_name)

            if user == None:
                await ctx.send(f"I couldn't find {fault_name}. Check your spelling and try again.")
                log.error(f"Failed to get user {fault_name} from Fault website.")
                return
        
        match = api.get_matches(user)
        _, id_to_hero = api.get_hero_dicts()

        embed_win, embed_lose = helpers.embed_match(match, id_to_hero)

        await ctx.send(embeds=[embed_win, embed_lose])
