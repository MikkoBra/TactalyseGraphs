import unittest
from unittest.mock import patch, MagicMock

from graph_app.data.preprocessors.line_processor import LineProcessor


class TestLineProcessor(unittest.TestCase):

    def setUp(self):
        self.processor = LineProcessor()
        self.line_map = {"key": "value"}
        self.mock_return_value = MagicMock(return_value="mock")

    def test_set_player(self):
        params = {"player": "name"}
        result = self.processor.set_player(params, self.line_map)
        expected = {"key": "value", "player": "name"}
        self.assertEqual(expected, result)

    def test_set_player_random(self):
        with patch.object(self.processor.randomizer, 'random_player', new=self.mock_return_value) as mock_random:
            result = self.processor.set_player({}, {})
            mock_random.assert_called_once()
            self.assertTrue("player" in result.keys())

    def test_set_compare_empty(self):
        result = self.processor.set_compare({}, self.line_map)
        self.assertEqual(self.line_map, result)

    def test_set_compare(self):
        params = {"compare": "name"}
        with patch.object(self.processor.reader, 'player_data', new=self.mock_return_value) as mock_read:
            result = self.processor.set_compare(params, self.line_map)
            mock_read.assert_called_once_with("name")
            expected = {"key": "value", "compare": "name", "compare_data": "mock"}
            self.assertEqual(expected, result)

    def test_set_league(self):
        params = {"league": "LEA"}
        result = self.processor.set_league(params, self.line_map)
        expected = {"key": "value", "league": "LEA"}
        self.assertEqual(expected, result)

    def test_set_league_lowercase_input(self):
        params = {"league": "lea"}
        result = self.processor.set_league(params, self.line_map)
        expected = {"key": "value", "league": "LEA"}
        self.assertEqual(expected, result)

    def test_set_league_no_league(self):
        result = self.processor.set_league({}, self.line_map)
        expected = {"key": "value", "league": "League"}
        self.assertEqual(expected, result)

    def test_set_player_data(self):
        params = {"player": "name"}
        mock_file_pos = MagicMock(return_value="pos_f")
        mock_pos = MagicMock(return_value={"pos_f": "pos_l"})
        mock_short_pos = MagicMock(return_value={"pos_f": "pos_s"})
        with patch.object(self.processor.reader, 'player_data', new=self.mock_return_value) as mock_read:
            with patch.object(self.processor, 'main_position_player_file', new=mock_file_pos) \
                    as mock_get_file_pos:
                with patch.object(self.processor, 'position_dictionary', new=mock_pos) \
                        as mock_get_long_pos:
                    with patch.object(self.processor, 'shortened_dictionary', new=mock_short_pos) \
                            as mock_get_short_pos:
                        result = self.processor.set_player_data(params)
                        expected = {"player": "name", "main_pos": "pos_f", "player_pos": "pos_l",
                                    "main_pos_short": "pos_s", "player_data": "mock"}
                        mock_read.assert_called_once_with("name")
                        mock_get_file_pos.assert_called_once_with("mock")
                        mock_get_long_pos.assert_called_once()
                        mock_get_short_pos.assert_called_once()
                        self.assertEqual(expected, result)

    def test_set_tactalyse_data(self):
        params = {"start_date": "start", "end_date": "end"}
        result = self.processor.set_tactalyse_data(params, self.line_map)
        params["key"] = "value"
        expected = params
        self.assertEqual(expected, result)

    def test_set_tactalyse_data_no_data(self):
        params = {}
        result = self.processor.set_tactalyse_data(params, self.line_map)
        params = {"start_date": None, "end_date": None}
        params["key"] = "value"
        expected = params
        self.assertEqual(expected, result)

    def test_set_stats(self):
        params = {'stat': 'stat'}
        result = self.processor.set_stats(params, self.line_map)
        expected = {'key': 'value', 'columns': ['stat']}
        self.assertEqual(expected, result)

    def test_set_stats_no_stat(self):
        params = {}
        with patch.object(self.processor.randomizer, 'random_player_stat', new=self.mock_return_value):
            result = self.processor.set_stats(params, self.line_map)
            expected = {'key': 'value', 'columns': ['mock']}
            self.assertEqual(expected, result)

    def test_extract_line_data(self):
        line_map = {'type': "line"}
        mock_player = MagicMock(return_value="player added")
        mock_compare = MagicMock(return_value="compare added")
        mock_league = MagicMock(return_value="league added")
        mock_data = MagicMock(return_value="data added")
        mock_dates = MagicMock(return_value="dates added")
        mock_stats = MagicMock(return_value="stats added")
        with patch.object(self.processor, 'set_player', new=mock_player) as set_player:
            with patch.object(self.processor, 'set_compare', new=mock_compare) as set_compare:
                with patch.object(self.processor, 'set_league', new=mock_league) as set_league:
                    with patch.object(self.processor, 'set_player_data', new=mock_data) as set_data:
                        with patch.object(self.processor, 'set_tactalyse_data', new=mock_dates) as set_dates:
                            with patch.object(self.processor, 'set_stats', new=mock_stats) as set_stats:
                                result = self.processor.extract_line_data({})
                                set_player.assert_called_once_with({}, line_map)
                                set_compare.assert_called_once_with({}, "player added")
                                set_league.assert_called_once_with({}, "compare added")
                                set_data.assert_called_once_with("league added")
                                set_dates.assert_called_once_with({}, "data added")
                                set_stats.assert_called_once_with({}, "dates added")
                                expected = "stats added"
                                self.assertEqual(expected, result)


if __name__ == "__main__":
    unittest.main()
