import unittest
from unittest.mock import patch, MagicMock, Mock

from graph_app.controller.connectors.graph_connector import GraphConnector


class TestGraphConnector(unittest.TestCase):

    def setUp(self):
        self.param_map = {'key': 'value'}
        self.connector = GraphConnector()
        self.mock_return_value = MagicMock(return_value="mock data")
        self.mock_graph = MagicMock(return_value="mock graph")

    def test_get_data(self):
        params = self.param_map
        with patch.object(self.connector, "create_graph", new=self.mock_return_value) as mock_create_graph:
            result = self.connector.get_data(params)
            mock_create_graph.assert_called_once_with(params)
            self.assertEqual(result, "mock data")

    def test_create_graph(self):
        graph_mock = Mock()
        graph_mock.draw_all.return_value = "Mocked plot"
        factory_mock = Mock()
        factory_mock.create_instance.return_value = graph_mock
        self.connector.factory = factory_mock
        params = self.param_map

        plot = self.connector.create_graph(params)
        self.assertEqual(plot, "Mocked plot")
        factory_mock.create_instance.assert_called_with(params)
        graph_mock.draw_all.assert_called_with(params)
