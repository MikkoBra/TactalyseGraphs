import unittest
from unittest.mock import patch, MagicMock

from graph_app.data.preprocessors.radar_processor import RadarProcessor


class TestRadarProcessor(unittest.TestCase):

    def setUp(self):
        self.processor = RadarProcessor()
        self.radar_map = {"key": "value"}
        self.mock_return_value = MagicMock(return_value="mock")
        self.mock_league_df = MagicMock(return_value={"player": "stat"})

    def test_get_columns_radar_chart(self):
        with patch.object(self.processor, 'league_category_dictionary',
                          return_value={"position": "columns"}) as mock_columns:
            result = self.processor.get_columns_radar_chart("position")
            mock_columns.assert_called_once()
            self.assertEqual("columns", result)

    def test_set_player(self):
        params = {"player": "name"}
        result = self.processor.set_player(params, self.mock_league_df, self.radar_map)
        expected = {"key": "value", "player": "name"}
        self.assertEqual(expected, result)

    def test_set_random_player(self):
        params = {}
        with patch.object(self.processor.randomizer, 'random_player_radar', new=self.mock_return_value) as mock_random:
            result = self.processor.set_player(params, self.mock_league_df, self.radar_map)
            mock_random.assert_called_once_with(self.mock_league_df)
            expected = {"key": "value", "player": "mock"}
            self.assertEqual(expected, result)

    def test_set_player_data(self):
        params = {"player": "name"}
        with patch.object(self.processor.reader, 'league_data', new=self.mock_return_value) as mock_read:
            result = self.processor.set_player_data(self.mock_league_df, params)
            mock_read.assert_called_once_with("name", self.mock_league_df)
            expected = {"player": "name", "player_row": "mock"}
            self.assertEqual(expected, result)

    def test_set_player_positions(self):
        params = {'player_row': 'row'}
        with patch.object(self.processor, 'main_position_league_file', return_value='pos_f') as mock_file_pos:
            with patch.object(self.processor, 'position_dictionary', return_value={'pos_f': 'pos_l'}) as mock_long_pos:
                with patch.object(self.processor, 'shortened_dictionary',
                                  return_value={'pos_f': 'pos_s'}) as mock_short_pos:
                    result = self.processor.set_player_positions(params)
                    expected = {'player_row': 'row',
                                'main_pos': 'pos_f',
                                'player_pos': 'pos_l',
                                'player_pos_short': 'pos_s'}
                    mock_file_pos.assert_called_once_with('row')
                    mock_long_pos.assert_called_once()
                    mock_short_pos.assert_called_once()
                    self.assertEqual(expected, result)

    def test_set_compare_empty(self):
        result = self.processor.set_compare({}, self.mock_league_df, self.radar_map)
        self.assertEqual(self.radar_map, result)

    def test_set_compare(self):
        params = {"compare": "name"}
        with patch.object(self.processor.reader, 'league_data', new=self.mock_return_value) as mock_read:
            result = self.processor.set_compare(params, self.mock_league_df, self.radar_map)
            mock_read.assert_called_once_with("name", self.mock_league_df)
            expected = {"key": "value", "compare": "name", "compare_row": "mock"}
            self.assertEqual(expected, result)

    def test_set_stats(self):
        params = {"player_pos_short": "pos"}
        with patch.object(self.processor, 'get_columns_radar_chart', new=self.mock_return_value) as mock_columns:
            result = self.processor.set_stats(params)
            expected = {"player_pos_short": "pos", "columns": "mock"}
            mock_columns.assert_called_once_with("pos")
            self.assertEqual(expected, result)

    def test_set_max_vals(self):
        params = {"columns": "stats"}
        max_vals_df = MagicMock(return_value="max")
        self.mock_league_df.__getitem__().max.return_value = max_vals_df
        max_vals_df.tolist.return_value = "max vals list"
        result = self.processor.set_max_vals(self.mock_league_df, params)
        expected = {"columns": "stats", "scales": "max vals list"}
        self.assertEqual(expected, result)

    def test_extract_radar_data(self):
        radar_map = {'type': "radar"}
        params = {'league_df': self.mock_league_df}
        mock_player = MagicMock(return_value="player added")
        mock_data = MagicMock(return_value="data added")
        mock_pos = MagicMock(return_value="positions added")
        mock_compare = MagicMock(return_value="compare added")
        mock_stats = MagicMock(return_value="stats added")
        mock_scales = MagicMock(return_value="scales added")

        with patch.object(self.processor, 'set_player', new=mock_player) as set_player:
            with patch.object(self.processor, 'set_compare', new=mock_compare) as set_compare:
                with patch.object(self.processor, 'set_player_positions', new=mock_pos) as set_positions:
                    with patch.object(self.processor, 'set_player_data', new=mock_data) as set_data:
                        with patch.object(self.processor, 'set_max_vals', new=mock_scales) as set_scales:
                            with patch.object(self.processor, 'set_stats', new=mock_stats) as set_stats:
                                result = self.processor.extract_radar_data(params)
                                set_player.assert_called_once_with(params, self.mock_league_df, radar_map)
                                set_data.assert_called_once_with(self.mock_league_df, "player added")
                                set_positions.assert_called_once_with("data added")
                                set_compare.assert_called_once_with(params, self.mock_league_df, "positions added")
                                set_stats.assert_called_once_with("compare added")
                                set_scales.assert_called_once_with(self.mock_league_df, "stats added")
                                expected = "scales added"
                                self.assertEqual(expected, result)


if __name__ == "__main__":
    unittest.main()