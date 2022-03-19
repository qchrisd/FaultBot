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

    
    def test_embed_match(self):
        match_details = {
                            "id": 123,
                            "winner": 1,
                            "timeLength": "1:00:20",
                            "startDateTime": "date String",
                            "status": 2,
                            "players": 
                            [
                                {
                                    "playerId": 29016,
                                    "username": "qchrisd",
                                    "team": 0,
                                    "heroId": 4,
                                    "mmr": 1200,
                                    "mmrChange": -15
                                },
                                {
                                    "playerId": 6969,
                                    "username": "saxy_beast",
                                    "team": 1,
                                    "heroId": 6,
                                    "mmr": 1100,
                                    "mmrChange": 15
                                }
                            ]
                        }
        id_to_hero = {
            4:"Twinblast",
            6:"Narbash"
        }
        
        expected_winner = {
            "color": 0x00dc04,
            "author":{"name":"Winner"},
            "title": "Team 1 - Average ELO 1100",
            "fields":[
                {"name":"Narbash", "value":"saxy_beast: ELO 1100 (15)", "inline":False}
            ],
            "footer": {"text":"1:00:20 - id:123"}
        }
        expected_winner = discord.Embed.from_dict(expected_winner).to_dict()

        expected_loser = {
            "color": 0xef0000,
            "author":{"name":"Loser"},
            "title": "Team 0 - Average ELO 1200",
            "fields":[
                {"name":"Twinblast", "value":"qchrisd: ELO 1200 (-15)", "inline":False}
            ],
            "footer": {"text":"1:00:20 - id:123"}
        }
        expected_loser = discord.Embed.from_dict(expected_loser).to_dict()
        
        actual_winner, actual_loser = embed_match(match_details, id_to_hero)

        print()
        print(actual_winner.to_dict())
        print(expected_winner)

        self.assertEqual(actual_winner.to_dict(), expected_winner)
        self.assertEqual(actual_loser.to_dict(), expected_loser)


if __name__ == '__main__':
    unittest.main()