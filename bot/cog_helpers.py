"""
Contains the functions called by the FaultBot.

Written by Chris Quartararo

"""

import bot.logger as log


def read_file(path):
    """
    Opens a file and returns the data.
    Returns -1 if the file is not found.
    """

    try:
        with open(f"{path}", "r") as file:
            file_data = file.read()
        return file_data
    except FileNotFoundError as e:
        log.error(f"Caught error {e}. No file found.")

    return -1


def decode_json(json_file):
    """
    Reads a JSON file and returns a python dict.
    If there is an issue decoding the JSON file then a new users dict is started from scratch.
    """

    # If the file is not found, json_file will be -1 and the dict is started from scratch.
    if json_file == -1:
        return {"guild":{}}

    import json

    data = -1
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
    
    user = users_dict["guild"][guild_id].pop(discord_name, -1)

    if user == -1:
        log.error(f"KeyError when looking for the user in {guild_id}.")
    
    return users_dict


def match_info(ctx):
    """
    Gets match information for the given user.
    Returns an embedded message to be sent by the FaultBot.
    """
    
    msg_author = ctx.author
    return f"Found user {msg_author}"