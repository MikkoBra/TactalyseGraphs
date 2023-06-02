import unittest
from unittest.mock import patch
from graph_app.graph_generator.graphs.line_plot import LinePlot
from graph_app.graph_generator.graphs.line_plot_data_helper import LinePlotDataHelper
import pandas as pd
import os


class TestLinePlot(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Change the CWD to the root folder
        root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

        os.chdir(root_dir)

    def setUp(self):
        self.plot = LinePlot({'player_pos': 'pos'})
        dates = ['2020/01/01', '2020/01/02', '2020/01/03', '2020/01/04', '2020/01/05', '2020/01/06', '2020/01/07']
        data_p1 = [20, 3, 49, 3, 5, 6, 1]
        player_data = pd.DataFrame({'Date': dates, 'Stat': data_p1})
        data_p2 = [20, 5, 29, 13, 3, 15, 3]
        compare_data = pd.DataFrame({'Date': dates, 'Stat': data_p2})

        self.params = {
            "player_data": player_data,
            "compare_data": compare_data,
            "columns": "Stat",
            "start_date": "2020/01/02",
            "end_date": "2020/01/06",
            "player": "J. Doe",
            "compare": "D. Man"
        }

    def tearDown(self):
        pass

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

    def test_draw_returns_png(self):
        plot = self.plot.draw(self.params)
        self.assertNotEqual(plot, None, 'no changes')
        self.assertTrue(plot.startswith(b'\x89PNG'), 'Wrong graph format. Expected PNG.')


if __name__ == "__main__":
    unittest.main()
