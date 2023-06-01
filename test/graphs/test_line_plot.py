import unittest
from unittest.mock import patch, MagicMock
from graph_app.graph_generator.graphs.line_plot import LinePlot
from graph_app.graph_generator.graphs.line_plot_data_helper import LinePlotDataHelper


class TestLinePlot(unittest.TestCase):

    def setUp(self):
        self.plot = LinePlot({'player_pos': 'pos'})

    def test_constructor(self):
        self.assertIsInstance(self.plot.helper, LinePlotDataHelper)
        self.assertEqual('pos', self.plot.position)

    def test_draw_all(self):
        cols = ['stat1', 'stat2']
        params = {
            'columns': cols
        }
        with patch.object(self.plot, 'draw', return_value='plot'):
            result = self.plot.draw_all(params)
            expected = ['plot', 'plot']
            self.assertEqual(expected, result)

    def test_draw_all_one_stat(self):
        cols = ['stat1']
        params = {
            'columns': cols
        }
        with patch.object(self.plot, 'draw', return_value='plot'):
            result = self.plot.draw_all(params)
            expected = 'plot'
            self.assertEqual(expected, result)

