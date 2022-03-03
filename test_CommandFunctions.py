"""
Contains unit tests for the CommandFunctions module.
"""

import unittest
from CommandFunctions import update_dict


class TestCommandFunctions(unittest.TestCase):

    def test_update_dict(self):
        actual = update_dict(users_dict = {"guild":{}}, guild_id=123, discord_name="qchrisd#1644", fault_name="qchrisd")
        self.assertEqual(actual, {"guild":{123:{"qchrisd#1644":"qchrisd"}}})


if __name__ == '__main__':
    unittest.main()