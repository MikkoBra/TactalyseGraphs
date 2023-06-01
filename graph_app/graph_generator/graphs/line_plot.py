import io

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib.offsetbox import AnnotationBbox, OffsetImage

from .abstract_models import Graph
from .line_plot_data_helper import LinePlotDataHelper


class LinePlot(Graph):
    """
    Class representing a line graph. It contains functionality for generating one from input data passed in a parameter
    map, with the main data coming from a dataframe. This dataframe is extracted from a player file in the 'files'
    folder of this project. Most variables to do with layout and colors have been set as class attributes. They may all
    be adjusted manually within this class. This class only contains functions directly to do with drawing plots and
    setting layout. Data processing functions are contained in LinePlotDataHelper.
    """
    # Main player's position
    __position = ''
    # Tactalyse's company color (red)
    __tactalyse = "#e51e24"
    # Black color code
    __black = "#242424"
    # Color used for the season lines in the graph
    __season_color = "#00a70b"
    # Color used for the main player's main stat line
    __player_color = '#f45600'
    # Color used for the main player's sub-stat line
    __player_sub_color = '#dda2a4'
    # Color used for the comparison player's main stat line
    __compare_color = '#4a24ec'
    # Color used for the comparison player's sub-stat line
    __compare_sub_color = '#bbafec'
    # Color used for the graph's title
    __title = "#D46508"
    # Color used for the graph's subtitle
    __subtitle = "#5E5E5E"
    # Distance of the bottom of graph from the bottom
    __bottom_offset = 0.1
    # Distance of the top of the graph from the bottom
    __top_offset = 0.8
    # Distance of the right side of the graph from the left
    __right_offset = 0.95
    # Distance of the left side of the graph from the left
    __left_offset = 0.1
    # Distance of the subtitle, presumably from the bottom
    __subtitle_offset = 0.895
    # Distance of the title from the graph itself
    __title_offset = 1.15
    # Distance of tactalyse's logo from the left of the graph
    __logo_x_offset = 0.95
    # Distance of tactalyse's logo from the bottom of the graph
    __logo_y_offset = 1.15
    # Zoom of the logo, 1 = original image size
    __logo_size = 0.5
    # Amount of original data points to average for each plotted point
    __avg_window = 4

    def __init__(self, param_map):
        """
        Constructor for the class. Sets the main player's position to be used in the graph's title.

        :param param_map: Map containing the player's position (player_pos) in string form.
        """
        player_pos = param_map.get('player_pos')
        if player_pos:
            self.__position = player_pos
        self.__helper = LinePlotDataHelper()

    def create_plot(self, ax, dates_x_values, data, color, label, order):
        """
        Function for creating a line plot using Seaborn.

        :param ax: The ax object to use for the plot.
        :param dates_x_values: Integer value representations of dates to be plotted on the x-axis.
        :param data: Stat values to plot on the y-axis.
        :param color: Color to use for the line.
        :param label: Label for the line, to be used in the legend.
        :param order: Order in which the line should be drawn in the whole plot, with a lower value being drawn first.
        """
        sns.lineplot(x=dates_x_values, y=data, ax=ax, color=color, label=label, zorder=order, linewidth=1)

    def plot_player(self, ax, player_x_values, player_stat_data, player, stat, color, player_sub_data=None,
                    sub_stat=None, sub_color=None):
        """
        Function for plotting a player's line in a line plot.

        :param ax: The ax object to use for the plot.
        :param player_x_values: Integer value representations of dates to be plotted on the x-axis.
        :param player_stat_data: Series containing data for the stat to plot from the player DataFrame.
        :param player: Name of the player to plot.
        :param stat: Name of the stat to plot.
        :param color: Color to use for the line.
        :param player_sub_data: Series containing data for the sub-stat to plot from the player DataFrame.
        :param sub_stat: Name of the sub-stat to plot.
        :param sub_color: Color to use for the sub-stat line.
        """
        x_vals, y_vals = self.__helper.average_entries(player_x_values, player_stat_data, self.__avg_window)
        label = stat + " for " + player
        self.create_plot(ax, x_vals, y_vals, color, label, order=1)
        if player_sub_data is not None:
            x_vals, y_vals = self.__helper.average_entries(player_x_values, player_sub_data, self.__avg_window)
            label = sub_stat.capitalize() + " for " + player
            self.create_plot(ax, x_vals, y_vals, sub_color, label, order=1)

    def draw_seasons(self, ax, season_x_values, seasons):
        """
        Function for plotting vertical lines representing a change in football season.

        :param ax: The ax object to use for the plot.
        :param season_x_values: Integer value representations of the lines to be plotted on the x-axis.
        :param seasons: List containing string labels for each season to plot.
        :return: Ax object with the season lines drawn.
        """
        plt.xlabel("Season")
        ax.set(xticks=self.helper.set_season_tick_values(season_x_values), xticklabels=seasons)
        no_label = False
        for i, season in enumerate(season_x_values):
            if i == len(season_x_values) - 1:
                break
            if no_label:
                ax.axvline(x=season, linestyle="dashed", color=self.__black)
            else:
                ax.axvline(x=season, linestyle="dashed", color=self.__black, label="Season")
                no_label = True
        return ax

    def draw_tactalyse_dates(self, ax, data, start_date, end_date):
        """
        Function for plotting vertical lines representing the start- and end-date of Tactalyse's services for the main
        player that is being graphed.

        :param ax: The ax object to use for the plot.
        :param data: DataFrame containing player match data extracted from a player file.
        :param start_date: String containing the start date in YYYY-mm-dd format.
        :param end_date: String containing the end date in YYYY-mm-dd format.
        :return: Ax object with the Tactalyse contract lines drawn.
        """
        dates = pd.to_datetime(data["Date"], format='%Y-%m-%d')
        dates = dates.sort_values().reset_index(drop=True)
        start = pd.Timestamp(start_date)
        end = pd.Timestamp(end_date)

        scaled_x_values = self.__helper.scaled_date_values(dates)
        start_idx = dates.searchsorted(start, side='left') - 1
        start_x = scaled_x_values[start_idx]
        end_idx = dates.searchsorted(end, side='left') - 1
        end_x = scaled_x_values[end_idx]

        if 0 <= start_idx <= len(dates):
            ax.axvline(x=start_x, linestyle="-", label="Tactalyse contract", color=self.__black)
            if start_idx < end_idx <= len(dates):
                ax.axvline(x=end_x, linestyle="-", color=self.__black)
        return ax

    def set_layout(self, ax, p1, p2, stat):
        """
        Function that handles all things to do with layout of the plot. It has functionality for setting the title and
        subtitle of the plot, and the position and size of Tactalyse's logo within the figure.

        :param ax: The ax object to use for the plot.
        :param p1: Name of the main player of the graph.
        :param p2: Name of the comparison player of the graph.
        :param stat: Stat that has been plotted, in string form.
        :return: Ax object with the layout changes applied.
        """
        determinant = ', a '
        if self.__position[0].lower() in ['a', 'e', 'i', 'o', 'u']:
            determinant = ', an '
        title = 'Line plot for ' + p1 + determinant + self.__position
        subtitle = ""
        if p2 is not None:
            subtitle += "Compared with " + p2 + "\n"
        subtitle += "Stat: " + stat
        plt.suptitle(subtitle, fontsize=12, y=self.__subtitle_offset, color=self.__subtitle)
        ax.set_title(title, fontsize=15, fontweight=0, color=self.__tactalyse, weight="bold", y=self.__title_offset)

        path = "graph_app/files/images/Logo_Tactalyse_Triangle.png"
        arr_img = plt.imread(path)
        im = OffsetImage(arr_img, zoom=self.__logo_size)
        ab = AnnotationBbox(im, (self.__logo_x_offset, self.__logo_y_offset), xycoords='axes fraction', frameon=False)
        ax.add_artist(ab)

        return ax

    def draw_mean_line(self, ax, player_stat_data, player):
        """
        Function for plotting a horizontal line representing the mean of the stat represented in the passed data for the
        passed player.

        :param ax: The ax object to use for the plot.
        :param player_stat_data: Series containing data for the stat to plot from the player DataFrame.
        :param player: Name of the player whose stats are represented in the passsed data.
        :return: Ax object with the mean line drawn.
        """
        mean = np.mean(player_stat_data)
        label = "Mean for " + player
        ax.axhline(y=mean, color=self.__black, linestyle="dashed", label=label)
        return ax

    def draw(self, param_map):
        """
        Main draw function of the line plot. Makes calls to helper functions to extract and process data for use in the
        plot, and returns the generated plot.

        :param param_map: Map containing all relevant data: DataFrame with all data from a player file (player_data),
        List containing the columns to graph in string form (columns), the start date of Tactalyse's services for the
        player in string form and YYYY-mm-dd format (start_date) as well as the end date (end_date), the name of the
        main player (player), the name of the comparison player (compare), and a DataFrame with all data from the
        comparison player's file (compare_data). player_data, columns and player are required, the rest is optional.
        :return: The generated line plot in byte string form.
        """
        # Extract from parameter map
        player_data, column_name, start_date, end_date, player, compare, compare_data =\
            self.__helper.extract_data_from_param_map(param_map)

        # Create plot
        fig, ax = plt.subplots(figsize=(8, 6), gridspec_kw={'top': self.__top_offset, 'bottom': self.__bottom_offset,
                                                            'left': self.__left_offset, 'right': self.__right_offset})
        ax.clear()

        # Get x-axis values
        player_x_values, year_x_values, years = self.__helper.get_xlabels(player_data)

        # Extract y-axis values from dataframe
        subcolumns = column_name.split("/")
        column_index = player_data.columns.get_loc(column_name)
        player_stat_data = player_data[player_data.columns[column_index]][::-1].reset_index(drop=True)

        # Extract y-axis sub-values from dataframe, if available
        player_sub_data, second_column = self.__helper.create_sub_plot_data(subcolumns, player_data, column_index)

        # Plot main player
        self.plot_player(ax, player_x_values, player_stat_data, player, subcolumns[0],
                         self.__tactalyse, player_sub_data, second_column, self.__player_sub_color)

        # Repeat for compare player if they exist
        if compare and isinstance(compare_data, pd.DataFrame):
            compare_x_values, _, _ = self.__helper.get_xlabels(compare_data)
            compare_stat_data = compare_data[column_name][::-1].reset_index(drop=True)

            compare_sub_data, second_column = self.__helper.create_sub_plot_data(subcolumns, compare_data, column_index)

            self.plot_player(ax, compare_x_values, compare_stat_data, compare, subcolumns[0],
                             self.__compare_color, compare_sub_data, second_column, self.__compare_sub_color)

        # Draw mean for main player main stat
        ax = self.draw_mean_line(ax, player_stat_data, player)

        # Draw lines for each season change
        ax = self.draw_seasons(ax, year_x_values, years)

        # Draw Tactalyse contract lines if start date has been passed
        if start_date:
            ax = self.draw_tactalyse_dates(ax, player_data, start_date, end_date)

        # Set the layout of the plot
        ax = self.set_layout(ax, player, compare, column_name)

        # Set legend of the graph
        plt.legend(bbox_to_anchor=(0.5, 1), loc='upper center', fontsize="small")

        # Convert to byte string
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        plt.close()
        return buffer.getvalue()

    def draw_all(self, param_map):
        """
        Function for drawing plots for all passed stats.

        :param param_map: Map containing all data required for creating the line plots.
        :return: A list of generated plots for each stat if multiple stats were passed, otherwise one graph in byte
        string form.
        """
        columns = param_map.get('columns')
        plots = []
        for column in columns:
            param_map['columns'] = column
            plots.append(self.draw(param_map))
        if len(plots) == 1:
            return plots[0]
        return plots

    @property
    def helper(self):
        return self.__helper

    @property
    def position(self):
        return self.__position
