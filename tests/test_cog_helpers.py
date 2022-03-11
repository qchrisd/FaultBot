"""
Contains unit tests for the CommandFunctions module.
"""

import unittest
import unittest.mock as mock
from bot.cog_helpers import (read_file, 
                             update_dict, 
                             remove_from_dict,
                             get_from_dict,
                             embed_elo)


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


if __name__ == '__main__':
    unittest.main()