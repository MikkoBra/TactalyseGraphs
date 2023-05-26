import unittest
from unittest.mock import patch, MagicMock, Mock
from graph_app.controller.connectors.data_connector import DataConnector
from graph_app.data.preprocessors.randomizer import Randomizer


class TestDataConnector(unittest.TestCase):

    def setUp(self):
        self.connector = DataConnector()
        self.randomizer = Randomizer()
        self.radar_map = {'type': 'radar'}
        self.line_map = {'type': 'line'}
        self.random_map = {'type': 'random'}
        self.mock_return_value = MagicMock(return_value="mock data")

    def test_random_choice(self):
        params = self.random_map
        params = self.connector.random_graph_choice(params)
        self.assertIn(params.get('graph_type'), ['radar', 'line'])

    def test_random_choice_line(self):
        params = self.random_map
        params['graph_type'] = 'line'
        params = self.connector.random_graph_choice(params)
        self.assertEqual(params.get('graph_type'), 'line')

    def test_random_choice_radar(self):
        params = self.random_map
        params['graph_type'] = 'radar'
        params = self.connector.random_graph_choice(params)
        self.assertEqual(params.get('graph_type'), 'radar')

    def test_random_choice_false_type(self):
        params = self.random_map
        params['graph_type'] = 'nonsense'
        with self.assertRaises(ValueError):
            self.connector.random_graph_choice(params)

    def test_random_choice_not_random(self):
        self.assertEqual(self.connector.random_graph_choice(self.radar_map), self.radar_map)

    def test_set_random_data_calls_random_choice(self):
        with patch.object(self.connector, "random_graph_choice") as mock_random_choice:
            with patch.object(self.connector.randomizer, 'set_random_parameters', new=self.mock_return_value):
                self.connector.set_random_data(self.random_map)
                mock_random_choice.assert_called_once_with(self.random_map)

    def test_set_random_data_calls_set_random_parameters(self):

        params = self.random_map
        mock_choice = params
        mock_choice['graph_type'] = 'line'

        with patch.object(self.connector, "random_graph_choice", return_value=mock_choice):
            with patch.object(self.connector.randomizer, "set_random_parameters", new=self.mock_return_value)\
                    as randomizer_instance_mock:
                result = self.connector.set_random_data(params)
                randomizer_instance_mock.assert_called_once_with(mock_choice)
                self.assertEqual(result, "mock data")

    def test_set_random_data_line(self):
        params = self.line_map
        with patch.object(self.connector.randomizer, "set_random_parameters") as mock_randomizer_call:
            self.assertEqual('line', self.connector.set_random_data(params).get('type'))
            mock_randomizer_call.assert_not_called()

    def test_set_random_data_radar(self):
        params = self.radar_map
        with patch.object(self.connector.randomizer, "set_random_parameters") as mock_randomizer_call:
            self.assertEqual('radar', self.connector.set_random_data(params).get('type'))
            mock_randomizer_call.assert_not_called()

    def test_get_data_for_radar(self):
        params = self.radar_map
        with patch.object(self.connector, "set_random_data", return_value=params) as mock_set_random_data:
            with patch.object(self.connector, "get_radar_data", new=self.mock_return_value) as mock_get_radar_data:
                results = self.connector.get_data(params)
                mock_set_random_data.assert_called_once_with(params)
                mock_get_radar_data.assert_called_once_with(params)
                self.assertEqual('mock data', results)

    def test_get_data_for_line(self):
        params = self.line_map
        with patch.object(self.connector, "set_random_data", return_value=params) as mock_set_random_data:
            with patch.object(self.connector, "get_line_data", new=self.mock_return_value) as mock_get_line_data:
                results = self.connector.get_data(params)
                mock_set_random_data.assert_called_once_with(params)
                mock_get_line_data.assert_called_once_with(params)
                self.assertEqual('mock data', results)

    def test_get_radar_data(self):
        params = self.radar_map
        with patch.object(self.connector.radar_processor, "extract_radar_data", new=self.mock_return_value)\
                as processor_instance_mock:
            result = self.connector.get_radar_data(params)
            processor_instance_mock.assert_called_once_with(params)
            self.assertEqual(result, "mock data")

    def test_get_line_data(self):
        params = self.line_map
        with patch.object(self.connector.line_processor, "extract_line_data", new=self.mock_return_value)\
                as processor_instance_mock:
            result = self.connector.get_line_data(params)
            processor_instance_mock.assert_called_once_with(params)
            self.assertEqual(result, "mock data")


if __name__ == '__main__':
    unittest.main()
