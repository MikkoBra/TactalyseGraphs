from flask import Response

from .abstract_service import Service
from ..connectors.data_connector import DataConnector
from ..connectors.graph_connector import GraphConnector


class RandomGraphService(Service):
    """
    Class that extracts parameters from a random graph endpoint request, passes them to module connectors, and returns
    the requested random graph.
    """

    def __init__(self):
        super().__init__()
        self.__data_connector = DataConnector()
        self.__graph_connector = GraphConnector()

    def json_process(self, payload):
        """
        Function that handles a json-formatted request to the random graph API endpoint. It extracts parameters from
        the json payload, puts them in a map, and sends them on to the pass_data function to be sent to module
        connector objects. As the code is now, json_process and key_value_process are the same, since there are no
        files to be extracted for this endpoint.

        :param payload: The json payload of the API endpoint request.
        :return: A response either containing an error message, or the generated graph in byte string
        representation.
        """
        if payload is None:
            return Response("Error: invalid JSON payload.", 400, mimetype='application/json')

        graph_type = payload.get('graph-type')
        league = payload.get('league')
        player = payload.get('player')
        start_date = payload.get('start-date')
        end_date = payload.get('end-date')

        param_map = {"type": "random",
                     "graph_type": graph_type,
                     "league": league,
                     "player": player,
                     "start_date": start_date,
                     "end_date": end_date}

        return self.pass_data(param_map)

    def key_value_process(self, files, form):
        """
        Function that handles a key-value-formatted request to the random graph API endpoint. It extracts parameters
        from the form parameters, puts them in a map, and sends them on to the pass_data function to be sent to module
        connector objects. As the code is now, json_process and key_value_process are the same, since there are no
        files to be extracted for this endpoint.

        :param files: Map containing files sent with the request.
        :param form: Map containing parameters sent with the API request.
        :return: A response either containing an error message, or the generated graph in byte string
        representation.
        """
        graph_type = form.get('graph-type')
        league = form.get('league')
        player = form.get('player')
        start_date = form.get('start-date')
        end_date = form.get('end-date')

        param_map = {"type": "random",
                     "graph_type": graph_type,
                     "league": league,
                     "player": player,
                     "start_date": start_date,
                     "end_date": end_date}

        return self.pass_data(param_map)

    def pass_data(self, param_map):
        """
        Function that takes the parameter map as extracted from the API request parameters, sends it to connectors that
        send the parameters to the right modules, and gets output back from those modules.
        This class retrieves a generated graph, and returns it in a Flask response.

        :param param_map: Map containing parameters extracted from the API request.
        :return: A response either containing the generated graph in byte string representation.
        """
        data_map = self.__data_connector.get_data(param_map)

        graph = self.__graph_connector.get_data(data_map)

        response = self.create_response(data_map, graph)

        return response

    def create_response(self, data_map, graph):
        response = Response(graph, mimetype='image/png')
        player = data_map['player']
        compare = data_map.get('compare')
        response.headers['player'] = player
        if compare is not None:
            response.headers['compare'] = compare
        return response

    @property
    def data_connector(self):
        """
        Getter for the data_connector attribute of the RandomGraphService.

        :return: DataConnector object representing the RandomGraphService's connector for data modules.
        """
        return self.__data_connector

    @property
    def graph_connector(self):
        """
        Getter for the graph_connector attribute of the RandomGraphService.

        :return: GraphConnector object representing the RandomGraphService's connector for graph modules.
        """
        return self.__graph_connector
