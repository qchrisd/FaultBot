"""
Unit tests for FaultAPI module.

Written by Chris Quartararo
Last update 2/27/2022

"""

# Imports
import unittest
from unittest.mock import MagicMock

# Import methods
from FaultAPI import _create_pool_manager, _decode_json, get_user, sanitize_fault_user_response
from FaultAPI import _create_hero_dicts

# Test case
class FaultAPIRequestTest(unittest.TestCase):
    def test_create_pool_manager(self):
        import urllib3
        self.assertIsInstance(_create_pool_manager(), urllib3.PoolManager)

    def test_decode_json(self):
        actual = _decode_json(b'{"id":"29016","username":"qchrisd","eloTitle":"Silver","MMR":1223.1,"ranking":1129,"placementGamesRemain":0}')
        self.assertEqual(actual['id'], "29016")

    def test_sanitize_fault_user_response(self):
        actual = sanitize_fault_user_response({"success":False})
        self.assertEqual(actual, -1)

    def test_create_hero_dicts(self):
        actual_hero_to_id, actual_id_to_hero = _create_hero_dicts({"Twinblast":{"Id":2}})
        self.assertEqual(actual_hero_to_id, {"Twinblast":2})
        self.assertEqual(actual_id_to_hero, {2:"Twinblast"})

    """
    def test_get_user(self):
        #actual = get_user("qchrisd", lambda x: {"success": False})
        actual = get_user("qchrisd")
        self.assertEqual(actual) # fail case
    """
# Run testing
if __name__ == '__main__':
    unittest.main()