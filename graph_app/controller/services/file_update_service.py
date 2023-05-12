from .abstract_service import Service
from ...data.file_updater import FileUpdater
from flask import request, Response
import base64


class FileUpdateService(Service):

    def json_process(self, payload):
        """
            Function that handles a json-formatted request to the PDF generator API endpoint.

            :param payload: The json payload of the request.
            :return: A response either containing an error message, or the generated PDF in byte representation.
            """
        if payload is None:
            return Response("Error: invalid JSON payload.", 400, mimetype='application/json')

        files = []
        for file_data in payload['files']:
            file_contents = base64.b64decode(file_data)
            files.append(file_contents)

        param_map = {"new_files": files}

        return self.pass_data(param_map)

    def key_value_process(self, files, form):
        league_files = request.files.getlist('league-files')
        player_files = request.files.getlist('player-files')
        param_map = {"league_files": league_files, "player_files": player_files}
        return self.pass_data(param_map)

    def pass_data(self, param_map):
        updater = FileUpdater()
        updater.update_league_files(param_map.get("league_files"))
        updater.update_player_files(param_map.get("player_files"))
        return Response("Files successfully updated.", 200, mimetype='application/json')
