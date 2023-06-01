import unittest
from unittest.mock import patch
import numpy as np
import matplotlib as plt

from graph_app.graph_generator.graphs.radar_chart import RadarChart


class RadarChartTestCase(unittest.TestCase):

    def setUp(self):
        self.param_map = {
            'player_pos': 'Player',
            'player_row': {
                'Team': 'Team A',
                'Matches played': 10,
                'Birth country': 'Country A'
            },
            'compare_row': {
                'Team': 'Team B',
                'Matches played': 5,
                'Birth country': 'Country B'
            },
            'player': 'Player A',
            'compare': 'Player B',
            'columns': ['Team', 'Matches played', 'Birth country'],
            'scales': [1, 2, 3]
        }
        self.radar_chart = RadarChart(self.param_map)

    def test_init(self):
        self.assertEqual(self.radar_chart.position, 'Player')

    def test_create_radar_chart(self):
        fig, ax, angles, p1_values, p2_values = self.radar_chart.create_radar_chart(
            [1, 2, 3], [4, 5, 6], [7, 8, 9]
        )
        self.assertIsNotNone(fig)
        self.assertIsNotNone(ax)
        self.assertEqual(angles, [0, np.pi, 0])
        self.assertEqual(p1_values, [1/7, 2/8, 3/9, 1/7])
        self.assertEqual(p2_values, [4/7, 5/8, 6/9, 4/7])

        fig, ax, angles, p1_values, p2_values = self.radar_chart.create_radar_chart(
            [1, 2, 3], None, [1, 2, 3]
        )
        self.assertIsNone(p2_values)

    def test_get_scale_labels(self):
        labels = self.radar_chart.get_scale_labels([1, 2, 3], 6.0)
        self.assertEqual(labels, [[0.0, 0.2, 0.4, 0.6, 0.8, 1.0], [0.0, 0.4, 0.8, 1.2, 1.6, 2.0], [0.0, 0.6, 1.2, 1.8, 2.4, 3.0]])

    def test_check_zeroes(self):
        zeroes = self.radar_chart.check_zeroes([0, 0, 0])
        self.assertTrue(zeroes)

        zeroes = self.radar_chart.check_zeroes([0, 1, 0])
        self.assertFalse(zeroes)

    def test_draw_all(self):
        with patch.object(self.radar_chart, 'draw', return_value='plot') as mock_draw:
            result = self.radar_chart.draw_all({})
            mock_draw.assert_called_once_with({})
            self.assertEqual('plot', result)


if __name__ == '__main__':
    unittest.main()
