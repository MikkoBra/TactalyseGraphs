from flask import Flask, request
from flask_wtf.csrf import CSRFProtect

from .services.file_update_service import FileUpdateService
from .services.line_graph_service import LineGraphService
from .services.radar_graph_service import RadarGraphService
from .services.random_graph_service import RandomGraphService

csrf = CSRFProtect()
app = Flask(__name__)
csrf.init_app(app)

@app.route('/graph', methods=["PUT"])
def update_files():
    """
    API endpoint for updating the local files used to generate graphs. Currently lacking functionality, i.e. does not
    work. The intention is to write functions that extract all league files from the passed league file list, and
    replace all existing league files in the file folder with those. Same process for player files.

    :return: A response either containing an error message, or a success message.
    """
    service = FileUpdateService()
    if request.is_json:
        return service.json_process(request.get_json())
    else:
        return service.key_value_process(request.files, request.form)


@app.route('/graph', methods=["POST"])
def random_graph():
    """
    API endpoint for generating a random graph, optionally based on query parameters.
    Optional parameters include:
    - graph-type: type of graph to randomize and return. Currently supports line and radar plots.
    - league: league file to use for randomized radar charts.
    - player: player to use for randomized line plots.
    - start-date: start of tactalyse's contract with the specified player for the random line plot.
    - end-date: end of tactalyse's contract with the specified player for the random line plot.

    :return: A response either containing an error message, or the generated graph PNG in byte representation.
    """
    service = RandomGraphService()
    if request.is_json:
        return service.json_process(request.get_json())
    else:
        return service.key_value_process(request.files, request.form)


@app.route('/graph/radar', methods=["POST"])
def radar_graph():
    """
    API endpoint for generating a radar graph, based on query parameters.
    The following parameters are randomized if not passed, but required for graph generation:
    - league: name of the league to generate a radar graph for. Must be the same as the name of the league file.
    - player: name of the player to graph. Must exist in the league file.
    Optional parameters include:
    - compare: name of the comparison player to graph. Must exist in the league file.

    :return: A response either containing an error message, or the generated graph PNG in byte representation.
    """
    service = RadarGraphService()
    if request.is_json:
        return service.json_process(request.get_json())
    else:
        return service.key_value_process(request.files, request.form)


@app.route('/graph/line', methods=["POST"])
def line_graph():
    """
    API endpoint for generating a line graph, based on query parameters.
    The following parameters are randomized if not passed, but required for graph generation:
    - player: name of the player to graph. Must exist among the player files in the files folder.
    - stat: stat to graph for the player. Must exist in the player file.
    Optional parameters include:
    - compare: name of the comparison player to graph. Must exist among the player files in the files folder.
    - league: name of the football league the player plays in.
    - start-date: start of tactalyse's contract with the specified player.
    - end-date: end of tactalyse's contract with the specified player.
    :return: A response either containing an error message, or the generated graph PNG in byte representation.
    """
    service = LineGraphService()
    if request.is_json:
        return service.json_process(request.get_json())
    else:
        return service.key_value_process(request.files, request.form)


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, port=5001)
