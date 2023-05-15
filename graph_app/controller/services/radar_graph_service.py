from .abstract_service import Service
from ..connectors.data_connector import DataConnector
from ..connectors.graph_connector import GraphConnector
from flask import Response


class RadarGraphService(Service):
    def json_process(self, payload):
        """
            Function that handles a json-formatted request to the PDF generator API endpoint.

            :param payload: The json payload of the request.
            :return: A response either containing an error message, or the generated PDF in byte representation.
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
        league = form.get('league')
        player = form.get('player')
        compare = form.get('compare')

        param_map = {"type": "radar",
                     "league": league,
                     "player": player,
                     "compare": compare}

        return self.pass_data(param_map)

    def pass_data(self, param_map):
        data_connector = DataConnector()
        data_map = data_connector.get_data(param_map)

        graph_connector = GraphConnector()
        graph = graph_connector.get_data(data_map)

        return Response(graph, mimetype='image/png')
