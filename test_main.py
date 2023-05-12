from graph_app.controller.connectors.data_connector import DataConnector
from graph_app.controller.connectors.graph_connector import GraphConnector
import io
from PIL import Image


def show_plot(bytes):
    stream = io.BytesIO(bytes)

    # Load the image data using Pillow's Image.open function
    image = Image.open(stream)

    # Display the image using Pillow's Image.show function
    image.show()


def test_line():
    param_map = {"type": "line",
                 "league": "eng2",
                 "player": "I. Sarr",
                 "stat": "Interceptions"}

    data_connector = DataConnector()
    data_map = data_connector.get_data(param_map)

    graph_connector = GraphConnector()
    graph = graph_connector.get_data(data_map)
    show_plot(graph)


def test_radar():
    param_map = {"type": "radar",
                 "league": "eng2",
                 "player": "I. Sarr"}

    data_connector = DataConnector()
    data_map = data_connector.get_data(param_map)

    graph_connector = GraphConnector()
    graph = graph_connector.get_data(data_map)
    show_plot(graph)


if __name__ == "__main__":
    test_radar()
    test_line()
