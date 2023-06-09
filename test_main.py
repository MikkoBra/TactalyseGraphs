import io

from PIL import Image

from graph_app.controller.connectors.data_connector import DataConnector
from graph_app.controller.connectors.graph_connector import GraphConnector


def show_plot(bytes):
    stream = io.BytesIO(bytes)

    # Load the image data using Pillow's Image.open function
    image = Image.open(stream)

    # Display the image using Pillow's Image.show function
    image.show()


def test_line():
    param_map = {
        "type": "line",
        # "compare": "C. Cathcart",
        # "player": "Kiko Femenía",
        # "stat": "Defensive duels / won",
        # "start_date": "2016-09-25",
        # "end_date": "2020-12-23"
    }

    data_connector = DataConnector()
    data_map = data_connector.get_data(param_map)

    graph_connector = GraphConnector()
    graph = graph_connector.get_data(data_map)
    show_plot(graph)


def test_radar():
    param_map = {"type": "radar",
                 # "league": "MLS",
                 # "player": "E. Reynoso",
                 # "compare": "F. Torres"
                 }

    data_connector = DataConnector()
    data_map = data_connector.get_data(param_map)

    graph_connector = GraphConnector()
    graph = graph_connector.get_data(data_map)
    show_plot(graph)


def test_random():
    param_map = {"type": "random",
                 "graph_type": "line"}

    data_connector = DataConnector()
    data_map = data_connector.get_data(param_map)

    graph_connector = GraphConnector()
    graph = graph_connector.get_data(data_map)
    show_plot(graph)


if __name__ == "__main__":
    """
    This function tests the functionality of the graph generator without relying on endpoints. It uses the same classes
    and functions, but can be run as a local script. It was mostly used for testing visual output without having to
    dockerize our code every time. It is not part of the graph generator code, and its removal would not affect
    functionality. It was left in for convenience of future developers.
    """
    test_line()
    test_radar()
    # test_random()
