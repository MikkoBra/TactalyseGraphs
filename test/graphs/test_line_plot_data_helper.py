import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
from datetime import datetime
from graph_app.graph_generator.graphs.line_plot_data_helper import LinePlotDataHelper


class TestLinePlotDataHelper(unittest.TestCase):

    def setUp(self):
        self.helper = LinePlotDataHelper()

    def test_scaled_date_values(self):
        dates = pd.Series([
            datetime(2023, 5, 1),
            datetime(2023, 5, 3),
            datetime(2023, 5, 6),
            datetime(2023, 5, 10)
        ])
        expected = pd.Series([0, 2, 5, 9])
        result = self.helper.scaled_date_values(dates)
        self.assertEqual(expected.tolist(), result.tolist())

    def test_get_season_change_indices(self):
        dates = pd.Series([
            datetime(2023, 5, 1),
            datetime(2023, 7, 3),
            datetime(2024, 5, 6),
            datetime(2024, 9, 10)
        ])
        expected = [1, 3]
        result = self.helper.get_season_change_indices(dates)
        self.assertEqual(expected, result)

    def test_get_season_change_x_vals(self):
        x_vals = pd.Series([0, 2, 5, 9])
        indices = [1, 3]
        expected = [2, 9, 9]
        result = self.helper.get_season_change_x_vals(indices, x_vals)
        self.assertEqual(expected, result)

    def test_season_tick_labels(self):
        dates = pd.Series([
            datetime(2023, 5, 1),
            datetime(2023, 7, 3),
            datetime(2024, 5, 6),
            datetime(2024, 9, 10)
        ])
        indices = [1, 3]
        expected = ['23/24', '24/25']
        result = self.helper.season_tick_labels(dates, indices)
        self.assertEqual(expected, result)

    def test_get_xlabels(self):
        dates_string = [
            {"Date": "2022-01-01"},
            {"Date": "2022-01-02"},
            {"Date": "2022-01-03"}
        ]
        data = pd.DataFrame(dates_string)
        dates = [
            datetime(2022, 1, 1),
            datetime(2022, 1, 2),
            datetime(2022, 1, 3)
        ]
        with patch.object(pd, 'to_datetime', return_value=pd.Series(dates)) as to_dt:
            with patch.object(self.helper, 'scaled_date_values', return_value='scaled') as scaled:
                with patch.object(self.helper, 'get_season_change_indices', return_value='idx') as szn_idx:
                    with patch.object(self.helper, 'get_season_change_x_vals', return_value='x') as szn_x_vals:
                        with patch.object(self.helper, 'season_tick_labels', return_value='labs') as labels:
                            result_scaled, result_szn_x, result_labels = self.helper.get_xlabels(data)
                            expected_scaled, expected_szn_x, expected_labels = 'scaled', 'x', 'labs'
                            self.assertEqual(result_scaled, expected_scaled)
                            self.assertEqual(result_szn_x, expected_szn_x)
                            self.assertEqual(result_labels, expected_labels)
                            to_dt.assert_called_once_with(data['Date'], format='%Y-%m-%d')
                            scaled.assert_called_once()
                            szn_idx.assert_called_once()
                            szn_x_vals.assert_called_once_with('idx', 'scaled')
                            labels.assert_called_once()

    def test_average_entries(self):
        x_vals = pd.Series([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        y_vals = pd.Series([2, 4, 6, 8, 10, 12, 14, 16, 18, 20])
        r_x, r_y = self.helper.average_entries(x_vals, y_vals, 5)
        e_x, e_y = pd.Series([3, 8]), pd.Series([6, 16])
        self.assertEqual(e_x.tolist(), r_x.tolist())
        self.assertEqual(e_y.tolist(), r_y.tolist())

    def test_create_sub_plot_data(self):
        subcolumns = ['Total shots', 'Successful shots']
        column_index = 0
        player_data = pd.DataFrame({
            'Total shots': [10, 15, 8, 12],
            'Successful shots': [7, 12, 5, 10]
        })
        result_data, result_column = self.helper.create_sub_plot_data(subcolumns, player_data, column_index)
        expected_data = pd.Series([7, 12, 5, 10])[::-1].reset_index(drop=True)
        expected_column = 'Successful shots'
        self.assertEqual(result_data.tolist(), expected_data.tolist())
        self.assertEqual(result_column, expected_column)

    def test_extract_data_from_param_map(self):
        params = {
            'player_data': 'data',
            'columns': 'cols',
            'start_date': 'start',
            'end_date': 'end',
            'player': 'name',
            'compare': None,
            'compare_data': None
        }
        r_data, r_cols, r_start, r_end, r_player, r_comp, r_compdata = self.helper.extract_data_from_param_map(params)
        e_data = 'data'
        e_cols = 'cols'
        e_start = 'start'
        e_end = 'end'
        e_player = 'name'
        self.assertEqual(e_data, r_data)
        self.assertEqual(e_cols, r_cols)
        self.assertEqual(e_start, r_start)
        self.assertEqual(e_end, r_end)
        self.assertEqual(e_player, r_player)
        self.assertIsNone(r_comp)
        self.assertIsNone(r_compdata)

    def test_set_season_tick_values(self):
        season_x_vals = [0, 10, 20, 30, 40]
        result = self.helper.set_season_tick_values(season_x_vals)
        self.assertEqual([5, 15, 25, 35], result)


if __name__ == "__main__":
    unittest.main()
