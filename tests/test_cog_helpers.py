"""
Contains unit tests for the CommandFunctions module.
"""

import unittest
from bot.cog_helpers import update_dict, remove_from_dict


class TestCommandFunctions(unittest.TestCase):

    def test_update_dict(self):
        actual = update_dict(users_dict = {"guild":{}}, guild_id=123, discord_name="qchrisd#1644", fault_name="qchrisd")
        self.assertEqual(actual, {"guild":{123:{"qchrisd#1644":"qchrisd"}}})


    def test_remove_from_dict(self):
        actual = remove_from_dict(users_dict = {"guild":{123:{"qchrisd#1644":"qchrisd"}}}, guild_id=123, discord_name="qchrisd#1644")
        self.assertEqual(actual, {"guild":{123:{}}})

if __name__ == '__main__':
    unittest.main()