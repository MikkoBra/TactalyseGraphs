import random

from graph_app.controller.connectors.abstract_connector import AbstractConnector
from graph_app.data.preprocessors.line_processor import LineProcessor
from graph_app.data.preprocessors.radar_processor import RadarProcessor
from graph_app.data.preprocessors.randomizer import Randomizer


class DataConnector(AbstractConnector):

    def get_data(self, param_map):
        types = ['radar', 'line']
        if param_map.get('type') not in types:
            if param_map.get('graph_type'):
                print(param_map.get('graph_type'))
                param_map['type'] = param_map.get('graph_type')
            else:
                param_map['type'] = random.choice(types)
            param_map = self.set_random_data(param_map)

        if param_map.get('type') == 'radar':
            return self.get_radar_data(param_map)
        elif param_map.get('type') == 'line':
            return self.get_line_data(param_map)

    def set_random_data(self, param_map):
        """
        Function that randomizes all unfilled parameters

        :param param_map: Map containing all passed parameters
        :return: A map with all keys that were missing values filled in with random values
        """
        randomizer = Randomizer()
        return randomizer.set_random_parameters(param_map)

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
