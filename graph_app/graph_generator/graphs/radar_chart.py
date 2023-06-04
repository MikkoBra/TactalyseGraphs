import io

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.offsetbox import AnnotationBbox, OffsetImage

from .abstract_models import Graph


class RadarChart(Graph):
    """ Class representing a default Graph """
    __tactalyse = "#e51e24"
    __player_fill = "#F7B6A7"
    __compare = "#4A24EC"
    __compare_fill = "#B6A7F7"
    __title = "#D46508"
    __subtitle = "#5E5E5E"
    __left_pos = 0.19
    __bottom_pos = 0.1
    __plot_w = 0.6
    __plot_h = 0.62
    __num_labels = 6.0
    __title_offset = 1.33
    __subtitle_offset = 0.92

    def __init__(self, param_map):
        player_pos = param_map.get('player_pos')
        if player_pos:
            self.__position = player_pos
        else:
            self.__position = "Player"

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

    def create_radar_chart(self, p1_values, p2_values, scales):
        # calculate the angles for each category
        n = len(p1_values) - 1
        angles = np.linspace(0, 2 * np.pi, n, endpoint=False).tolist()
        angles += angles[:1]  # Close the loop

        # create the radar chart
        fig = plt.figure(figsize=(8, 7))
        ax = fig.add_axes([self.__left_pos, self.__bottom_pos, self.__plot_w, self.__plot_h], projection='polar')

        p1_data_normalized = [d / scale for d, scale in zip(p1_values, scales)]
        p1_data_normalized += p1_data_normalized[:1]  # Close the loop

        p2_data_normalized = None
        if p2_values is not None:
            p2_data_normalized = [d / scale for d, scale in zip(p2_values, scales)]
            p2_data_normalized += p2_data_normalized[:1]  # Close the loop

        return fig, ax, angles, p1_data_normalized, p2_data_normalized

    def get_scale_labels(self, scales, num_labels):
        labels = []
        for scale in scales:
            y_vals = np.linspace(0, scale, int(num_labels)).tolist()
            fraction = scale / float(num_labels)
            if fraction >= 1:
                y_vals = [round(value, 2) for value in y_vals]
            else:
                decimals = 0
                while fraction < 1.0:
                    fraction *= 10
                    decimals += 1
                y_vals = [round(value, decimals + 1) for value in y_vals]
            labels.append(y_vals)
        return labels

    def check_zeroes(self, player_vals):
        all_zeroes = all(element == 0 for element in player_vals)
        return all_zeroes

    def plot_player(self, ax, player, player_values, angles, color):
        ax.plot(angles, player_values, linewidth=1, linestyle='solid', label=player, color=color)
        ax.fill(angles, player_values, alpha=0.25, color=color)
        return ax

    def print_stat_labels(self, ax, angles, column_names):
        ax.set_theta_offset(np.pi / 2)
        ax.set_theta_direction(-1)
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels([])

        for label, angle, column_name in zip(ax.get_xticklabels(), angles, column_names):
            x, y = label.get_position()
            # Increase offset with respect to distance from vertical (angle = 0 or pi)
            vertical = np.pi
            if angle < abs(np.pi - angle):
                vertical = 0.0
            elif abs(2 * np.pi - angle) < abs(angle - np.pi):
                vertical = 2 * np.pi
            # length of column (label) name increases distance from plot for readability
            offset = (0.1 + 0.01 * len(column_name)) * abs(angle - vertical) / (np.pi / 2)
            lab = ax.text(x, y - offset, column_name, transform=label.get_transform(),
                          ha=label.get_ha(), va=label.get_va())
        return ax

    def clear_grid(self, ax):
        ax.set_yticklabels([])
        ax.grid(False)

        ax.set_yticks([])
        ax.yaxis.grid(False)
        ax.xaxis.grid(False)

        # Remove spines
        ax.spines["start"].set_color("none")
        ax.spines["polar"].set_color("none")
        return ax

    def print_radial_axis_lines(self, ax, num_scales):
        h_angles = np.linspace(0, 2 * np.pi)
        h0 = np.zeros(len(h_angles))
        ticks = np.linspace(0, 1, num_scales)

        rad_axis_lines = [h0]
        for i in range(1, len(ticks)):
            rad_axis_lines.append(np.ones(len(h_angles)) * ticks[i])
        for line in rad_axis_lines:
            ax.plot(h_angles, line, c='gray', lw=0.5)
        return ax

    def print_angular_axis_lines(self, ax, angles, scale_labels):
        # max_scales = []
        # for scales in scale_labels:
        #     max_scales.append(scales[-1])
        # # Print lines going from center to max radius, which is max(player_vals)
        # radius = max(max_scales)
        for angle in angles[:-1]:
            ax.plot([angle, angle], [0, 1], c='gray', lw=0.5)
        return ax

    def print_y_scale_values(self, ax, angles, scale_labels):
        for i, label in enumerate(scale_labels):
            angle = angles[i]

            for j, value in enumerate(label):
                # Don't print 0 to avoid clutter in middle
                if value == 0.00:
                    continue
                # Calculate the position of the label
                x = angle
                y = (1 / (len(label) - 1)) * j

                # Place the label on the plot
                ax.text(x, y, str(value), ha='center', va='center', fontsize=8, color='black')
        return ax

    def print_scales(self, ax, angles, scale_labels, player_vals, compare_vals=None):
        if compare_vals is None or max(player_vals) < max(compare_vals):
            return ax

        ax = self.clear_grid(ax)
        num_scales = len(scale_labels[0])
        ax = self.print_radial_axis_lines(ax, num_scales)
        ax = self.print_y_scale_values(ax, angles, scale_labels)
        ax = self.print_angular_axis_lines(ax, angles, player_vals)

        return ax

    def set_layout(self, ax, p1, p2, team, matches, country):
        path = "graph_app/files/images/Logo_Tactalyse_Triangle.png"
        arr_img = plt.imread(path)
        im = OffsetImage(arr_img, zoom=0.4)
        ab = AnnotationBbox(im, (1.3, 1.35), xycoords='axes fraction', frameon=False)
        ax.add_artist(ab)

        determinant = ', a '
        if self.__position[0].lower() in ['a', 'e', 'i', 'o', 'u']:
            determinant = ', an '
        title = 'Radar chart for ' + p1 + determinant + self.__position
        subtitle = ""
        subtitle += "Birth country: " + country + "\n"
        subtitle += "Team: " + str(team) + "\n"
        subtitle += "Matches played: " + str(matches) + "\n"
        if p2 is not None:
            subtitle += "Compared with " + p2 + "\n"
        plt.suptitle(subtitle, fontsize=12, y=self.__subtitle_offset, color=self.__subtitle)
        ax.set_title(title, fontsize=15, fontweight=0, color=self.__tactalyse, weight="bold", y=self.__title_offset)

        return ax

    def draw(self, param_map):
        column_names = param_map.get('columns')

        p1_data, p1, p1_values = self.get_player_data(column_names, param_map)
        p2_data, p2, p2_values = self.get_player_data(column_names, param_map, True)

        scales = param_map.get('scales')
        fig, ax, angles, p1_values, p2_values = self.create_radar_chart(p1_values, p2_values, scales)

        # plot the values on the radar chart
        if self.check_zeroes(p1_values):
            raise ValueError("Player " + p1 + " had only NA entries.")
        ax = self.plot_player(ax, p1, p1_values, angles, self.__tactalyse)

        scale_labels = self.get_scale_labels(scales, self.__num_labels)
        ax = self.print_scales(ax, angles, scale_labels, p1_values)

        if p2_values is not None:
            if self.check_zeroes(p2_values):
                raise ValueError("Player " + p2 + " had only NA entries.")
            ax = self.plot_player(ax, p2, p2_values, angles, self.__compare)
            ax = self.print_scales(ax, angles, scale_labels, p2_values, p1_values)

        ax = self.print_stat_labels(ax, angles, column_names)

        team = param_map.get('player_row')['Team'].iloc[0]
        matches = param_map.get('player_row')['Matches played'].iloc[0]
        country = param_map.get('player_row')['Birth country'].iloc[0]
        ax = self.set_layout(ax, p1, p2, team, matches, country)

        plt.legend(bbox_to_anchor=(1.1, 1.15), loc='upper center')

        # Save the plot to a file
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        return buffer.getvalue()

    def draw_all(self, param_map):
        return self.draw(param_map)

    @property
    def position(self):
        return self.__position
