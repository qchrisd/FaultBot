"""
Unit tests for FaultAPI module.

Written by Chris Quartararo
Last update 2/27/2022

"""

# Imports
import unittest
from unittest.mock import MagicMock

# Import methods
from fault_api import _create_pool_manager, _decode_json, _check_user_request_response, get_match_data
from fault_api import get_hero_play_stats, get_hero_dicts, get_user, get_user_id, get_hero_info, get_items, get_aspects

# Test case
class FaultAPIRequestTest(unittest.TestCase):
    
    def test_decode_json(self):
        actual = _decode_json(b'{"id":"29016","username":"qchrisd","eloTitle":"Silver","MMR":1223.1,"ranking":1129,"placementGamesRemain":0}')
        self.assertEqual(actual['id'], "29016")
    

    def test_create_pool_manager(self):
        import urllib3
        self.assertIsInstance(_create_pool_manager(), urllib3.PoolManager)


    def test_check_user_request_response(self):
        # Success case
        actual_success = _check_user_request_response({"success":True, "players":{0:{"id":29016}}})
        self.assertEqual(actual_success, {"id":29016})
        # Fail case
        actual_failure = _check_user_request_response({"success":False})
        self.assertEqual(actual_failure, -1)


    def test_get_hero_play_stats(self):
        test_fn = lambda _:{"heroes": {"Twinblast": {"wins": 2204}}}
        actual = get_hero_play_stats(query_website_fn=test_fn)
        self.assertEqual(actual, {"Twinblast": {"wins": 2204}})


    def test_get_hero_dicts(self):
        actual_hero_to_id, actual_id_to_hero = get_hero_dicts({"Twinblast":{"Id":2}})
        self.assertEqual(actual_hero_to_id, {"Twinblast":2})
        self.assertEqual(actual_id_to_hero, {2:"Twinblast"})


    def test_get_user(self):
        actual = get_user("qchrisd", lambda _: [{"id": 29016,"username": "qchrisd"}])
        self.assertEqual(actual, {"id": 29016,"username": "qchrisd"})

    """
    def test_top_palyers(self):
        # fail case
        actual = get_user("qchrisd", lambda _: {"success": False})
        self.assertEqual(actual, -1)
        # success case
        actual = get_user("qchrisd", lambda _: {"success": True,"players": [{"rank": 1139,"id": 29016}]})
        self.assertEqual(actual, {"rank": 1139,"id": 29016})
    """

    def test_get_user_id(self):
        # fail case
        actual = get_user_id("qchrisd", lambda _: -1)
        self.assertEqual(actual, -1)
        # success case
        actual = get_user_id("qchrisd", lambda _: {"rank": 1139,"id": 29016})
        self.assertEqual(actual, 29016)


    def test_get_hero_info(self):
        actual = get_hero_info("Twinblast", lambda _: {"info": {"basicRange": "Ranged"}})
        self.assertEqual(actual, {"info": {"basicRange": "Ranged"}})


    def test_get_items(self):
        actual = get_items(lambda _:{"1": {"id": 1,"name": "S.I. Boots"}})
        self.assertEqual(actual, {"1": {"id": 1,"name": "S.I. Boots"}})


    def test_get_aspects(self):
        actual = get_aspects(lambda _:{"0": {"id": 0,"name": "King"}})
        self.assertEqual(actual, {"0": {"id": 0,"name": "King"}})

    """
    # Get matches is too impure to test. Leaving it as an orchestrator
    def test_get_matches(self):
        pass
    """

    def test_get_match_data(self):
        actual = get_match_data(766814, lambda _: {"ID": 766814,"Winner": 0,"StartDateTime": "2022-02-17T03:20:48.000Z"})
        self.assertEqual(actual["ID"], 766814)




# Run testing
if __name__ == '__main__':
    unittest.main()