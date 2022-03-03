"""
Contains unit tests for the CommandFunctions module.
"""

import unittest
from CommandFunctions import register_fault_username


class TestCommandFunctions(unittest.TestCase):

    def test_register_fault_username(self):
        actual = register_fault_username(discord_name="qchrisd#1644", fault_name="qchrisd")
        self.assertEqual(actual, {"qchrisd#1644":"qchrisd"})


if __name__ == '__main__':
    unittest.main()