import unittest
from unittest.mock import patch, MagicMock

from flask import Response

from graph_app.controller.services.random_graph_service import RandomGraphService


class TestRandomGraphService(unittest.TestCase):

    def setUp(self):
        self.api_params = {"league": "league1",
                           "graph-type": "graph",
                           "player": "player1",
                           "start-date": "start",
                           "end-date": "end"}
        self.data_map = {"type": "random",
                         "league": "league1",
                         "graph_type": "graph",
                         "player": "player1",
                         "start_date": "start",
                         "end_date": "end"}
        self.service = RandomGraphService()
        self.mock_return_value = MagicMock(return_value="mock data 1")
        self.mock_return_value_2 = MagicMock(return_value="mock data 2")

    def test_json_process(self):
        with patch.object(self.service, "pass_data", new=self.mock_return_value) as mock_pass_data:
            result = self.service.json_process(self.api_params)
            mock_pass_data.assert_called_once_with(self.data_map)
            self.assertEqual("mock data 1", result)

    def test_key_value_process(self):
        with patch.object(self.service, "pass_data", new=self.mock_return_value) as mock_pass_data:
            result = self.service.key_value_process(None, self.api_params)
            mock_pass_data.assert_called_once_with(self.data_map)
            self.assertEqual("mock data 1", result)

    def test_pass_data(self):
        with patch.object(self.service.data_connector, 'get_data', new=self.mock_return_value) as mock_data_get_data:
            with patch.object(self.service.graph_connector, 'get_data', new=self.mock_return_value_2) \
                    as mock_graph_get_data:
                with patch.object(self.service, 'create_response', return_value='mock response') as mock_make_response:
                    response = self.service.pass_data(self.data_map)
                    mock_data_get_data.assert_called_once_with(self.data_map)
                    mock_graph_get_data.assert_called_once_with("mock data 1")
                    mock_make_response.assert_called_once_with('mock data 1', 'mock data 2')
                    expected = 'mock response'
                    self.assertEqual(expected, response)

    def test_create_response(self):
        mock_graph = MagicMock()
        params = {'player': 'pname', 'compare': 'cname'}
        response = self.service.create_response(params, mock_graph)
        self.assertIsInstance(response, Response)
        self.assertEqual('image/png', response.mimetype)
        self.assertEqual('pname', response.headers['player'])
        self.assertEqual('cname', response.headers['compare'])


if __name__ == "__main__":
    unittest.main()
