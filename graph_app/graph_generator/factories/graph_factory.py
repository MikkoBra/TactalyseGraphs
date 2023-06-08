import random

from .abstract_graph_factory import AbstractGraphFactory
from ..graphs.line_plot import LinePlot
from ..graphs.radar_chart import RadarChart


class GraphFactory(AbstractGraphFactory):
    """ Class representing a factory for twitter bot plots"""

    def create_instance(self, param_map):
        graph_type = param_map.get('type')
        if graph_type == 'line':
            return LinePlot(param_map)
        elif graph_type == 'radar':
            return RadarChart(param_map)
        else:
            graph = self.random_graph(param_map)
            return graph

    def random_graph(self, params):
        """
        Function for generating a random graph instance to output from the factory.

        :param params:
        :return: The randomly chosen Graph object.
        """
        graphs = {'line': LinePlot(params),
                  'radar': RadarChart(params)}
        random_graph = random.choice(list(graphs.values()))
        return random_graph
