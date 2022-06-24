"""
Contains the functions called by the FaultBot.

Written by Chris Quartararo

"""

# imports
import discord
import fault_api as api

# Set up logging
import bot.logger
log = bot.logger.setup_logger("./bot/cog_helpers.log", "cog_helpers")


def read_file(path):
    """
    Opens a file and returns the data.
    Returns None if the file is not found.
    """

    try:
        with open(f"{path}", "r") as file:
            file_data = file.read()
        return file_data
    except FileNotFoundError as e:
        log.error(f"Caught error {e}. No file found.")

    return None


def decode_json(json_file):
    """
    Reads a JSON file and returns a python dict.
    If there is an issue decoding the JSON file then a new users dict is started from scratch.
    """

    # If the file is not found, json_file will be None and the dict is started from scratch.
    if json_file == None:
        return {"guild":{}}

    import json

    data = None
    try:
        data = json.loads(json_file)
    except json.decoder.JSONDecodeError as e:
        log.error(f"Caught error {e}. File will be set to default.")
        data = {"guild":{}}

    return data


def write_file(path, data):
    """
    Writes a JSON file with the given data to the given path.
    """

    import json
    with open(f"{path}", "w") as file:
        json_data = json.dumps(data, indent=4)
        file.write(json_data)


def update_dict(users_dict, guild_id, discord_name, fault_name):
    """
    Updates a dictionary with either a new entry for a user.
    Returns a dictionary
    """

    if guild_id not in users_dict["guild"].keys():
        users_dict["guild"][guild_id] = {}

    users_dict["guild"][guild_id][discord_name] = fault_name

    return users_dict


def remove_from_dict(users_dict, guild_id, discord_name):
    """
    Removes a discord user from the users.json dictionary.
    """
    
    if guild_id not in users_dict["guild"].keys():
        log.error("Guild not found when trying to remove user.")
        return
    
    user = users_dict["guild"][guild_id].pop(discord_name, None)

    if user == None:
        log.error(f"KeyError when looking for the user in {guild_id}.")
    
    return users_dict


def get_from_dict(users_dict, guild_id, discord_name):
    """
    Retrieves a Fault user name from the users.json dictionary.
    """
    try:
        user = users_dict["guild"][guild_id].pop(discord_name)
    except KeyError as e:
        user = None
    return user


def match_info(ctx):
    """
    Gets match information for the given user.
    Returns an embedded message to be sent by the FaultBot.
    """
    
    msg_author = ctx.author
    return f"Found user {msg_author}"


def embed_elo(fault_name, elo_title, mmr, ranking, avatar_link):
    """
    Creates an embedded message to send to a discord server.
    """

    colors = {
        "Bronze": 0xD36210,
        "Silver": 0x808080,
        "Gold": 0xFBC02D,
        "Platinum": 0x0FB96D,
        "Diamond": 0x03A9F4,
        "Master": 0x9C27B0
    }

    dict = {
        "color": colors[elo_title],
        "author": {
            "name": f"{fault_name}",
            "icon_url": f"{avatar_link}"
        },
        "fields":[
            {"name": "Rank", "value":f"{elo_title}", "inline":True},
            {"name": "MMR", "value":f"{mmr:.0f}", "inline":True},
            {"name": "Position", "value":f"{ranking}", "inline":True}
        ]
    }

    embed = discord.Embed.from_dict(dict)

    return embed


def embed_match(match_details, id_to_hero, fault_name):
    """
    Create two embeds, one for the winning team and one for the losing team.
    """
    
    colors = {"win":0x00dc04, "lose":0xef0000}

    footer = {"text":f"{match_details['TimeLength']} - id:{match_details['ID']}"}

    team_win = match_details['Winner']
    team_lose = int(not match_details['Winner'])

    embeds_win = []
    embeds_lose = []

    elo_win = 0
    elo_lose = 0
    
    for player in match_details['Players']:

        kda = (player['Kills']+player['Assists'])/player['Deaths']

        fields = []
        fields.append({"name":"ELO", "value":f"{player['MMR']} ({player['MMRChange']})", "inline":True})
        fields.append({"name":"K/D/A", "value":f"{player['Kills']}/{player['Deaths']}/{player['Assists']} ({kda:.1f})", "inline":True})
        fields.append({"name":"CS", "value":f"{player['CS']}", "inline":True})

        author_icon_url = api.get_player_avatar(api.get_user(player['Username']))['avatarURI']
        author_name = f"{player['Username']}"
        if author_name == fault_name:
            author_name += u" U+1F3AE"
        author = {"name":author_name, "icon_url":author_icon_url}

        thumbnail = {"url":api.get_image_hero_portrait(player['HeroID'])}

        title = f"{id_to_hero[player['HeroID']]} - lvl {player['HeroLevel']}"

        if player['Team'] == match_details['Winner']:
            elo_win += player['MMR']
            embeds_win.append({
                "color":colors['win'],
                "author":author,
                "thumbnail":thumbnail,
                "title":title,
                "fields":fields
            })
        else:
            elo_lose += player['MMR']
            embeds_lose.append({
                "color":colors['lose'],
                "author":author,
                "thumbnail":thumbnail,
                "title":title,
                "fields":fields
            })


    elo_win_average = elo_win/(len(match_details['Players'])/2)
    elo_lose_average = elo_lose/(len(match_details['Players'])/2)

    embeds = embeds_win + embeds_lose
    embeds = [discord.Embed.from_dict(x) for x in embeds]

    return embeds