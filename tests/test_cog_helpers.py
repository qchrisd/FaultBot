"""
Contains unit tests for the CommandFunctions module.
"""

import unittest
import unittest.mock as mock
import discord
from bot.cog_helpers import (read_file, 
                             update_dict, 
                             remove_from_dict,
                             get_from_dict,
                             embed_elo,
                             embed_match)


class TestCogHelpers(unittest.TestCase):


    def test_read_file(self):
        # Found file
        with mock.patch("bot.cog_helpers.open", mock.mock_open(read_data='{"guild":{}}')):
            actual = read_file("./bot/users.json")
        self.assertEqual(actual, '{"guild":{}}')
        # Did not find file
        actual = read_file("")
        self.assertEqual(actual, None)


    @unittest.skip("No test written")
    def test_decode_json(self):
        pass


    @unittest.skip("no test written")
    def test_write_file(self):
        pass


    def test_update_dict(self):
        actual = update_dict(users_dict = {"guild":{}}, guild_id=123, discord_name="qchrisd#1644", fault_name="qchrisd")
        self.assertEqual(actual, {"guild":{123:{"qchrisd#1644":"qchrisd"}}})


    def test_remove_from_dict(self):
        actual = remove_from_dict(users_dict = {"guild":{123:{"qchrisd#1644":"qchrisd"}}}, guild_id=123, discord_name="qchrisd#1644")
        self.assertEqual(actual, {"guild":{123:{}}})


    def test_get_from_dict(self):
        users_dict = {"guild":{123:{"qchrisd#1644":{"id":29016, "username":"qchrisd"}}}}
        actual = get_from_dict(users_dict, guild_id=123, discord_name= "qchrisd#1644")
        self.assertEqual(actual, {"id":29016, "username":"qchrisd"})


    def test_embed_elo(self):
        fault_name = "qchrisd"
        elo_title = "Silver"
        mmr = 1200
        ranking = 222
        avatar_link = "avatar.link"

        expected = {
        "color": 0x808080,
        "author": {
            "name":f"{fault_name}",
            "icon_url":f"{avatar_link}"
        },
        "fields":[
            {"name": "Rank", "value":f"{elo_title}", "inline":True},
            {"name": "MMR", "value":f"{mmr:.0f}", "inline":True},
            {"name": "Position", "value":f"{ranking}", "inline":True}
        ]
        }

        actual = embed_elo(fault_name, elo_title, mmr, ranking, avatar_link)

        self.assertEqual(actual.to_dict(), expected)

    
    @mock.patch("fault_api.get_player_avatar", return_value="https://api.playfault.com/imagecdn/avatars/21034.jpg")
    @mock.patch("fault_api.get_image_hero_portrait", return_value = "https://api.playfault.com/imagecdn/portraits/6.jpg")
    def test_embed_match(self, mock_get_player_avatar, mock_hero_avatar):
        match_details = {
                            "ID": 123,
                            "Winner": 1,
                            "TimeLength": "1:00:20",
                            "StartDateTime": "date String",
                            "Status": 2,
                            "Players": 
                            [
                                {
                                    "PlayerID": 29016,
                                    "Username": "qchrisd",
                                    "Team": 0,
                                    "HeroID": 4,
                                    "MMR": 1200,
                                    "MMRChange": -15,
                                    "HeroLevel": 14,
                                    "Kills":3,
                                    "Deaths":10,
                                    "Assists":2,
                                    "CS":34
                                },
                                {
                                    "PlayerID": 6969,
                                    "Username": "saxy_beast",
                                    "Team": 1,
                                    "HeroID": 6,
                                    "MMR": 1100,
                                    "MMRChange": 15,
                                    "Kills":7,
                                    "Deaths":2,
                                    "Assists":3,
                                    "CS":96,
                                    "HeroLevel":15
                                }
                            ]
                        }
        id_to_hero = {
            4:"Twinblast",
            6:"Narbash"
        }
        
        expected_winner = {
            "color": 0x00dc04,
            "author":{"name":"saxy_beast", "icon_url":"https://api.playfault.com/imagecdn/avatars/21034.jpg"},
            "title": "Narbash - lvl 15",
            "thumbnail": {"url":"https://api.playfault.com/imagecdn/portraits/6.jpg"},
            "fields":[
                {"name":"ELO", "value":"1100 (15)", "inline":True},
                {"name":"K/D/A", "value":"7/2/3 (5.0)", "inline":True},
                {"name":"CS", "value":"96", "inline":True}
            ],
            "footer": {"text":"1:00:20 - id:123"}
        }
        expected_winner = discord.Embed.from_dict(expected_winner).to_dict()

        expected_loser = {
            "color": 0xef0000,
            "author":{"name":"qchrisd", "icon_url":"https://api.playfault.com/imagecdn/avatars/21034.jpg"},
            "title": "Twinblast - lvl 14",
            "thumbnail": {"url":"https://api.playfault.com/imagecdn/portraits/6.jpg"},
            "fields":[
                {"name":"ELO", "value":"1200 (-15)", "inline":True},
                {"name":"K/D/A", "value":"3/10/2 (0.5)", "inline":True},
                {"name":"CS", "value":"34", "inline":True},
            ],
            "footer": {"text":"1:00:20 - id:123"}
        }
        expected_loser = discord.Embed.from_dict(expected_loser).to_dict()

        expected_embeds = [expected_winner, expected_loser]
        
        actual_embeds = embed_match(match_details, id_to_hero)
        actual_embeds = [discord.Embed.to_dict(x) for x in actual_embeds]

        self.assertEqual(actual_embeds, expected_embeds)


if __name__ == '__main__':
    unittest.main()