from .abstract_service import Service
from ..connectors.data_connector import DataConnector
from ..connectors.graph_connector import GraphConnector
from flask import Response


class RandomGraphService(Service):
    def json_process(self, payload):
        """
            Function that handles a json-formatted request to the PDF generator API endpoint.

            :param payload: The json payload of the request.
            :return: A response either containing an error message, or the generated PDF in byte representation.
            """
        if payload is None:
            return Response("Error: invalid JSON payload.", 400, mimetype='application/json')

        graph_type = payload.get('graph-type')
        league = payload.get('league')
        player = payload.get('player')
        start_date = payload.get('start-date')
        end_date = payload.get('end-date')

        param_map = {"graph_type": graph_type,
                     "league": league,
                     "player": player,
                     "start_date": start_date,
                     "end_date": end_date}

        return self.pass_data(param_map)

    def key_value_process(self, files, form):
        graph_type = form.get('graph-type')
        league = form.get('league')
        player = form.get('player')
        start_date = form.get('start-date')
        end_date = form.get('end-date')

        param_map = {"graph_type": graph_type,
                     "league": league,
                     "player": player,
                     "start_date": start_date,
                     "end_date": end_date}

        return self.pass_data(param_map)

    def pass_data(self, param_map):
        data_connector = DataConnector()
        data = data_connector.get_data(param_map)

        graph_connector = GraphConnector()
        graph = graph_connector.get_graph(data)

        return Response(graph, mimetype='image/png')
