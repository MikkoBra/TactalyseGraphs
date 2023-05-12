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

    def draw(self, param_map):
        data = param_map.get('player_row')
        column_names = param_map.get('columns')
        player = data.iloc[0]['Player']
        # create a list of the values for each category
        data = data[column_names]
        values = data.iloc[0].tolist()
        # close the loop for the radar chart
        values += values[:1]

        # calculate the angles for each category
        angles = [n / float(len(column_names)) * 2 * np.pi for n in range(len(column_names))]
        angles += angles[:1]

        # create the radar chart
        fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
        ax.set_theta_offset(np.pi / 2)
        ax.set_theta_direction(-1)
        ax.spines['polar'].set_visible(False)
        max_val = max(values)
        ax.set_ylim(0, ceil(max_val / 10) * 10)
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(column_names)
        ax.yaxis.grid(True)
        ax.set_title('Radar chart for ' + player + ', a ' + self.__position)

        # plot the values on the radar chart
        ax.plot(angles, values, linewidth=1, linestyle='solid')
        ax.fill(angles, values, 'b', alpha=0.1)

        # Save the plot to a file
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        return buffer.getvalue()

    def draw_all(self, param_map):
        return self.draw(param_map)
