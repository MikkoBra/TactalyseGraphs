import io
from math import ceil

import matplotlib.pyplot as plt
import numpy as np

from .abstract_models import Graph


class RadarChart(Graph):
    """ Class representing a default Graph """

    def __init__(self, param_map):
        player_pos = param_map.get('main_pos_long')
        if player_pos:
            self.__position = player_pos

    def get_player_data(self, column_names, param_map, compare=False):
        if not compare:
            player_data = param_map.get('player_row')
            player = param_map.get('player')
        else:
            player_data = param_map.get('compare_row')
            if player_data is None:
                return None, None, None
            player = param_map.get('compare')
        # create a list of the values for each category
        player_data = player_data[column_names]
        values = player_data.iloc[0].tolist()
        # close the loop for the radar chart
        values += values[:1]
        return player_data, player, values

    def create_radar_chart(self, column_names, p1_values, p2_values):
        # calculate the angles for each category
        angles = [n / float(len(column_names)) * 2 * np.pi for n in range(len(column_names))]
        angles += angles[:1]

        # create the radar chart
        fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
        ax.set_theta_offset(np.pi / 2)
        ax.set_theta_direction(-1)
        ax.spines['polar'].set_visible(False)
        max_val = max(p1_values)
        if p2_values is not None:
            max_val = max(max_val, max(p2_values))
        ax.set_ylim(0, ceil(max_val / 10) * 10)
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(column_names)
        ax.yaxis.grid(True)
        return fig, ax, angles

    def plot_player(self, ax, player_values, angles):
        ax.plot(angles, player_values, linewidth=1, linestyle='solid')
        ax.fill(angles, player_values, 'b', alpha=0.1)
        return ax

    def set_layout(self, ax, p1):
        ax.set_title('Radar chart for ' + p1 + ', a ' + self.__position)
        return ax

    def draw(self, param_map):
        column_names = param_map.get('columns')

        p1_data, p1, p1_values = self.get_player_data(column_names, param_map)
        p2_data, p2, p2_values = self.get_player_data(column_names, param_map, True)

        fig, ax, angles = self.create_radar_chart(column_names, p1_values, p2_values)

        # plot the values on the radar chart
        ax = self.plot_player(ax, p1_values, angles)
        if p2_values is not None:
            ax = self.plot_player(ax, p2_values, angles)

        ax = self.set_layout(ax, p1)

        # Save the plot to a file
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        return buffer.getvalue()

    def draw_all(self, param_map):
        return self.draw(param_map)
