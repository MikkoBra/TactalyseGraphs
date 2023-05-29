import unittest
from unittest.mock import patch, MagicMock

from graph_app.data.preprocessors.randomizer import Randomizer


class TestRandomizer(unittest.TestCase):

    def setUp(self):
        self.randomizer = Randomizer()
        self.mock_league_df = MagicMock()

    def test_random_player_line_graph(self):
        params = {'graph_type': 'line'}
        with patch.object(self.randomizer, 'random_player_line', return_value='mock name') as mock_random:
            result = self.randomizer.random_player(params)
            expected = {'graph_type': 'line', 'player': 'mock name'}
            mock_random.assert_called_once()
            self.assertEqual(expected, result)

    def test_random_player_radar_graph(self):
        params = {
            'graph_type': 'radar',
            'league_df': self.mock_league_df
        }
        with patch.object(self.randomizer, 'random_player_radar', return_value='mock name') as mock_name:
            result = self.randomizer.random_player(params)
            expected = {
                'graph_type': 'radar',
                'league_df': self.mock_league_df,
                'player': 'mock name'
            }
            self.assertEqual(expected, result)
            mock_name.assert_called_once_with(self.mock_league_df)

    def test_random_player_radar(self):
        # Configure the MagicMock to return a random value when called
        self.mock_league_df.__getitem__.return_value.sample.return_value = MagicMock(values=['mock name'])
        result = self.randomizer.random_player_radar(self.mock_league_df)
        expected = 'mock name'
        self.assertEqual(expected, result)

    def test_random_compare(self):
        params = {
            'player': 'p1',
            'league_df': self.mock_league_df
        }
        with patch.object(self.randomizer.reader, 'league_data', return_value='row') as mock_row:
            with patch.object(self.randomizer, 'main_position_league_file', return_value='pos') as mock_pos:
                with patch.object(self.randomizer, 'select_random_compare', return_value='p2') as mock_name:
                    result = self.randomizer.random_compare(params)
                    expected = {
                        'player': 'p1',
                        'league_df': self.mock_league_df,
                        'compare': 'p2'
                    }
                    mock_row.assert_called_once_with('p1', self.mock_league_df)
                    mock_pos.assert_called_once_with('row')
                    mock_name.assert_called_once_with(self.mock_league_df, 'pos', 'p1')
                    self.assertEqual(expected, result)


if __name__ == "__main__":
    unittest.main()
