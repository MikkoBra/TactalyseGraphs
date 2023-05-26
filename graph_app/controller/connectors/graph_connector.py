from ...graph_generator.factories.graph_factory import GraphFactory


class GraphConnector:
    """
    Class that takes care of sending the preprocessed data from the data module to the graph module, and returning
    generated graphs as a list of byte strings. It does minimal data processing in the form of generating an object for
    the graph that should be generated, as well as a GraphFactory. It should not be used for actual data processing and
    matplotlib graph creation, as it is part of the controller module in the MVC pattern.
    """

    def __init__(self):
        super().__init__()
        self.__factory = GraphFactory()

    def get_data(self, param_map):
        """
        Function that passes the parameter map containing graph data to the create_graph function to return a list of
        graphs to the API endpoint.

        :param param_map: Map containing preprocessed football data to be used in a graph.
        :return: The graph(s) generated from the preprocessed data in byte form in a list.
        """
        return self.create_graph(param_map)

    def create_graph(self, param_map):
        """
        Function that creates an instance of the desired graph, invokes its draw function to create graph images,
        and returns them in a list. Currently, it only returns a single graph in a list.

        :param param_map: Map containing preprocessed football data to be used in a graph.
        :return: The graph(s) generated from the preprocessed data in byte form in a list.
        """
        plot_obj = self.__factory.create_instance(param_map)
        plot = plot_obj.draw_all(param_map)
        return plot

    @property
    def factory(self):
        """
        Getter for the factory attribute of the GraphConnector.

        :return: GraphFactory object representing the GraphConnector's graph factory.
        """
        return self.__factory

    @factory.setter
    def factory(self, value):
        """
        Setter fo the factory attribute of the GraphConnector.

        :param value: Factory object to set the factory attribute of the GraphConnector with.
        """
        self.__factory = value
