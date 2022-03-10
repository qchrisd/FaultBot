"""
Contains unit tests for the CommandFunctions module.
"""

import unittest
import unittest.mock as mock
from bot.cog_helpers import (read_file, 
                             update_dict, 
                             remove_from_dict,
                             get_from_dict)


class TestCogHelpers(unittest.TestCase):


    def test_read_file(self):
        # Found file
        with mock.patch("bot.cog_helpers.open", mock.mock_open(read_data='{"guild":{}}')):
            actual = read_file("./bot/users.json")
        self.assertEqual(actual, '{"guild":{}}')
        # Did not find file
        actual = read_file("")
        self.assertEqual(actual, None)


    def test_update_dict(self):
        actual = update_dict(users_dict = {"guild":{}}, guild_id=123, discord_name="qchrisd#1644", fault_name="qchrisd")
        self.assertEqual(actual, {"guild":{123:{"qchrisd#1644":"qchrisd"}}})


    def test_remove_from_dict(self):
        actual = remove_from_dict(users_dict = {"guild":{123:{"qchrisd#1644":"qchrisd"}}}, guild_id=123, discord_name="qchrisd#1644")
        self.assertEqual(actual, {"guild":{123:{}}})


    def test_get_from_dict(self):
        users_dict = {"guild":{123:{"qchrisd#1644":"qchrisd"}}}
        actual = get_from_dict(users_dict, guild_id=123, discord_name= "qchrisd#1644")
        self.assertEqual(actual, "qchrisd")



if __name__ == '__main__':
    unittest.main()