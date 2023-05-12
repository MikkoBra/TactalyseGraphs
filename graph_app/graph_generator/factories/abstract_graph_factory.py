from abc import ABC, abstractmethod

from ..graphs.abstract_models import Graph


class AbstractGraphFactory(ABC):
    """
    Abstract class representing a graph factory and its functionality.
    A graph factory is an object that is able to create a new graph based on a passed string parameter, and return it.
    This allows for the instantiation of new graphs without knowing the explicit graph type.
    """

    @abstractmethod
    def create_instance(self, param_map) -> Graph:
        """
        Creates a new graph instance based on the passed string parameter

        :param param_map: Map containing the type of graph to create, and the parameters needed for initialization.
        :return: The graph object represented by the factory and graph_type.
        """
        pass
