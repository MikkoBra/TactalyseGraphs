from flask import Response

from .abstract_service import Service
from ..connectors.data_connector import DataConnector
from ..connectors.graph_connector import GraphConnector


class RadarGraphService(Service):
    """
    Class that extracts parameters from a radar chart endpoint request, passes them to module connectors, and returns
    the requested radar chart.
    """

    def __init__(self):
        super().__init__()
        self.__data_connector = DataConnector()
        self.__graph_connector = GraphConnector()

    def json_process(self, payload):
        """
        Function that handles a json-formatted request to the radar chart API endpoint. It extracts parameters from
        the json payload, puts them in a map, and sends them on to the pass_data function to be sent to module
        connector objects. As the code is now, json_process and key_value_process are the same, since there are no
        files to be extracted for this endpoint.

        :param payload: The json payload of the API endpoint request.
        :return: A response either containing an error message, or the generated graph in byte string
        representation.
        """
        if payload is None:
            return Response("Error: invalid JSON payload.", 400, mimetype='application/json')

        league = payload.get('league')
        player = payload.get('player')
        compare = payload.get('compare')

        param_map = {"type": "radar",
                     "league": league,
                     "player": player,
                     "compare": compare}

        return self.pass_data(param_map)

    def key_value_process(self, files, form):
        """
        Function that handles a key-value-formatted request to the radar chart API endpoint. It extracts parameters from
        the form parameters, puts them in a map, and sends them on to the pass_data function to be sent to module
        connector objects. As the code is now, json_process and key_value_process are the same, since there are no
        files to be extracted for this endpoint.

        :param files: Map containing files sent with the request.
        :param form: Map containing parameters sent with the API request.
        :return: A response either containing an error message, or the generated graph in byte string
        representation.
        """
        if form is None:
            return Response("Error: invalid form, was received as None.", 400, mimetype='application/json')

        league = form.get('league')
        player = form.get('player')
        compare = form.get('compare')

        param_map = {"type": "radar",
                     "league": league,
                     "player": player,
                     "compare": compare}

        return self.pass_data(param_map)

    def pass_data(self, param_map):
        """
        Function that takes the parameter map as extracted from the API request parameters, sends it to connectors that
        send the parameters to the right modules, and gets output from those modules back.
        This class retrieves a generated graph, and returns it in a Flask response.

        :param param_map: Map containing parameters extracted from the API request.
        :return: A response either containing the generated graph in byte string representation.
        """
        data_map = self.__data_connector.get_data(param_map)
        graph = self.__graph_connector.get_data(data_map)

        return Response(graph, mimetype='image/png')

    @property
    def data_connector(self):
        """
        Getter for the data_connector attribute of the RadarGraphService.

        :return: DataConnector object representing the RadarGraphService's connector for data modules.
        """
        return self.__data_connector

    @property
    def graph_connector(self):
        """
        Getter for the graph_connector attribute of the RadarGraphService.

        :return: GraphConnector object representing the RadarGraphService's connector for graph modules.
        """
        return self.__graph_connector
