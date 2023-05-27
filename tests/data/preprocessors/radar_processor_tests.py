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
        with patch.object(self.processor, 'league_category_dictionary', return_value={"position": "columns"}) as mock_columns:
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
        mock_player_row = MagicMock(return_value={"player": "stat"})
        mock_file_pos = MagicMock(return_value="pos_f")
        mock_pos = MagicMock(return_value={"pos_f": "pos_l"})
        mock_short_pos = MagicMock(return_value={"pos_f": "pos_s"})
        with patch.object(self.processor.reader, 'league_data', new=mock_player_row) as mock_read:
            with patch.object(self.processor, 'main_position_league_file', new=mock_file_pos) \
                    as mock_get_file_pos:
                with patch.object(self.processor, 'position_dictionary', new=mock_pos) \
                        as mock_get_long_pos:
                    with patch.object(self.processor, 'shortened_dictionary', new=mock_short_pos) \
                            as mock_get_short_pos:
                        result = self.processor.set_player_data(self.mock_league_df, params)
                        expected = {"player": "name", "main_pos": "pos_f", "player_pos": "pos_l",
                                    "player_pos_short": "pos_s", "player_row": {"player": "stat"}}
                        mock_read.assert_called_once_with("name", self.mock_league_df)
                        mock_get_file_pos.assert_called_once_with("mock")
                        mock_get_long_pos.assert_called_once()
                        mock_get_short_pos.assert_called_once()
                        self.assertEqual(expected, result)
