"""
Unit tests for FaultAPI module.

Written by Chris Quartararo
Last update 3/7/2022

"""

# Imports
import unittest
import unittest.mock as mock

# Import methods
import fault_api
from fault_api import (_decode_json,
                       _create_pool_manager,
                       _check_user_request_response,
                       get_hero_play_stats,
                       get_hero_dicts,
                       get_user,
                       get_user_id,
                       get_hero_info,
                       get_items,
                       get_aspects,
                       get_matches,
                       get_match_data,
                       get_player_hero_stats,
                       get_elo)

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
        self.assertEqual(actual_failure, None)


    @mock.patch("fault_api._query_website")
    def test_get_hero_play_stats(self, mock_query_website):
        mock_query_website.return_value={"heroes": {"Twinblast": {"wins": 2204}}}
        actual = get_hero_play_stats()
        self.assertEqual(actual, {"Twinblast": {"wins": 2204}})


    def test_get_hero_dicts(self):
        actual_hero_to_id, actual_id_to_hero = get_hero_dicts({"Twinblast":{"Id":2}})
        self.assertEqual(actual_hero_to_id, {"Twinblast":2})
        self.assertEqual(actual_id_to_hero, {2:"Twinblast"})


    @mock.patch("fault_api._query_website")
    def test_get_user(self, mock_query_website):
        # Success case
        mock_query_website.return_value = [{"id": 29016,"username": "qchrisd"}]
        actual = get_user("qchrisd")
        self.assertEqual(actual, {"id": 29016,"username": "qchrisd"})
        # Fail case
        mock_query_website.return_value = []
        actual = get_user("qchrisd")
        self.assertEqual(actual, None)


    # TODO add test for a useful function
    @unittest.skip("Function is not ready for testing")
    def test_top_palyers(self):
        # fail case
        actual = get_user("qchrisd", lambda _: {"success": False})
        self.assertEqual(actual, None)
        # success case
        actual = get_user("qchrisd", lambda _: {"success": True,"players": [{"rank": 1139,"id": 29016}]})
        self.assertEqual(actual, {"rank": 1139,"id": 29016})


    @unittest.skip("Function still uses old get_user function. This method may not be needed.")
    @mock.patch("fault_api._query_website")
    def test_get_user_id(self, mock_query_website):
        # fail case
        mock_query_website.return_value = None
        actual = get_user_id("qchrisd")
        self.assertEqual(actual, None)
        # success case
        mock_query_website.return_value = {"rank": 1139,"id": 29016}
        actual = get_user_id("qchrisd")
        self.assertEqual(actual, 29016)

    
    @mock.patch("fault_api._query_website")
    def test_get_hero_info(self, mock_query_website):
        mock_query_website.return_value = {"info": {"basicRange": "Ranged"}}
        actual = get_hero_info("Twinblast")
        self.assertEqual(actual, {"info": {"basicRange": "Ranged"}})

    
    @mock.patch("fault_api._query_website")
    def test_get_items(self, mock_query_website):
        mock_query_website.return_value = {"1": {"id": 1,"name": "S.I. Boots"}}
        actual = get_items()
        self.assertEqual(actual, {"1": {"id": 1,"name": "S.I. Boots"}})

    
    @mock.patch("fault_api._query_website")
    def test_get_aspects(self, mock_query_website):
        mock_query_website.return_value = {"0": {"id": 0,"name": "King"}}
        actual = get_aspects()
        self.assertEqual(actual, {"0": {"id": 0,"name": "King"}})


    @mock.patch("fault_api._query_website")
    def test_get_matches(self, mock_query_website):
        # Successfully found user
        mock_query_website.return_value = {"success": True,"matches": [{"id": 766814}]}
        actual = get_matches({"ID":29016, "username":"qchrisd"})
        self.assertEqual(actual, {"id": 766814})
        # Failed to find user
        mock_query_website.return_value = {"success":False}
        actual = get_matches(None)
        self.assertEqual(actual, None)


    @mock.patch("fault_api._query_website")
    def test_get_match_data(self, mock_query_website):
        mock_query_website.return_value = {"ID": 766814,"Winner": 0,"StartDateTime": "2022-02-17T03:20:48.000Z"}
        actual = get_match_data(766814)
        self.assertEqual(actual["ID"], 766814)

    
    @mock.patch("fault_api._query_website")
    def test_get_player_hero_stats(self, mock_query_website):
        user = {"ID":29016, "username":"qchrisd"}
        # successfully found user
        mock_query_website.return_value ={"heroes": {"2": {"wins": 27,"games": 49,"kills": 380,"deaths": 244,"assists": 273}}}
        actual = get_player_hero_stats(user)
        self.assertEqual(actual["2"]["wins"], 27)
        # Failed to find user
        mock_query_website.return_value = {"success": False}
        actual = get_player_hero_stats(None)
        self.assertEqual(actual, None)


    @mock.patch("fault_api._query_website")
    def test_get_elo(self, mock_query_website):
        user = {"ID":29016, "username":"qchrisd"}
        # successfully found user
        mock_query_website.return_value = {"id":"29016","username":"qchrisd","eloTitle":"Silver","MMR":1223.1,"ranking":1136,"placementGamesRemain":0}
        actual = get_elo(user)
        self.assertEqual(actual["id"], "29016")
        # Failed to find user
        actual = get_elo(None)
        self.assertEqual(actual, None)
    

# Run testing
if __name__ == '__main__':
    unittest.main()