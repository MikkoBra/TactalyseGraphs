import random

from graph_app.controller.connectors.abstract_connector import AbstractConnector
from graph_app.data.preprocessors.line_processor import LineProcessor
from graph_app.data.preprocessors.radar_processor import RadarProcessor
from graph_app.data.preprocessors.randomizer import Randomizer


class DataConnector(AbstractConnector):
    """
    Class that takes care of processing the data in incoming API requests, and returning parameter maps containing data
    that's usable by the graph classes. It does minimal data processing in the form of randomizing headers representing
    the graph type in the case of a random graph request. It should not be used for actual data processing, as it is
    part of the controller module in the MVC pattern.
    """

    def __init__(self):
        super().__init__()
        self.__randomizer = Randomizer()
        self.__radar_processor = RadarProcessor()
        self.__line_processor = LineProcessor()

    def random_graph_choice(self, param_map):
        """
        Function for setting the "graph_type" to a random graph from the graph generator. Possible types are contained
        in the "types" list. If graph_type is predefined, the input parameter map remains unchanged.

        :param param_map: Map containing at least the 'type' key, and optionally the 'graph_type' key.
        :return: The same map, with 'graph_type' set to random if it was not defined.
        :raises: ValueError when the passed 'graph_type' value was not known to the system.
        """
        types = ['radar', 'line']
        if param_map.get('type') not in types:
            if not param_map.get('graph_type'):
                param_map['graph_type'] = random.choice(types)
            elif param_map.get('graph_type') not in types:
                raise ValueError('The passed graph type for random graphs is not known. Please choose radar or line.')
        return param_map

    def set_random_data(self, param_map):
        """
        Function that randomizes all unfilled parameters of a random graph API request, using the Randomizer class from
        the data module. See set_random_parameters() from Randomizer for more information.

        :param param_map: Map containing all parameters passed to the API endpoint.
        :return: A map with the values of all keys that were missing filled in with randomly selected values.
        """
        param_map = self.random_graph_choice(param_map)
        types = ['radar', 'line']
        if param_map.get('type') not in types:
            param_map['type'] = param_map['graph_type']
            return self.__randomizer.set_random_parameters(param_map)
        else:
            return param_map

    def get_data(self, param_map):
        """
        Function that calls upon the appropriate data retrieval function depending on either the passed graph_type, or
        the randomized graph_type.

        :param param_map: Map containing all parameters passed to the API endpoint.
        :return: Map containing all data needed for generating the specified graph.
        """
        param_map = self.set_random_data(param_map)
        if param_map.get('type') == 'radar':
            return self.get_radar_data(param_map)
        elif param_map.get('type') == 'line':
            return self.get_line_data(param_map)

    def get_radar_data(self, param_map):
        """
        Function that takes a map containing a football league's data along with required parameters, and extracts the
        relevant data for a radar chart. This is done using a RadarProcessor instance, which has all functions needed
        for extracting the data into a parameter map.

        :param param_map: Map containing all parameters passed to the API endpoint, along with potentially randomized
        data.
        :return: Map containing all data needed for generating the radar chart.
        """
        return self.__radar_processor.extract_radar_data(param_map)

    def get_line_data(self, param_map):
        """
        Function that takes a map containing a football player's data along with required parameters, and extracts the
        relevant data for a line plot. This is done using a LineProcessor instance, which has all functions needed
        for extracting the data into a parameter map.

        :param param_map: Map containing all parameters passed to the API endpoint, along with potentially randomized
        data.
        :return: Map containing all data needed for generating the line plot.
        """
        return self.__line_processor.extract_line_data(param_map)

    @property
    def randomizer(self):
        """
        Getter for the randomizer attribute of the DataConnector.

        :return: Randomizer object representing the DataConnector's randomizer.
        """
        return self.__randomizer

    @property
    def radar_processor(self):
        """
        Getter for the radar_processor attribute of the DataConnector.

        :return: RadarProcessor object representing the DataConnector's data processor for radar charts.
        """
        return self.__radar_processor

    @property
    def line_processor(self):
        """
        Getter for the line_processor attribute of the DataConnector.

        :return: LineProcessor object representing the DataConnector's data processor for line charts.
        """
        return self.__line_processor
