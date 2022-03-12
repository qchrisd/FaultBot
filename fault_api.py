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
    Returns None if unsuccessful.
    """

    if page_dict['success']:
        user = page_dict['players'][0]
    else:
        user = None
    
    return user


## Main
def get_hero_play_stats():
    """
    Gets the stats per hero in the format https://api.playfault.com/getStatsPerHero
    Returns a JSON object with the HeroID as the key.
    
    JSON
    {
        "heroes": {
            "{heroName}": {
                "wins": 0,
                "games": 0,
                "averageGameTime": "string",
                "averageLevel": 0,
                "kills": 0,
                "deaths": 0,
                "assists": 0,
                "damage": 0,
                "damageTaken": 0,
                "gold": 0,
                "pickRate": 0.0,
                "winRate": 0.0,
                "kda": 0.0,
                "killsPerMin": 0.0,
                "deathsPerMin": 0.0,
                "assistsPerMin": 0.0,
                "damagePerMin": 0.0,
                "damageTakenPerMin": 0.0,
                "goldPerMin": 0.0,
                "Id": 0
            }
        }
    }
    """

    page_link = 'https://api.playfault.com/getStatsPerHero'
    page_dict = _query_website(page_link)
    
    return page_dict['heroes']


def get_hero_dicts(hero_stats = get_hero_play_stats()):

    """Creates a dictionary with the hero ID as keys and their names as values"""
    
    hero_to_id = {}
    id_to_hero = {}

    for key, val in hero_stats.items():
        id_to_hero[val["Id"]] = key
        hero_to_id[key] = val["Id"]
    
    return hero_to_id, id_to_hero


def get_user(fault_username):
    """
    Gets the usernames and IDs of fault users given a search string.
    Returns a dict.

    JSON
    [
        {
            "id": 0,
            "username": "string"
        }
    ]
    """

    page_link = f"https://api.playfault.com/searchUsers/{fault_username}"
    user = _query_website(page_link)
    
    try:
        user = user[0]
    except TypeError as e:
        user = None
    except IndexError as e:
        user = None

    return user


def get_top_players(user):
    """ 
    TODO update this method to be useful
    OLD GET_USERS() METHOD. NEEDS REWORK FOR TOP PLAYERS LIST
    Returns a player's information from a username as a dict.
    Returns None if the username is not found.

    JSON
    {
        "success": true,
        "players": 
        [
            {
                "rank": 0,
                "id": 0,
                "name": "string",
                "elo": 0.0,
                "eloType": "string",
                "winRate": 0.0,
                "totalGames": 0,
                "totalKills": 0,
                "totalDeaths": 0,
                "totalAssists": 0,
                "mostPlayedHeroes": 
                [
                    {
                        "HeroID": 0,
                        "Count": 0
                    },
                    {
                        "HeroID": 0,
                        "Count": 0
                    }
                ]
            }
        ]
    }
    """
    
    page_link = f'https://api.playfault.com/getTopPlayers/1/{user}'
    page_dict = _query_website(page_link)
    
    user = _check_user_request_response(page_dict)

    return user


def get_user_id(user, get_user_fn=get_user):
    """
    TODO evaluate if this method needs to be here
    Returns a player's ID given a username.
    """

    user = get_user_fn(user)
    if user == None:
        return user
    
    return user["id"]


def get_hero_info(hero):
    """
    Gets the information for a given hero.

    {
        "info": {
            "basicRange": "string",
            "niche": "string",
            "role": "string",
            "damageType": "string",
            "description": "string"
        },
        "health": 0,
        "healthPerLevel": 0,
        "healthRegen": 0,
        "healthRegenPerLevel": 0,
        "mana": 0,
        "manaPerLevel": 0,
        "manaRegen": 0,
        "manaRegenPerLevel": 0,
        "physicalArmor": 0,
        "physicalArmorPerLevel": 0,
        "energyArmor": 0,
        "energyArmorPerLevel": 0,
        "movespeed": 0,
        "lmb": {
            "name": "string",
            "description": "string",
            "anyOtherAttribute": 0
        },
        "rmb": {
            "name": "string",
            "description": "string",
            "anyOtherAttribute": 0
        },
        "q": {
            "name": "string",
            "description": "string",
            "anyOtherAttribute": 0
        },
        "e": {
            "name": "string",
            "description": "string",
            "anyOtherAttribute": 0
        },
        "r": {
            "name": "string",
            "description": "string",
            "anyOtherAttribute": 0
        },
        "p": {
            "name": "string",
            "description": "string",
            "anyOtherAttribute": 0
        }
    }
    """

    page_link = f"https://api.playfault.com/heroData/{hero}"
    page_json = _query_website(page_link)

    return page_json


def get_items():
    """
    Gets the list of items from the website.
    Returns a dict.

    {
        "id": 
        {
            "id": 0,
            "name": "string",
            "parents": 
            [
                0
            ],
            "children": 
            [
                0
            ],
            "treeId": 0,
            "attributes": 
            [
                {
                    "AttributeName": "string",
                    "Value": 0,
                    "RankValue": 0,
                    "UIDetails": "string"
                }
            ],
            "passive": "string",
            "active": "string",
            "cost": "string",
            "color": "string"
        }
    }
    """

    # Gets information from the website
    items_link = "https://api.playfault.com/items"
    items = _query_website(items_link)

    return items


def get_aspects():
    """
    Gets the list of aspects.
    Returns a dict.

    [
        {
            "name": "string",
            "color": "string",
            "effect1": "string",
            "effect2": "string"
        }
    ]
    """

    # Gets information from the website
    aspects_link = "https://api.playfault.com/aspects"
    aspects = _query_website(aspects_link)

    return aspects


def get_matches(user, n = 1):
    """
    Gets the last match for a given player.
    Returns  None if no matches were found.

    {
        "success": true,
        "matches": 
        [
            {
                "id": 0,
                "winner": 0,
                "timeLength": "string",
                "startDateTime": "string",
                "status": 0,
                "players": 
                [
                    {
                        "playerId": 0,
                        "team": 0,
                        "heroId": 0,
                        "heroLevel": 0,
                        "kills": 0,
                        "deaths": 0,
                        "assists": 0,
                        "heroDamage": 0,
                        "damageTaken": 0,
                        "gold": 0,
                        "card1": 0,
                        "card2": 0,
                        "item1": 0,
                        "item2": 0,
                        "item3": 0,
                        "item4": 0,
                        "item5": 0,
                        "item6": 0,
                        "cs": 0,
                        "username": "string",
                        "mmr": 0,
                        "mmrChange": 0
                    }
                ]
            }
        ]
    }
    """
    
    # Check if the user is good
    if user == None:
        return user
    else:
        user_id = user["ID"]

    page_link = f'https://api.playfault.com/getMatches/{user_id}/{n}'
    page_dict = _query_website(page_link)
    match = page_dict["matches"][0]

    return match


def get_match_data(match_id):
    """
    Gets match data from the website.
    Returns a dict.

    {
        "id": 0,
        "winner": 0,
        "timeLength": "string",
        "startDateTime": "string",
        "status": 0,
        "players": 
        [
            {
                "playerId": 0,
                "team": 0,
                "heroId": 0,
                "heroLevel": 0,
                "kills": 0,
                "deaths": 0,
                "assists": 0,
                "heroDamage": 0,
                "damageTaken": 0,
                "gold": 0,
                "card1": 0,
                "card2": 0,
                "item1": 0,
                "item2": 0,
                "item3": 0,
                "item4": 0,
                "item5": 0,
                "item6": 0,
                "cs": 0,
                "username": "string",
                "mmr": 0,
                "mmrChange": 0
            }
        ]
    }
    """

    page_link = f'https://api.playfault.com/getMatchData/{match_id}'
    match = _query_website(page_link)

    return match


def get_player_hero_stats(user):
    """
    Gets hero statistics for a specified user.
    Returns None if the player is not found.

    {
        "heroes": 
        {
            heroID: 
            {
                "wins": 0,
                "games": 0,
                "kills": 0,
                "deaths": 0,
                "assists": 0
            }
        }
    }
    """

    # Check if the user is good
    if user == None:
        return user
    else:
        user_id = user["id"]
    
    # Collect info from Fault website and convert json to dict
    page_link = f'https://api.playfault.com/getPlayerHeroStats/{user_id}'
    page_dict = _query_website(page_link)
    player_hero_stats = page_dict["heroes"]

    return player_hero_stats


def get_elo(user):
    """
    Gets the MMR and ELO information for an ID. 
    Returns None if no user is found

    JSON
    {
        "id": 0,
        "username": "string",
        "eloTitle": "string",
        "MMR": 0,
        "ranking": 0,
        "placementGamesRemain": 0
    }
    """

    # Check if the user is good
    if user == None:
        return user
    else:
        user_id = user["id"]

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


def get_player_avatar(user):
    """
    Gets the avatar of the given user.
    Returns a dict with avatarId and avatarURI

    {
        "avatarId": 0,
        "avatarURI": "https://api.playfault.com/imagecdn/avatars/{avatarId}.jpg"
    }
    """

    if user == None:
        return None

    page_link = f"https://api.playfault.com/userAvatar/{user['id']}"
    page_json = _query_website(page_link)

    return page_json


if __name__ == '__main__':
    print("File called directly.")
    _startup()
    print(get_user("bbbbbbbbb"))
else:
    _startup()