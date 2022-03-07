''' 
Fault Public API
Written by: Chris Quartararo

This file is a list of all the fault website API links for reference.
When imported it will return dictionaries of these useful things.

The current functionality allows for the following methods:
- Getting a player ID by username
- Get the previous matches of a player
- Get the hero performance data for a player
- Get the MMR/ELO information for a player
- Get item list

To Do:
- hero win statistics and pick rates
- Document aspect labels

Last Update: 3/1/2022

'''


## Import dependencies
import urllib3
import json


## Utilities
def _decode_json(json_data):
    """
    Decodes json binary data and returns a dictionary.
    """
    
#    try:
    dict = json.loads(json_data)
    """    
    except:
        dict = json.loads(json_data.decode('utf8'))
    """
    return dict


def _query_website(url):
    """
    Returns a JSON object from a website query.
    """

    http = _create_pool_manager()
    page = http.request("GET", url)
    page_data = page.data
    page_json = _decode_json(page_data)

    return page_json


def _create_pool_manager():
    """
    Creates a pool manager for website queries.
    """

    return urllib3.PoolManager()


def _startup():
    """
    Creates global variables.
    """

    pass


def _check_user_request_response(page_dict):
    """
    Check to see if the request for a player was successful.
    Returns the user JSON if successful.
    Returns -1 if unsuccessful.
    """

    if page_dict['success']:
        user = page_dict['players'][0]
    else:
        user = -1
    
    return user


## Main
def get_hero_play_stats(query_website_fn=_query_website):
    """
    Gets the stats per hero in the format https://api.playfault.com/getStatsPerHero
    Returns a JSON object with the HeroID as the key
    """

    page_link = 'https://api.playfault.com/getStatsPerHero'
    page_dict = query_website_fn(page_link)
    
    return page_dict['heroes']


def get_hero_dicts(hero_stats = get_hero_play_stats()):

    """Creates a dictionary with the hero ID as keys and their names as values"""
    
    hero_to_id = {}
    id_to_hero = {}

    for key, val in hero_stats.items():
        id_to_hero[val["Id"]] = key
        hero_to_id[key] = val["Id"]
    
    return hero_to_id, id_to_hero


def get_user(fault_username, query_website_fn=_query_website):
    """
    Gets the usernames and IDs of fault users given a search string.
    Returns a dict.
    """

    page_link = f"https://api.playfault.com/searchUsers/{fault_username}"
    user = query_website_fn(page_link)
    
    try:
        user = user[0]
    except IndexError as e:
        print(user)
        user = -1

    return user


def get_top_players(user, query_website_fn=_query_website):
    """ 
    OLD GET_USERS() METHOD. NEEDS REWORK FOR TOP PLAYERS LIST
    Returns a player's information from a username as a dict.
    Returns -1 if the username is not found.
    """
    
    page_link = f'https://api.playfault.com/getTopPlayers/1/{user}'
    page_dict = query_website_fn(page_link)
    
    user = _check_user_request_response(page_dict)

    return user


def get_user_id(user, get_user_fn=get_user):
    """
    Returns a player's ID given a username.
    """

    user = get_user_fn(user)
    if user == -1:
        return user
    
    return user["id"]


def get_hero_info(hero, query_website_fn=_query_website):
    """
    Gets the information for a given hero.
    """

    page_link = f"https://api.playfault.com/heroData/{hero}"
    page_json = query_website_fn(page_link)

    return page_json


def get_items(query_website_fn=_query_website):
    """
    Gets the list of items from the website.
    Returns a dict.
    """

    # Gets information from the website
    items_link = "https://api.playfault.com/items"
    items = query_website_fn(items_link)

    return items


def get_aspects(query_website_fn=_query_website):
    """
    Gets the list of aspects.
    Returns a dict.
    """

    # Gets information from the website
    aspects_link = "https://api.playfault.com/aspects"
    aspects = query_website_fn(aspects_link)

    return aspects


def get_matches(user, n = 1, query_website_fn=_query_website):
    """
    Gets the last match for a given player.
    Returns  -1 if no matches were found.
    """
    
    user_id = user["ID"]

    # Check if the ID is good
    if user_id == -1:
        return user_id

    page_link = f'https://api.playfault.com/getMatches/{user_id}/{n}'
    page_dict = query_website_fn(page_link)
    match = page_dict["matches"][0]

    return match


def get_match_data(match_id, query_website_fn):
    """
    Gets match data from the website.
    Returns a dict.
    """

    page_link = f'https://api.playfault.com/getMatchData/{match_id}'
    match = query_website_fn(page_link)

    return match


def get_player_hero_stats(user):
    """
    Gets hero statistics for a specified user.
    Returns -1 if the player is not found.
    """

    user_id = user["ID"]

    if user_id == -1:
        return user_id
    
    # Collect info from Fault website and convert json to dict
    page_link = f'https://api.playfault.com/getPlayerHeroStats/{user_id}'
    page_dict = _query_website(page_link)
    player_hero_stats = page_dict["heroes"]

    return player_hero_stats


def get_elo(user):
    """
    Gets the MMR and ELO information for an ID. 
    Returns a dict.
    Returns -1 if no user is found
    """

    user_id = user["ID"]

    if user_id == -1:
        return user_id

    # Gets the information from the website
    page_link = f'https://api.playfault.com/getEloData/{user_id}'
    page_json = _query_website(page_link)

    return page_json


## Image API
def get_image_hero_ability(hero, ability):
    """
    Gets the image of a hero ability.
    Returns a png.
    TODO
    """

    image_link = f"https://api.playfault.com/imagecdn/abilities/{hero}/{ability}.png"


def get_image_item(item_id):
    """
    Gets the image of a hero ability.
    Returns a jpg.
    TODO
    """

    image_link = f"https://api.playfault.com/imagecdn/items/{item_id}.jpg"


def get_image_hero_portrait(hero_id):
    """
    Gets the image of a hero ability.
    Returns a jpg.
    TODO
    """

    image_link = f"https://api.playfault.com/imagecdn/portraits/{hero_id}.jpg"



if __name__ == '__main__':
    print("File called directly.")
    _startup()
    print(get_user("bbbbbbbbb"))
else:
    _startup()