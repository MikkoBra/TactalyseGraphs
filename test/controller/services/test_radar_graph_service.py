import unittest
from unittest.mock import patch, MagicMock

from flask import Response

from graph_app.controller.services.radar_graph_service import RadarGraphService


class TestRadarGraphService(unittest.TestCase):

    def setUp(self):
        self.api_params = {"league": "league1",
                           "player": "player1",
                           "compare": "player2"}
        self.data_map = {"type": "radar",
                         "league": "league1",
                         "player": "player1",
                         "compare": "player2"}
        self.service = RadarGraphService()
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
                response = self.service.pass_data(self.data_map)
                mock_data_get_data.assert_called_once_with(self.data_map)
                mock_graph_get_data.assert_called_once_with("mock data 1")
                self.assertIsInstance(response, Response)
                self.assertEqual('image/png', response.mimetype)
                self.assertEqual("mock data 2", response.data.decode('utf-8'))


if __name__ == '__main__':
    unittest.main()
