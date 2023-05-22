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
    param_map = {
        "type": "line",
        "player": "C. Cathcart",
        "compare": "Kiko Femenía",
        "stat": "Defensive duels / won",
        "start_date": "2016-09-25",
        "end_date": "2020-12-23"
    }

    data_connector = DataConnector()
    data_map = data_connector.get_data(param_map)

    graph_connector = GraphConnector()
    graph = graph_connector.get_data(data_map)
    show_plot(graph)


def test_radar():
    param_map = {"type": "radar",
                 "player": "Bruno Fernandes"}

    data_connector = DataConnector()
    data_map = data_connector.get_data(param_map)

    graph_connector = GraphConnector()
    graph = graph_connector.get_data(data_map)
    show_plot(graph)


def test_random():
    param_map = {"type": "random",
                 "graph_type": "radar"}

    data_connector = DataConnector()
    data_map = data_connector.get_data(param_map)

    graph_connector = GraphConnector()
    graph = graph_connector.get_data(data_map)
    show_plot(graph)


if __name__ == "__main__":
    # test_line()
    # test_radar()
    test_random()
