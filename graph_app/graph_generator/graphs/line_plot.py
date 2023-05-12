import io
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

from .abstract_models import Graph

matplotlib.use('TkAgg')


class LinePlot(Graph):
    __position = ''

    def __init__(self, param_map):
        player_pos = param_map.get('main_pos')
        if player_pos:
            self.__position = player_pos

    def get_xlabels(self, date):
        date = date.str.slice(start=2, stop=4)
        unique_dates = date.unique()
        unique_date_int = [int(i) for i in unique_dates]
        unique_date_int_plus_one = [x + 1 for x in unique_date_int]
        labels = []
        for i in range(len(unique_dates)):
            labels.append(str(unique_date_int[i]) + "/" + str(unique_date_int_plus_one[i]))
        start_years = []
        for i in range(len(unique_dates)):
            numbers = date[date == unique_dates[i]]
            start_years.append(len(date) - numbers.index[len(numbers) - 1] - 1)
        start_years.reverse()
        locations = []
        for i in range(len(start_years)):
            if i != len(start_years) - 1:
                locations.append((start_years[i] + start_years[i + 1]) / 2)
            else:
                locations.append((start_years[i] + len(date)) / 2)
        locations.reverse()
        start_years.reverse()

        return labels, locations, start_years

    def draw(self, param_map):
        data = param_map.get('player_data')
        column_name = param_map.get('columns')
        temp_start_date = 20
        temp_end_date = 144
        date = data["Date"]
        labels, locations, start_years = self.get_xlabels(date)
        data = data[column_name]
        fig, ax = plt.subplots()
        ax.clear()
        sns.lineplot(x=date, y=data, marker='o', ax=ax)
        ax.set(title=column_name, xticks=locations, xticklabels=labels)
        mean = np.mean(data)
        sns.lineplot(x=date, y=mean, ax=ax, linestyle="solid", label="Mean", color="black")
        for i in start_years:
            ax.axvline(x=i, linestyle="dashed", color='g')
        ax.axvline(x=temp_start_date, linestyle="dashed", label="Tactalyse start & end date", color='r')
        ax.axvline(x=temp_end_date, linestyle="dashed", color='r')
        ax.legend()
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
