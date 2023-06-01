import numpy as np
import pandas as pd


class LinePlotDataHelper:
    """
    Class containing all functionality needed by the LinePlot class to process the passed data into data usable in
    Seaborn and matplotlib functions.
    """

    def scaled_date_values(self, dates):
        """
        Converts a Series containing dates into integer representations of the dates, with the integer representing
        the distance in days from the first date.

        :param dates: Pandas Series containing each date for which there is a data point in the player file.
        :return: The Series converted to integers, each entry representing distance from the first date.
        """
        time_diff = dates.diff().dt.days
        time_diff = time_diff.fillna(0)

        scaled_date_values = np.cumsum(time_diff)
        return scaled_date_values

    def get_season_change_indices(self, dates):
        """
        Function that finds the indices of entries in a Series containing dates where the date is the first after the
        start of a football season (July 1st).

        :param dates: Pandas Series containing each date for which there is a data point in the player file.
        :return: List containing indices of the first data point in the Series after July 1st for each year.
        """
        season_indices = []
        year = dates.dt.year
        month = dates.dt.month
        for y in year.unique():
            year_dates = dates[year == y]
            first_of_july = year_dates[(month >= 7) & (year_dates.dt.day > 1)].index.min()
            if pd.notnull(first_of_july):
                season_indices.append(first_of_july)
        return season_indices

    def get_season_change_x_vals(self, season_indices, scaled_x_values):
        """
        Function that retrieves the line plot x-values from a data series corresponding with passed indices. The
        indices should represent the first data point after the start of a football season for each year in the series.
        The last x-value represented is also added so that the tick for the last season can be put between that and the
        last season value.

        :param season_indices: List containing indices of the data Series where the date is the first after the start of
        the football season for each year.
        :param scaled_x_values: Series containing line plot x-values representing all dates in a data Series.
        :return: The x-values corresponding with the start of the football season for each year.
        """
        season_x_values = []
        for i in season_indices:
            season_x_values.append(scaled_x_values[i])
        season_x_values.append(scaled_x_values.iloc[-1])
        return season_x_values

    def season_tick_labels(self, dates, year_indices):
        """
        Function that creates a label for each football season represented in the dates series.

        :param dates: Series containing dates for which a data point exists in the passed dataframe.
        :param year_indices: Indices in the dates Series for which the date is the first after the start of a football
        season.
        :return: List containing the season labels in string form.
        """
        date_strings = dates.iloc[year_indices].dt.strftime('%Y-%m-%d')
        years = date_strings.str.slice(start=2, stop=4)
        seasons = [f"{n}/{int(n)+1}" for n in years]
        return seasons

    def get_xlabels(self, data):
        """
        Function that retrieves the x-value representations of each match data point in a player file, as well as the
        x-values of season changes and the seasons in string form, to be used for x-axis ticks.

        :param data: DataFrame containing all relevant data to be plotted from a player file.
        :return: Series containing integer x-value representations of the dates in the passed DataFrame, list containing
        integer x-value representations of the first data point after a change in football season for each year, and
        a list containing string representations of each season represented in the passed Dataframe, in that order.
        """
        dates = pd.to_datetime(data["Date"], format='%Y-%m-%d')
        dates = dates.sort_values().reset_index(drop=True)

        scaled_x_values = self.scaled_date_values(dates)
        season_indices = self.get_season_change_indices(dates)
        season_x_values = self.get_season_change_x_vals(season_indices, scaled_x_values)
        seasons = self.season_tick_labels(dates, season_indices)

        return scaled_x_values, season_x_values, seasons

    def average_entries(self, x_vals, y_vals, window):
        """
        Function that averages every X data points in two passed Series, with X being defined by the 'window' parameter.

        :param x_vals: Series containing x-values to average.
        :param y_vals: Series containing y-values to average.
        :param window: The amount of data point to average per new data point. I.e., if set to 5, each data point in the
        returned Series is the average of 5 data points.
        :return: The input Series (x_vals, y_vals) with the data averaged over each 'window' data points.
        """
        avg_x = x_vals.rolling(window=window).mean()
        avg_x = avg_x[window-1::window]
        avg_y = y_vals.rolling(window=window).mean()
        avg_y = avg_y[window-1::window]
        return avg_x, avg_y

    def create_sub_plot_data(self, subcolumns, player_data, column_index):
        """
        Function for splitting the data for a sub-stat from its main stat. E.g.: Successful shots is split from Total
        shots.

        :param subcolumns: List containing the name of the column for the stat, split into the main stat at index 0, and
        the sub-stat at index 1.
        :param player_data: DataFrame containing one player's match data.
        :param column_index: Index of the main stat's column in the DataFrame.
        :return: Series containing data for the sub-stat from the player DataFrame, and the name of the sub-stat, in
        that order.
        """
        player_sub_data, second_column = None, None
        if len(subcolumns) > 1:
            second_column = subcolumns[1].strip()
            player_sub_data = player_data[player_data.columns[column_index + 1]][::-1].reset_index(drop=True)
        return player_sub_data, second_column

    def extract_data_from_param_map(self, param_map):
        """
        Function that extracts all known parameters from the passed parameter map.

        :param param_map: Map containing all passed parameters.
        :return: Each extracted parameter as a separate variable.
        """
        player_data = param_map.get('player_data')
        column_name = param_map.get('columns')
        start_date = param_map.get('start_date')
        end_date = param_map.get('end_date')
        player = param_map.get('player')
        compare = param_map.get('compare')
        compare_data = param_map.get('compare_data')
        return player_data, column_name, start_date, end_date, player, compare, compare_data

    def set_season_tick_values(self, season_x_vals):
        tick_vals = []
        for i, season in enumerate(season_x_vals):
            if i == len(season_x_vals) - 1:
                return tick_vals
            tick_vals.append((season_x_vals[i] + season_x_vals[i+1])/2)
