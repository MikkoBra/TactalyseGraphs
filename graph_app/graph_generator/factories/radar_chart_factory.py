from ..factories.abstract_graph_factory import AbstractGraphFactory
from ..graphs.radar_chart import RadarChart


class RadarChartFactory(AbstractGraphFactory):
    """ Class representing a factory for polar plots of each player position """

    def create_instance(self, param_map):
        graph_type = param_map.get('type')
        params = param_map.get('params')
        if graph_type != 'Default':
            print("To be implemented.")
            return RadarChart(params)
        else:
            return RadarChart({})
