from graph_app.data.preprocessors.line_processor import LineProcessor
from graph_app.data.preprocessors.radar_processor import RadarProcessor
from graph_app.controller.connectors.abstract_connector import AbstractConnector
import random


class DataConnector(AbstractConnector):
    def random_choice(self):
        graphs = ['radar', 'line']
        return random.choice(graphs)

    def get_data(self, param_map):
        if param_map['type'] == 'random':
            param_map['type'] = self.random_choice()
        graph_type = param_map['type']

        if graph_type == 'radar':
            return self.get_radar_data(param_map)
        elif graph_type == 'line':
            return self.get_line_data(param_map)

    def get_radar_data(self, param_map):
        """
        Function that takes a football league's data along with required parameters, and extracts the relevant data for
        a radar chart.
        """
        processor = RadarProcessor()
        return processor.extract_radar_data(param_map)

    def get_line_data(self, param_map):
        """
        Function that takes a football player's data along with required parameters, and extracts the relevant data for a
        line plot.
        """
        processor = LineProcessor()
        return processor.extract_line_data(param_map)
