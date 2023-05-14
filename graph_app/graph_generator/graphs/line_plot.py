import io
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pandas as pd

from .abstract_models import Graph

matplotlib.use('TkAgg')


class LinePlot(Graph):
    __position = ''
    __tactalyse = "#EC4A24"
    __player_color = '#000000'
    __compare_color = '#646464'

    def __init__(self, param_map):
        player_pos = param_map.get('main_pos')
        if player_pos:
            self.__position = player_pos

    def dates_to_int(self, dates):
        return list(range(len(dates)))

    def get_xlabels(self, data):
        dates = pd.to_datetime(data["Date"], format='%Y-%m-%d')
        dates = dates.sort_values()
        dates_x_values = self.dates_to_int(dates)
        year_x_values = np.where(dates.dt.year.diff() != 0)[0]
        date_strings = dates.iloc[year_x_values].dt.strftime('%Y-%m-%d')
        years = date_strings.str.slice(start=2, stop=4)

        return dates_x_values, year_x_values, years

    def create_plot(self, ax, dates_x_values, data, color, label, order):
        sns.lineplot(x=dates_x_values, y=data, ax=ax, color=color, label=label, zorder=order, linewidth=1, marker='o',
                     markersize=3)

    def draw_years(self, ax, column_name, year_x_values, years):
        plt.xlabel("Year")
        ax.set(title=column_name, xticks=year_x_values, xticklabels=years)
        no_label = False
        for year in year_x_values:
            if no_label:
                ax.axvline(x=year, linestyle="dashed", color='#B5B3FF')
            else:
                ax.axvline(x=year, linestyle="dashed", color='#B5B3FF', label="Year")
                no_label = True
        return ax

    def draw_tactalyse_dates(self, ax, data, start_date, end_date):
        dates = pd.to_datetime(data['Date'], format='%Y-%m-%d')[::-1]
        start = pd.Timestamp(start_date)
        end = pd.Timestamp(end_date)
        print(start_date)
        start_x = dates.searchsorted(start, side='left') - 1
        end_x = dates.searchsorted(end, side='left') - 1

        print(start_x)
        print(end_x)
        if 0 <= start_x <= len(dates):
            ax.axvline(x=start_x, linestyle="-", label="Tactalyse contract", color=self.__tactalyse)
            if start_x < end_x <= len(dates):
                ax.axvline(x=end_x, linestyle="-", color=self.__tactalyse)
        return ax

    def draw(self, param_map):
        player_data = param_map.get('player_data')
        column_name = param_map.get('columns')
        start_date = param_map.get('start_date')
        end_date = param_map.get('end_date')
        player = param_map.get('player')
        compare = param_map.get('compare')
        compare_data = param_map.get('compare_data')

        fig, ax = plt.subplots()
        ax.clear()

        player_x_values, year_x_values, years = self.get_xlabels(player_data)
        player_stat_data = player_data[column_name]
        label = column_name + " for " + player
        self.create_plot(ax, player_x_values, player_stat_data, self.__player_color, label, order=1)

        if compare and isinstance(compare_data, pd.DataFrame):
            compare_x_values, x, y = self.get_xlabels(compare_data)
            compare_stat_data = compare_data[column_name]
            label = column_name + " for " + compare
            self.create_plot(ax, compare_x_values, compare_stat_data, self.__compare_color, label, order=0)

        mean = np.mean(player_stat_data)
        label = "Mean for " + player
        ax.axhline(y=mean, color='black', linestyle="dashed", label=label)

        ax = self.draw_years(ax, column_name, year_x_values, years)

        if start_date:
            ax = self.draw_tactalyse_dates(ax, player_data, start_date, end_date)

        ax.legend(fontsize='small')
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        plt.close()
        return buffer.getvalue()

    def draw_all(self, param_map):
        columns = param_map.get('columns')
        plots = []
        for column in columns:
            param_map['columns'] = column
            plots.append(self.draw(param_map))
        if len(plots) == 1:
            return plots[0]
        return plots
