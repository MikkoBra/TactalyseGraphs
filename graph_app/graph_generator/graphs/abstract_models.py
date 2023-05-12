from abc import ABC, abstractmethod


class Graph(ABC):
    """
    Abstract class representing a graph and its functionality
    """

    @abstractmethod
    def __init__(self):
        """
        Constructor for graphs
        """
        pass

    @abstractmethod
    def draw(self, param_map) -> any:
        """
        Draws the graph based on passed data

        :param param_map: Map containing key/value pairs for all parameters needed for drawing the graph.
        :return: Image containing the drawn graph in byte form.
        """
        pass

    @abstractmethod
    def draw_all(self, param_map) -> any:
        """
        Draws the graph based on passed data

        :param param_map: Map containing key/value pairs for all parameters needed for drawing the graph.
        :return: Image containing the drawn graph in byte form.
        """
        pass
