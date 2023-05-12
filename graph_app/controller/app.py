from flask import Flask, request
from .services.file_update_service import FileUpdateService
from .services.random_graph_service import RandomGraphService
from .services.line_graph_service import LineGraphService
from .services.radar_graph_service import RadarGraphService
import os

app = Flask(__name__)


@app.route('/graph', methods=["PUT"])
def update_files():
    """
    API endpoint for generating a football report based on query parameters.
    The following parameters must be included in the request:
    - league-file: an Excel file containing football league data.
    - player-file: an Excel file containing a player's match data.
    - player-name: a string representing the name of the player. Must exist within the league file.
    Optional parameters include:
    - start-date: start date of Tactalyse's services for the player.
    - end-date: end date of Tactalyse's services for the player.

    :return: A response either containing an error message, or the generated PDF in byte representation.
    """
    service = FileUpdateService()
    if request.is_json:
        return service.json_process(request.get_json())
    else:
        return service.key_value_process(request.files, request.form)


@app.route('/graph', methods=["POST"])
def random_graph():
    """
    API endpoint for generating a football report based on query parameters.
    The following parameters must be included in the request:
    - league-file: an Excel file containing football league data.
    - player-file: an Excel file containing a player's match data.
    - player-name: a string representing the name of the player. Must exist within the league file.
    Optional parameters include:
    - start-date: start date of Tactalyse's services for the player.
    - end-date: end date of Tactalyse's services for the player.

    :return: A response either containing an error message, or the generated PDF in byte representation.
    """
    service = RandomGraphService()
    if request.is_json:
        return service.json_process(request.get_json())
    else:
        return service.key_value_process(request.files, request.form)


@app.route('/graph/radar', methods=["POST"])
def radar_graph():
    """
    API endpoint for generating a football report based on query parameters.
    The following parameters must be included in the request:
    - league-file: an Excel file containing football league data.
    - player-file: an Excel file containing a player's match data.
    - player-name: a string representing the name of the player. Must exist within the league file.
    Optional parameters include:
    - start-date: start date of Tactalyse's services for the player.
    - end-date: end date of Tactalyse's services for the player.

    :return: A response either containing an error message, or the generated PDF in byte representation.
    """
    service = RadarGraphService()
    if request.is_json:
        return service.json_process(request.get_json())
    else:
        return service.key_value_process(request.files, request.form)


@app.route('/graph/line', methods=["POST"])
def line_graph():
    """
    API endpoint for generating a football report based on query parameters.
    The following parameters must be included in the request:
    - league-file: an Excel file containing football league data.
    - player-file: an Excel file containing a player's match data.
    - player-name: a string representing the name of the player. Must exist within the league file.
    Optional parameters include:
    - start-date: start date of Tactalyse's services for the player.
    - end-date: end date of Tactalyse's services for the player.

    :return: A response either containing an error message, or the generated PDF in byte representation.
    """
    service = LineGraphService()
    if request.is_json:
        return service.json_process(request.get_json())
    else:
        return service.key_value_process(request.files, request.form)


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, port=5001)
